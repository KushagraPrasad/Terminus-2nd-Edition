import json
import re
import subprocess
from contextlib import contextmanager
from pathlib import Path


APP = Path("/app")
OUT = APP / "output" / "layer_report.json"
CASE_LANE_IDS = (
    (APP / "docs" / "case_lane_ids.txt").read_text(encoding="utf-8").strip().split(",")
)
EXPECTED_TRACE_DIGEST = "001765f2"
MAIN_RS = APP / "m2/k81/src/main.rs"
Y5_RS = APP / "p7/y5/src/tie.rs"
Y4_RS = APP / "p7/y4/src/hold.rs"
GATE_MUX_RS = APP / "m2/k81/src/gate_mux.rs"
Y6_STRIDE_RS = APP / "p7/y6/src/stride.rs"
SHIPPED_Y6_STRIDE_RS = """pub fn step_1<F: FnMut(), G: FnMut()>(gate_first: bool, mut side: F, mut gate: G) -> u32 {
    if gate_first {
        gate();
        side();
        0u32
    } else {
        side();
        gate();
        1u32
    }
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
    subprocess.run([str(APP / "target" / "release" / "mk")], cwd=APP, check=True)
    return json.loads(OUT.read_text(encoding="utf-8"))


def _rows_by_id(report: dict) -> dict:
    return {row["scenario_id"]: row for row in report["rows"]}


def trace_digest_from_rows(rows: list[dict]) -> str:
    parts = []
    for row in rows:
        parts.append(
            f'{row["scenario_id"]}|{int(row["layer_ok"])}|{int(row["gen_ok"])}|'
            f'{int(row["mount_ok"])}|{row["drift_code"]}|{row["facet_hex"]}'
        )
    parts.sort()
    payload = "\n".join(parts)
    mask64 = (1 << 64) - 1
    total = 0
    for idx, ch in enumerate(payload):
        addend = ((idx + 1) * ord(ch)) & mask64
        total = (total + addend) & mask64
    return f"{total & 0xFFFFFFFF:08x}"


def _check_report_shape_and_scenario_table(report: dict) -> None:
    assert "rows" in report and "summary" in report
    ids = {row["scenario_id"] for row in report["rows"]}
    assert ids == set(CASE_LANE_IDS)
    assert report["summary"]["rows_total"] == len(CASE_LANE_IDS)


def _check_paired_mirror_agreement(report: dict) -> None:
    rows = _rows_by_id(report)
    pairs = [
        ("lowerdir", "lowerdir_echo"),
        ("upper", "upper_echo"),
        ("worker", "worker_echo"),
    ]
    for a, b in pairs:
        assert rows[a]["facet_hex"] == rows[b]["facet_hex"]
        assert rows[a]["layer_ok"] == rows[b]["layer_ok"]
        assert rows[a]["gen_ok"] == rows[b]["gen_ok"]
        assert rows[a]["mount_ok"] == rows[b]["mount_ok"]


def _check_layer_flags_and_drift_code_zero(report: dict) -> None:
    for row in report["rows"]:
        assert row["layer_ok"] is True
        assert row["gen_ok"] is True
        assert row["mount_ok"] is True
        assert row["drift_code"] == 0


def _check_summary_sync_status_aligned(report: dict) -> None:
    assert report["summary"]["sync_status"] == "settled"


def _check_tier_span_matches_drift_codes(report: dict) -> None:
    span = max(abs(r["drift_code"]) for r in report["rows"])
    assert report["summary"]["tier_span"] == span


def _check_trace_digest_matches_driver_contract(report: dict) -> None:
    assert report["summary"]["trace_digest"] == trace_digest_from_rows(report["rows"])


def _check_trace_digest_matches_known_good_output(report: dict) -> None:
    assert report["summary"]["trace_digest"] == EXPECTED_TRACE_DIGEST


def _check_facet_hex_format(report: dict) -> None:
    for row in report["rows"]:
        s = row["facet_hex"]
        assert len(s) == 16
        assert s == s.lower()
        int(s, 16)


def _check_summary_rows_total_integer(report: dict) -> None:
    assert isinstance(report["summary"]["rows_total"], int)
    assert report["summary"]["rows_total"] == len(report["rows"])


def _fold_key_uses_full_lineage(src: str) -> bool:
    match = re.search(
        r"pub fn fold_key\s*\([^)]*\)\s*->\s*u64\s*\{(.*?)^\}",
        src,
        re.DOTALL | re.MULTILINE,
    )
    assert match, "fold_key missing for ablation check"
    body = match.group(1)
    if "let _ = family_ix" in body or "let _ = prev_family" in body:
        return False
    return "family_ix" in body and "prev_family" in body and "<<" in body


def _apply_buggy_fold_key(src: str) -> str:
    patched, count = re.subn(
        r"pub fn fold_key\s*\([^)]*\)\s*->\s*u64\s*\{.*?\n\}",
        "pub fn fold_key(step_ix: usize, family_ix: u32, prev_family: u32) -> u64 {\n"
        "    let _ = family_ix;\n"
        "    let _ = prev_family;\n"
        "    (step_ix as u64) << 32\n"
        "}\n",
        src,
        count=1,
        flags=re.DOTALL,
    )
    assert count == 1, "fold_key body not found for ablation revert"
    return patched


def _strip_merge_storage_refresh(src: str) -> str:
    patched, count = re.subn(
        r"\n\s*state\.storage = \*incoming;\n(?=\s*state\.last_b = stamp_b;)",
        "\n",
        src,
        count=1,
    )
    assert count == 1, "merge_pack storage refresh missing for ablation revert"
    return patched


def _force_gate_first_true_at_combine(src: str) -> str:
    patched = re.sub(r"step_1\s*\(\s*false\s*,", "step_1(true,", src, count=1)
    if patched != src:
        return patched
    return re.sub(r"step_1\s*\(\s*true\s*,", "step_1(true,", src, count=1)


def _bump_lowerdir_ladder_tail_step(main_src: str) -> str:
    def repl_lowerdir_block(match: re.Match[str]) -> str:
        block = match.group(0)
        updated, count = re.subn(
            r"\(\s*1\s*,\s*1\s*\)(\s*\])",
            r"(2, 1)\1",
            block,
            count=1,
        )
        assert count == 1, "lowerdir ladder tail step missing for mutation test"
        return updated

    patched, count = re.subn(
        r'"lowerdir",\s*vec!\[[^\]]*\]',
        repl_lowerdir_block,
        main_src,
        count=1,
    )
    assert count == 1, "lowerdir ladder block missing for mutation test"
    return patched


def _assert_not_fully_coherent(report: dict) -> None:
    rows = _rows_by_id(report)
    pairs = [
        ("lowerdir", "lowerdir_echo"),
        ("upper", "upper_echo"),
        ("worker", "worker_echo"),
    ]
    mirror_ok = all(
        rows[a]["facet_hex"] == rows[b]["facet_hex"]
        and rows[a]["layer_ok"] == rows[b]["layer_ok"]
        and rows[a]["gen_ok"] == rows[b]["gen_ok"]
        and rows[a]["mount_ok"] == rows[b]["mount_ok"]
        for a, b in pairs
    )
    closure_ok = all(
        r["layer_ok"] and r["gen_ok"] and r["mount_ok"] and r["drift_code"] == 0
        for r in report["rows"]
    )
    reload_ok = report["summary"]["sync_status"] == "settled"
    assert not (mirror_ok and closure_ok and reload_ok)


def test_report_rows_and_scenario_table() -> None:
    """JSON exposes rows and summary; case lane ids match the shipped table file."""
    _check_report_shape_and_scenario_table(_build_and_run())


def test_paired_mirror_agreement() -> None:
    """Paired case lanes agree on facet and closure fields when coherent."""
    _check_paired_mirror_agreement(_build_and_run())


def test_all_layer_flags_and_drift_code_zero() -> None:
    """Healthy run: closure integers read zero and all three booleans are true."""
    _check_layer_flags_and_drift_code_zero(_build_and_run())


def test_summary_sync_status_aligned() -> None:
    """Summary sync line reads settled when the row matrix is fully consistent."""
    _check_summary_sync_status_aligned(_build_and_run())


def test_tier_span_matches_drift_codes() -> None:
    """tier_span equals max absolute drift_code across rows."""
    _check_tier_span_matches_drift_codes(_build_and_run())


def test_trace_digest_matches_driver_contract() -> None:
    """trace_digest matches the driver module documentation reduction."""
    _check_trace_digest_matches_driver_contract(_build_and_run())


def test_trace_digest_matches_known_good_output() -> None:
    """trace_digest is anchored to the known-good repaired emission."""
    _check_trace_digest_matches_known_good_output(_build_and_run())


def test_facet_hex_format() -> None:
    """facet_hex is sixteen lowercase hex characters."""
    _check_facet_hex_format(_build_and_run())


def test_summary_rows_total_integer() -> None:
    """rows_total is an integer matching len(rows)."""
    _check_summary_rows_total_integer(_build_and_run())


def test_pipeline_overwrites_hand_written_json() -> None:
    """A stale hand-written report is replaced when cargo rebuilds and mk reruns."""
    baseline = _build_and_run()
    tampered = {
        **baseline,
        "summary": {**baseline["summary"], "sync_status": "split"},
    }
    OUT.write_text(json.dumps(tampered), encoding="utf-8")
    regenerated = _build_and_run()
    _check_layer_flags_and_drift_code_zero(regenerated)
    _check_summary_sync_status_aligned(regenerated)
    assert regenerated["summary"]["trace_digest"] == EXPECTED_TRACE_DIGEST


def test_consecutive_pipeline_runs_are_identical() -> None:
    """Back-to-back rebuild-and-run emissions match, proving a stable pipeline path."""
    first = _build_and_run()
    second = _build_and_run()
    assert first["summary"]["trace_digest"] == second["summary"]["trace_digest"]
    assert first["rows"] == second["rows"]


def test_lowerdir_ladder_driver_sensitivity() -> None:
    """Changing the lowerdir bind ladder in source changes the emitted stamp via mk."""
    baseline = _build_and_run()
    original_stamp = _rows_by_id(baseline)["lowerdir"]["facet_hex"]
    original_digest = baseline["summary"]["trace_digest"]

    main_src = MAIN_RS.read_text(encoding="utf-8")
    with _patched_text(MAIN_RS, _bump_lowerdir_ladder_tail_step(main_src)):
        mutated = _build_and_run()

    mutated_lowerdir = _rows_by_id(mutated)["lowerdir"]
    assert mutated_lowerdir["facet_hex"] != original_stamp
    assert mutated["summary"]["trace_digest"] != original_digest
    assert mutated["summary"]["trace_digest"] == trace_digest_from_rows(mutated["rows"])


def test_fold_bits_ablation_breaks_coherence() -> None:
    """Reverting stamp fold to the shipped broken form breaks coherent bind output."""
    tie_src = Y5_RS.read_text(encoding="utf-8")
    assert _fold_key_uses_full_lineage(tie_src), "repaired fold_key missing for ablation test"
    with _patched_text(Y5_RS, _apply_buggy_fold_key(tie_src)):
        report = _build_and_run()
    _assert_not_fully_coherent(report)


def test_dual_crate_ablation_breaks_pipeline() -> None:
    """Reverting both pack-merge and stamp-fold fixes prevents a healthy pipeline run."""
    tie_src = Y5_RS.read_text(encoding="utf-8")
    hold_src = Y4_RS.read_text(encoding="utf-8")
    assert _fold_key_uses_full_lineage(tie_src), "repaired fold_key missing for ablation test"
    assert "state.storage = *incoming" in hold_src, "repaired merge_pack branch missing for ablation test"
    reverted_tie = _apply_buggy_fold_key(tie_src)
    reverted_hold = _strip_merge_storage_refresh(hold_src)
    with _patched_text(Y5_RS, reverted_tie):
        with _patched_text(Y4_RS, reverted_hold):
            try:
                report = _build_and_run()
            except subprocess.CalledProcessError:
                return
    _assert_not_fully_coherent(report)


def test_invalidation_order_ablation_breaks_closure() -> None:
    """Shipped-broken gate wiring with the stock helper breaks per-step closure flags."""
    wire_src = GATE_MUX_RS.read_text(encoding="utf-8")
    broken_wire = _force_gate_first_true_at_combine(wire_src)
    with _patched_text(GATE_MUX_RS, broken_wire):
        with _patched_text(Y6_STRIDE_RS, SHIPPED_Y6_STRIDE_RS):
            report = _build_and_run()
    _assert_not_fully_coherent(report)
