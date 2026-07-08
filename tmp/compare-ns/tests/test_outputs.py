"""Verifier for recovery transcript pipeline with digest, anchor, lane, and span validation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
ENV = APP / "environment"
OUT = APP / "output" / "recovery_transcript.json"
DIGEST_SOURCES = ENV / "studio" / "app" / "data" / "digest_sources.json"
CLEANUP_SPANS = ENV / "studio" / "app" / "data" / "cleanup_spans.json"
SCHEDULE = ENV / "studio" / "app" / "data" / "schedule.json"
PROMOTION_TAILS = ENV / "studio" / "app" / "data" / "promotion_tails.json"


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


def _run_regen() -> None:
    OUT.unlink(missing_ok=True)
    subprocess.run(
        [
            "python3",
            "/app/environment/runner.py",
            "--write",
            "/app/output/recovery_transcript.json",
        ],
        check=True,
        cwd="/app",
        timeout=120,
    )


def _load_transcript() -> dict:
    return json.loads(OUT.read_text(encoding="utf-8"))


def _flatten_entries(doc: dict) -> list[dict]:
    out: list[dict] = []
    for run in doc["runs"]:
        out.extend(run["entries"])
    return out


@pytest.fixture(autouse=True)
def _fresh_output():
    OUT.unlink(missing_ok=True)
    yield
    OUT.unlink(missing_ok=True)


def test_t01_alpha_phase_digests():
    """Alpha phase entries use canonical byte digests."""
    _run_regen()
    doc = _load_transcript()
    assert doc["runs"][0]["phase"] == "alpha"
    alpha = doc["runs"][0]
    assert alpha["run_id"] == "run-1"
    assert alpha["steps"] == ["collect-alpha", "merge-alpha"]
    arts = [e["artifact"] for e in alpha["entries"]]
    assert arts == ["slot-a", "slot-b"]
    for ent in alpha["entries"]:
        assert ent["digest_line"] == _expected_digest_line(ent["artifact"])


def test_t02_beta_phase_digests():
    """Beta phase entries still use canonical digests for their artifacts."""
    _run_regen()
    doc = _load_transcript()
    assert doc["runs"][1]["phase"] == "beta"
    beta = doc["runs"][1]
    assert beta["run_id"] == "run-1"
    assert beta["steps"] == ["collect-beta", "merge-beta"]
    arts = [e["artifact"] for e in beta["entries"]]
    assert arts == ["slot-c", "slot-d"]
    for ent in beta["entries"]:
        assert ent["digest_line"] == _expected_digest_line(ent["artifact"])


def test_t03_anchor_heads():
    """Anchor heads track digest_line prefixes."""
    _run_regen()
    for ent in _flatten_entries(_load_transcript()):
        assert ent["anchor_head"] == ent["digest_line"][:8]


def test_t04_lane_trace():
    """tail_seq is strictly +1 across global entry order."""
    _run_regen()
    seq = [int(e["tail_seq"]) for e in _flatten_entries(_load_transcript())]
    assert seq == list(range(1, len(seq) + 1))


def test_t05_rerun_stability():
    """Regeneration is idempotent on disk."""
    _run_regen()
    first = OUT.read_text(encoding="utf-8")
    _run_regen()
    second = OUT.read_text(encoding="utf-8")
    assert first == second


def test_t06_slot_crosscut():
    """Cleanup phases apply bias + 3 * slot_index to merge_lane."""
    cleanup = _load_cleanup()
    bias = int(cleanup["bias"])
    idx = {str(k): int(v) for k, v in cleanup["slot_index"].items()}
    _run_regen()
    doc = _load_transcript()
    sched = _load_schedule()
    cleanup_labels = {str(p["label"]) for p in sched["phases"] if p.get("cleanup")}
    for run in doc["runs"]:
        if run["phase"] not in cleanup_labels:
            for ent in run["entries"]:
                assert "merge_lane" not in ent
            continue
        for ent in run["entries"]:
            fam = str(ent["artifact"])
            want = bias + idx[fam] * 3
            assert int(ent["merge_lane"]) == want


def test_t07_tail_generations():
    """Every entry carries the generation bound to its promotion-tail fixture."""
    tail_gens = _load_tail_gens()
    _run_regen()
    for ent in _flatten_entries(_load_transcript()):
        artifact = str(ent["artifact"])
        assert int(ent["tail_gen"]) == tail_gens[artifact]


def test_t08_replay_span_heads():
    """Span heads bind phase, artifact, generation, tail order, and emitted digest."""
    _run_regen()
    for run in _load_transcript()["runs"]:
        phase = str(run["phase"])
        for ent in run["entries"]:
            assert ent["span_head"] == _expected_span_head(phase, ent)


def test_t09_perturbation_detects_data_changes():
    """Pipeline must read data files dynamically; hardcoded output would fail."""
    _run_regen()
    baseline = _load_transcript()
    baseline_digest = baseline["runs"][0]["entries"][0]["digest_line"]
    ds = _load_digest_sources()
    orig_hex = str(ds["artifacts"]["slot-a"]["byte_hex"])
    ds["artifacts"]["slot-a"]["byte_hex"] = "ff" * 32
    DIGEST_SOURCES.write_text(json.dumps(ds, indent=2), encoding="utf-8")
    try:
        _run_regen()
        perturbed = _load_transcript()
        perturbed_digest = perturbed["runs"][0]["entries"][0]["digest_line"]
        assert perturbed_digest != baseline_digest, "output must change when input data changes"
    finally:
        ds["artifacts"]["slot-a"]["byte_hex"] = orig_hex
        DIGEST_SOURCES.write_text(json.dumps(ds, indent=2), encoding="utf-8")


def test_t10_digest_uses_probe_bytes_only():
    """The digest primitive must use probe byte_hex alone, not combined sources."""
    import sys
    sys.path.insert(0, str(ENV))
    from wal_slots.first_core import n_quench_u
    ctx = {"fam": "test"}
    ledger = {"outline": "aabbccdd" * 4}
    probe = {"byte_hex": "00aa" * 16}
    result = n_quench_u(ctx, ledger, probe)
    expected = hashlib.sha256(bytes.fromhex("00aa" * 16)).hexdigest()
    assert result == expected, "digest must use probe byte_hex alone"


def test_t11_anchor_derives_from_digest():
    """Anchor derivation must use digest_line, not outline-side material."""
    import sys
    sys.path.insert(0, str(ENV))
    from co_emitters.mid_slice import n_stitch_v
    slices = [{"digest_line": "abcd1234" + "00" * 28, "outline_prefix": "wxyz" * 4}]
    n_stitch_v({}, slices, {})
    assert slices[0]["anchor_head"] == "abcd1234", "anchor_head must be first 8 chars of digest_line"


def test_t12_lane_and_span_computed_correctly():
    """Replay logic must compute lane arithmetic and span heads correctly."""
    import sys
    sys.path.insert(0, str(ENV))
    from journal_apply.last_apply import n_bind_w
    rows = [{"cleanup_gate": True, "fam": "slot-a", "artifact": "slot-a", "tail_gen": 5, "digest_line": "ff" * 32}]
    staging = {"bias": 10, "idx": {"slot-a": 2}, "counter": [1]}
    result = n_bind_w({"label": "beta"}, {"rows": rows}, staging)
    assert int(result[0]["merge_lane"]) == 10 + 2 * 3, "cleanup lane must use bias + idx * 3"
    assert int(result[0]["tail_seq"]) == 1, "first row must get tail_seq 1"
    assert len(result[0]["span_head"]) == 12, "span_head must be 12 hex chars"
    assert all(c in "0123456789abcdef" for c in result[0]["span_head"]), "span_head must be lowercase hex"
