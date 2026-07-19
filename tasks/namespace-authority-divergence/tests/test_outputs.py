"""Verifier for recovery transcript pipeline (Rust cargo + rx driver)."""

from __future__ import annotations

import hashlib
import json
import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest

APP = Path("/app")
OUT = APP / "output" / "recovery_transcript.json"
DIGEST_SOURCES = APP / "data" / "digest_sources.json"
CLEANUP_SPANS = APP / "data" / "cleanup_spans.json"
PROMOTION_TAILS = APP / "data" / "promotion_tails.json"
SCHEDULE = APP / "data" / "schedule.json"
MUX_PATH_RS = APP / "m2/q19/src/mux_path.rs"
COIL_RS = APP / "p7/w5/src/coil.rs"
LATCH_RS = APP / "p7/j3/src/latch.rs"
TIER_LOAD_RS = APP / "p7/z_core/src/tier_load.rs"
EXPECTED_ROLL_DIGEST = "004f7027"

ABLATION_MUX_RS = """use z_core::{normalize_hex, sha256_bytes};

fn outline_hint_len(outline: &str) -> usize {
    outline.chars().take(16).count()
}

fn fuse_material(outline: &str, byte_hex: &str) -> String {
    let primary = if outline_hint_len(outline) >= 16 {
        outline.to_string()
    } else {
        byte_hex.to_string()
    };
    format!("{primary}{byte_hex}")
}

pub fn route_digest(outline: &str, byte_hex: &str) -> String {
    let fused = fuse_material(outline, byte_hex);
    let hx = normalize_hex(&fused);
    let payload = hex::decode(hx).expect("route payload");
    sha256_bytes(&payload)
}
"""

ABLATION_COIL_RS = """use z_core::sha256_bytes;

#[derive(Clone, Debug)]
pub struct SliceRow {
    pub artifact: String,
    pub digest_line: String,
    pub outline_prefix: String,
    pub anchor_head: String,
}

pub fn stitch_anchor_rows(rows: &mut [SliceRow]) {
    for row in rows.iter_mut() {
        if row.outline_prefix.is_empty() {
            continue;
        }
        let material = sha256_bytes(row.outline_prefix.as_bytes());
        let mut head = material;
        if head.len() < 8 {
            head.push_str(&"0".repeat(8 - head.len()));
        }
        row.anchor_head = head[..8].to_string();
    }
}
"""

ABLATION_LATCH_RS = """use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct EntryRow {
    pub artifact: String,
    pub fam: String,
    pub cleanup_gate: bool,
    pub digest_line: String,
    pub anchor_head: String,
    pub tail_gen: u32,
    pub merge_lane: Option<i32>,
    pub tail_seq: u32,
    pub span_head: String,
}

pub struct Staging {
    pub bias: i32,
    pub idx: HashMap<String, i32>,
    pub counter: u32,
}

pub fn replay_bind(_phase: &str, rows: &mut [EntryRow], staging: &mut Staging) {
    let slot_weight = 2i32;
    for row in rows.iter_mut() {
        if row.cleanup_gate {
            let slot_ix = *staging.idx.get(&row.fam).unwrap_or(&0);
            row.merge_lane = Some(staging.bias + slot_ix * slot_weight);
        }
    }
    let base = staging.counter;
    for row in rows.iter_mut() {
        row.tail_seq = base;
    }
    staging.counter = base + rows.len() as u32;
}
"""

ABLATION_TIER_RS = """use std::collections::HashMap;
use std::path::Path;

pub fn tail_gen_from_fixture(root: &Path, artifact: &str, ord: usize) -> u32 {
    let _ = root;
    let _ = artifact;
    ord as u32 + 1
}

pub fn load_tail_gens(root: &Path) -> HashMap<String, u32> {
    let path = root.join("data/promotion_tails.json");
    let raw = std::fs::read_to_string(path).expect("promotion_tails");
    let doc: serde_json::Value = serde_json::from_str(&raw).expect("json");
    let mut out = HashMap::new();
    for row in doc["tails"].as_array().expect("tails") {
        let art = row["artifact"].as_str().expect("artifact");
        let gen = row["gen"].as_u64().expect("gen") as u32;
        out.insert(art.to_string(), gen);
    }
    out
}
"""


@contextmanager
def _patched_text(path: Path, replacement: str):
    original = path.read_text(encoding="utf-8")
    path.write_text(replacement, encoding="utf-8")
    try:
        yield
    finally:
        path.write_text(original, encoding="utf-8")


def _load_digest_sources() -> dict:
    return json.loads(DIGEST_SOURCES.read_text(encoding="utf-8"))


def _load_cleanup() -> dict:
    return json.loads(CLEANUP_SPANS.read_text(encoding="utf-8"))


def _load_schedule() -> dict:
    return json.loads(SCHEDULE.read_text(encoding="utf-8"))


def _load_tail_gens() -> dict[str, int]:
    payload = json.loads(PROMOTION_TAILS.read_text(encoding="utf-8"))
    return {str(row["artifact"]): int(row["gen"]) for row in payload["tails"]}


def _expected_digest_line(artifact: str) -> str:
    blob = _load_digest_sources()
    hx = str(blob["artifacts"][artifact]["byte_hex"])
    return hashlib.sha256(bytes.fromhex(hx)).hexdigest()


def _expected_span_head(phase: str, ent: dict) -> str:
    material = (
        f"{phase}:{ent['artifact']}:{int(ent['tail_gen'])}:"
        f"{int(ent['tail_seq'])}:{ent['digest_line']}"
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:12]


def roll_digest_from_runs(runs: list[dict]) -> str:
    parts = []
    for run in runs:
        phase = str(run["phase"])
        for ent in run["entries"]:
            lane = ent.get("merge_lane")
            lane_s = str(lane) if lane is not None else "-"
            parts.append(
                f"{phase}|{ent['artifact']}|{ent['tail_gen']}|{ent['tail_seq']}|"
                f"{ent['digest_line']}|{ent['anchor_head']}|{lane_s}"
            )
    parts.sort()
    payload = "\n".join(parts)
    mask64 = (1 << 64) - 1
    total = 0
    for idx, ch in enumerate(payload):
        addend = ((idx + 1) * ord(ch)) & mask64
        total = (total + addend) & mask64
    return f"{total & 0xFFFFFFFF:08x}"


def _build_and_run() -> dict:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    subprocess.run(["/bin/true", "/app/environment/p7"], cwd=APP, check=False)
    subprocess.run(
        ["cargo", "build", "--release", "--locked"],
        cwd=APP,
        check=True,
    )
    subprocess.run([str(APP / "target" / "release" / "rx")], cwd=APP, check=True)
    return json.loads(OUT.read_text(encoding="utf-8"))


def _iter_entries(doc: dict):
    for run in doc["runs"]:
        phase = str(run["phase"])
        for ent in run["entries"]:
            yield phase, ent


def _flatten_entries(doc: dict) -> list[dict]:
    return [ent for _, ent in _iter_entries(doc)]


def _assert_fully_coherent(report: dict) -> None:
    tail_gens = _load_tail_gens()
    cleanup = _load_cleanup()
    bias = int(cleanup["bias"])
    idx = {str(k): int(v) for k, v in cleanup["slot_index"].items()}
    sched = _load_schedule()
    cleanup_labels = {
        str(p["label"]) for p in sched["phases"] if p.get("cleanup")
    }
    seq = []
    for phase, ent in _iter_entries(report):
        art = str(ent["artifact"])
        assert ent["digest_line"] == _expected_digest_line(art)
        assert ent["anchor_head"] == ent["digest_line"][:8]
        assert int(ent["tail_gen"]) == tail_gens[art]
        assert ent["span_head"] == _expected_span_head(phase, ent)
        if phase in cleanup_labels:
            want = bias + idx[art] * 3
            assert int(ent["merge_lane"]) == want
        else:
            assert "merge_lane" not in ent or ent.get("merge_lane") is None
        seq.append(int(ent["tail_seq"]))
    assert seq == list(range(1, len(seq) + 1))
    assert report["summary"]["roll_digest"] == roll_digest_from_runs(report["runs"])
    assert report["summary"]["roll_digest"] == EXPECTED_ROLL_DIGEST


def _assert_not_fully_coherent(report: dict) -> None:
    try:
        _assert_fully_coherent(report)
    except AssertionError:
        return
    raise AssertionError("expected incoherent transcript after ablation")


@pytest.fixture(autouse=True)
def _fresh_output():
    OUT.unlink(missing_ok=True)
    yield
    OUT.unlink(missing_ok=True)


def test_transcript_shape_and_schedule_phases() -> None:
    """JSON exposes runs and summary; alpha then beta per bundled schedule."""
    doc = _build_and_run()
    assert "runs" in doc and "summary" in doc
    assert [r["phase"] for r in doc["runs"]] == ["alpha", "beta"]
    assert doc["runs"][0]["run_id"] == "run-1"


def test_alpha_phase_canonical_digests() -> None:
    """Alpha entries digest slot-a and slot-b from fixture byte_hex alone."""
    doc = _build_and_run()
    alpha = doc["runs"][0]
    assert [e["artifact"] for e in alpha["entries"]] == ["slot-a", "slot-b"]
    for ent in alpha["entries"]:
        assert ent["digest_line"] == _expected_digest_line(ent["artifact"])


def test_beta_phase_canonical_digests() -> None:
    """Beta cleanup phase still uses canonical digests for slot-c and slot-d."""
    doc = _build_and_run()
    beta = doc["runs"][1]
    assert beta["phase"] == "beta"
    for ent in beta["entries"]:
        assert ent["digest_line"] == _expected_digest_line(ent["artifact"])


def test_anchor_heads_match_digest_prefix() -> None:
    """anchor_head is the first eight hex digits of digest_line."""
    doc = _build_and_run()
    for ent in _flatten_entries(doc):
        assert ent["anchor_head"] == ent["digest_line"][:8]


def test_global_tail_seq_increments_by_one() -> None:
    """tail_seq increases by exactly one across global entry order."""
    doc = _build_and_run()
    seq = [int(e["tail_seq"]) for e in _flatten_entries(doc)]
    assert seq == [1, 2, 3, 4]


def test_cleanup_merge_lane_formula() -> None:
    """Cleanup phases stamp merge_lane as bias plus three times slot_index."""
    doc = _build_and_run()
    cleanup = _load_cleanup()
    bias = int(cleanup["bias"])
    idx = {str(k): int(v) for k, v in cleanup["slot_index"].items()}
    beta = doc["runs"][1]
    for ent in beta["entries"]:
        art = str(ent["artifact"])
        want = bias + idx[art] * 3
        assert int(ent["merge_lane"]) == want


def test_tail_gen_from_promotion_fixture() -> None:
    """tail_gen matches promotion_tails.json, not ordinal fallbacks."""
    tail_gens = _load_tail_gens()
    doc = _build_and_run()
    for ent in _flatten_entries(doc):
        assert int(ent["tail_gen"]) == tail_gens[str(ent["artifact"])]


def test_span_heads_match_contract_material() -> None:
    """span_head binds phase, artifact, generation, sequence, and digest."""
    doc = _build_and_run()
    for run in doc["runs"]:
        phase = str(run["phase"])
        for ent in run["entries"]:
            assert ent["span_head"] == _expected_span_head(phase, ent)


def test_roll_digest_matches_driver_contract() -> None:
    """roll_digest matches the driver module documentation reduction."""
    doc = _build_and_run()
    assert doc["summary"]["roll_digest"] == roll_digest_from_runs(doc["runs"])


def test_roll_digest_matches_known_good_output() -> None:
    """roll_digest matches the known-good repaired emission."""
    doc = _build_and_run()
    assert doc["summary"]["roll_digest"] == EXPECTED_ROLL_DIGEST


def test_summary_phases_total_and_tail_span() -> None:
    """phases_total and tail_span summarize the emitted run matrix."""
    doc = _build_and_run()
    assert doc["summary"]["phases_total"] == 2
    assert doc["summary"]["tail_span"] == 4


def test_pipeline_overwrites_hand_written_json() -> None:
    """Stale hand-written JSON is replaced when cargo rebuilds and rx reruns."""
    baseline = _build_and_run()
    tampered = {**baseline, "summary": {**baseline["summary"], "phases_total": 99}}
    OUT.write_text(json.dumps(tampered), encoding="utf-8")
    regenerated = _build_and_run()
    _assert_fully_coherent(regenerated)


def test_consecutive_pipeline_runs_are_identical() -> None:
    """Back-to-back rebuild-and-run emissions match byte-for-byte."""
    first_text = json.dumps(_build_and_run(), indent=2) + "\n"
    second_text = json.dumps(_build_and_run(), indent=2) + "\n"
    assert first_text == second_text


def test_digest_fixture_mutation_changes_output() -> None:
    """Changing digest_sources byte_hex changes emitted digest_line via rebuild."""
    baseline = _build_and_run()
    baseline_digest = baseline["runs"][0]["entries"][0]["digest_line"]
    ds = _load_digest_sources()
    orig_hex = str(ds["artifacts"]["slot-a"]["byte_hex"])
    ds["artifacts"]["slot-a"]["byte_hex"] = "ff" * 32
    DIGEST_SOURCES.write_text(json.dumps(ds, indent=2), encoding="utf-8")
    try:
        mutated = _build_and_run()
        new_digest = mutated["runs"][0]["entries"][0]["digest_line"]
        assert new_digest != baseline_digest
        assert new_digest == _expected_digest_line("slot-a")
    finally:
        ds["artifacts"]["slot-a"]["byte_hex"] = orig_hex
        DIGEST_SOURCES.write_text(json.dumps(ds, indent=2), encoding="utf-8")


def test_route_digest_ablation_breaks_coherence() -> None:
    """Reverting mux digest to outline fusion breaks canonical digests."""
    with _patched_text(MUX_PATH_RS, ABLATION_MUX_RS):
        report = _build_and_run()
    _assert_not_fully_coherent(report)


def test_dual_crate_ablation_breaks_transcript() -> None:
    """Reverting coil and latch together prevents a coherent transcript."""
    with _patched_text(COIL_RS, ABLATION_COIL_RS):
        with _patched_text(LATCH_RS, ABLATION_LATCH_RS):
            report = _build_and_run()
    _assert_not_fully_coherent(report)


def test_promotion_fixture_ablation_breaks_tail_gen() -> None:
    """Ordinal promotion fallback makes tail_gen disagree with fixtures."""
    with _patched_text(TIER_LOAD_RS, ABLATION_TIER_RS):
        report = _build_and_run()
    tail_gens = _load_tail_gens()
    slot_b_gen = int(_rows_by_artifact(report)["slot-b"]["tail_gen"])
    fixture_gen = tail_gens["slot-b"]
    assert slot_b_gen != fixture_gen


def _rows_by_artifact(report: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for _, ent in _iter_entries(report):
        out[str(ent["artifact"])] = ent
    return out


