import json
import re
import subprocess
from contextlib import contextmanager
from pathlib import Path

APP = Path("/app")
OUT = APP / "output" / "report.json"
CASE_LANE_IDS = (
    (APP / "docs" / "case_lane_ids.txt").read_text(encoding="utf-8").strip().split(",")
)
EXPECTED_TRACE_DIGEST = "00213dcf"
MAIN_RS = APP / "m2/k81/src/main.rs"
STEP_KEY_RS = APP / "m2/k81/src/step_key.rs"
STACK_MIX_RS = APP / "m2/k81/src/stack_mix.rs"
Y5_RS = APP / "p7/y5/src/tie.rs"
Y4_RS = APP / "p7/y4/src/hold.rs"
GATE_MUX_RS = APP / "m2/k81/src/gate_mux.rs"
Y6_STRIDE_RS = APP / "p7/y6/src/stride.rs"
WAL_RS = APP / "p7/wal_store/src/lib.rs"
LANE_RS = APP / "p7/lane_gate/src/lib.rs"
FOLD_RS = APP / "p7/fold_row/src/lib.rs"
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
    subprocess.run([str(APP / "target" / "release" / "journal_run")], cwd=APP, check=True)
    return json.loads(OUT.read_text(encoding="utf-8"))


def _rows_by_id(report: dict) -> dict:
    return {row["scenario_id"]: row for row in report["rows"]}


def trace_digest_from_rows(rows: list[dict]) -> str:
    parts = []
    for row in rows:
        parts.append(
            f'{row["scenario_id"]}|{int(row["replay_ok"])}|{int(row["lane_ok"])}|'
            f'{int(row["fold_ok"])}|{int(row["seal_ok"])}|{row["drift_code"]}|{row["facet_hex"]}'
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
        ("cold", "cold_echo"),
        ("replay_compact", "replay_compact_echo"),
        ("wal_restart", "wal_restart_echo"),
    ]
    for a, b in pairs:
        assert rows[a]["facet_hex"] == rows[b]["facet_hex"]
        assert rows[a]["replay_ok"] == rows[b]["replay_ok"]
        assert rows[a]["lane_ok"] == rows[b]["lane_ok"]
        assert rows[a]["fold_ok"] == rows[b]["fold_ok"]
        assert rows[a]["seal_ok"] == rows[b]["seal_ok"]


def _check_closure_flags_and_drift_code_zero(report: dict) -> None:
    for row in report["rows"]:
        assert row["replay_ok"] is True
        assert row["lane_ok"] is True
        assert row["fold_ok"] is True
        assert row["seal_ok"] is True
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


def _revert_hold_storage_refresh(src: str) -> str:
    """Restore the shipped-broken else-if branch regardless of fix ordering."""
    patched, count = re.subn(
        r"(} else if state\.last_b != stamp_b \{)(.*?)(    \})",
        r"\1\n        state.last_b = stamp_b;\n\3",
        src,
        count=1,
        flags=re.DOTALL,
    )
    assert count == 1, "merge_pack else-if branch missing for ablation revert"
    return patched


def _step_key_delegates_to_fold_key(src: str) -> bool:
    match = re.search(
        r"pub fn step_key\s*\([^)]*\)\s*->\s*u64\s*\{(.*?)^\}",
        src,
        re.DOTALL | re.MULTILINE,
    )
    assert match, "step_key missing for wiring check"
    body = match.group(1)
    if "fold_key(" not in body:
        return False
    without_call = re.sub(r"fold_key\s*\([^)]*\)", "", body)
    return not re.search(r"<<\s*32", without_call)


def _gate_mux_delegates_to_stride_helper(src: str) -> bool:
    match = re.search(
        r"pub fn mux_combine\s*<[^>]+>\s*\([^)]*\)\s*->\s*u32\s*\{(.*?)^\}",
        src,
        re.DOTALL | re.MULTILINE,
    )
    assert match, "mux_combine missing for wiring check"
    body = match.group(1)
    if "step_1(" not in body:
        return False
    return "gate_first" not in body


def _stack_mix_calls_merge_pack(src: str) -> bool:
    return "fn stack_apply" in src and "merge_pack(" in src


def _force_gate_first_true_at_combine(src: str) -> str:
    patched = re.sub(r"step_1\s*\(\s*false\s*,", "step_1(true,", src, count=1)
    if patched != src:
        return patched
    return re.sub(r"step_1\s*\(\s*true\s*,", "step_1(true,", src, count=1)


def _apply_shipped_wal_replay_reverse(src: str) -> str:
    patched, count = re.subn(
        r"pub fn replay_compact\(book: &WalBook\) -> Vec<u64> \{.*?\n\}",
        "pub fn replay_compact(book: &WalBook) -> Vec<u64> {\n"
        "    let mut out = book.segments.clone();\n"
        "    out.reverse();\n"
        "    out\n"
        "}",
        src,
        count=1,
        flags=re.DOTALL,
    )
    assert count == 1, "replay_compact body not found for ablation revert"
    return patched


def _revert_lane_gate(src: str) -> str:
    return """/// Lane timing gate: minimum span length 12 bytes, window at least 90 ms, byte sum ≡ 3 (mod 7).
pub fn lane_window_ok(window_ms: u64, bytes: &[u8]) -> bool {
    if bytes.len() < 12 {
        return false;
    }
    let ms = window_ms;
    if ms < 5 {
        return false;
    }
    (ms % 2) == 0
}
"""


def _fold_gate_exercises_pick_row(src: str) -> bool:
    match = re.search(
        r"pub fn fold_gate_ok\s*\([^)]*\)\s*->\s*bool\s*\{(.*?)^\}",
        src,
        re.DOTALL | re.MULTILINE,
    )
    assert match, "fold_gate_ok missing for ablation check"
    body = match.group(1)
    if re.search(r"^\s*true\s*$", body.strip(), re.MULTILINE):
        return False
    return "pick_row" in body


def _apply_shipped_pick_row(src: str) -> str:
    shipped_fn = (
        "pub fn pick_row(left: &[u8], right: &[u8]) -> Vec<u8> {\n"
        "    if left.len() < 3 || right.len() < 3 {\n"
        "        return Vec::new();\n"
        "    }\n"
        "    if left[0] == right[0] {\n"
        "        let lt = &left[2..];\n"
        "        let rt = &right[2..];\n"
        "        if lt < rt {\n"
        "            left.to_vec()\n"
        "        } else {\n"
        "            right.to_vec()\n"
        "        }\n"
        "    } else if left[0] > right[0] {\n"
        "        left.to_vec()\n"
        "    } else {\n"
        "        right.to_vec()\n"
        "    }\n"
        "}"
    )
    patched, count = re.subn(
        r"pub fn pick_row\s*\([^)]*\)\s*->\s*Vec<u8>\s*\{.*?\n\}",
        shipped_fn + "\n",
        src,
        count=1,
        flags=re.DOTALL,
    )
    assert count == 1, "pick_row body not found for ablation revert"
    return patched


def _bump_cold_ladder_tail_step(main_src: str) -> str:
    def repl_cold_block(match: re.Match[str]) -> str:
        block = match.group(0)
        updated, count = re.subn(
            r"\(\s*1\s*,\s*1\s*\)(\s*\])",
            r"(2, 1)\1",
            block,
            count=1,
        )
        assert count == 1, "cold ladder tail step missing for mutation test"
        return updated

    patched, count = re.subn(
        r'"cold",\s*vec!\[[^\]]*\]',
        repl_cold_block,
        main_src,
        count=1,
    )
    assert count == 1, "cold ladder block missing for mutation test"
    return patched


def _assert_not_fully_coherent(report: dict) -> None:
    rows = _rows_by_id(report)
    pairs = [
        ("cold", "cold_echo"),
        ("replay_compact", "replay_compact_echo"),
        ("wal_restart", "wal_restart_echo"),
    ]
    mirror_ok = all(
        rows[a]["facet_hex"] == rows[b]["facet_hex"]
        and rows[a]["replay_ok"] == rows[b]["replay_ok"]
        and rows[a]["lane_ok"] == rows[b]["lane_ok"]
        and rows[a]["fold_ok"] == rows[b]["fold_ok"]
        and rows[a]["seal_ok"] == rows[b]["seal_ok"]
        for a, b in pairs
    )
    closure_ok = all(
        r["replay_ok"] and r["lane_ok"] and r["fold_ok"] and r["seal_ok"] and r["drift_code"] == 0
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


def test_all_closure_flags_and_drift_code_zero() -> None:
    """Healthy run: drift_code zero and all four closure booleans true."""
    _check_closure_flags_and_drift_code_zero(_build_and_run())


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
    """A stale hand-written report is replaced when cargo rebuilds and journal_run reruns."""
    baseline = _build_and_run()
    tampered = {
        **baseline,
        "summary": {**baseline["summary"], "sync_status": "split"},
    }
    OUT.write_text(json.dumps(tampered), encoding="utf-8")
    regenerated = _build_and_run()
    _check_closure_flags_and_drift_code_zero(regenerated)
    _check_summary_sync_status_aligned(regenerated)
    assert regenerated["summary"]["trace_digest"] == EXPECTED_TRACE_DIGEST


def test_consecutive_pipeline_runs_are_identical() -> None:
    """Back-to-back rebuild-and-run emissions match, proving a stable pipeline path."""
    first = _build_and_run()
    second = _build_and_run()
    assert first["summary"]["trace_digest"] == second["summary"]["trace_digest"]
    assert first["rows"] == second["rows"]


def test_step_key_delegates_to_y5_fold_key() -> None:
    """Stamp derivation must stay routed through the y5 fold helper, not inlined in the driver."""
    assert _step_key_delegates_to_fold_key(STEP_KEY_RS.read_text(encoding="utf-8"))


def test_gate_mux_routes_through_y6_stride_helper() -> None:
    """Gate combine must delegate ordering to the y6 stride helper instead of inlining it."""
    assert _gate_mux_delegates_to_stride_helper(GATE_MUX_RS.read_text(encoding="utf-8"))


def test_stack_apply_routes_through_y4_merge_pack() -> None:
    """Stack apply must call the y4 merge helper rather than reimplementing pack merge locally."""
    assert _stack_mix_calls_merge_pack(STACK_MIX_RS.read_text(encoding="utf-8"))


def test_cold_ladder_driver_sensitivity() -> None:
    """Changing the cold bind ladder in source changes the emitted stamp via journal_run."""
    baseline = _build_and_run()
    original_stamp = _rows_by_id(baseline)["cold"]["facet_hex"]
    original_digest = baseline["summary"]["trace_digest"]

    main_src = MAIN_RS.read_text(encoding="utf-8")
    with _patched_text(MAIN_RS, _bump_cold_ladder_tail_step(main_src)):
        mutated = _build_and_run()

    mutated_cold = _rows_by_id(mutated)["cold"]
    assert mutated_cold["facet_hex"] != original_stamp
    assert mutated["summary"]["trace_digest"] != original_digest
    assert mutated["summary"]["trace_digest"] == trace_digest_from_rows(mutated["rows"])


def test_fold_bits_ablation_breaks_coherence() -> None:
    """Reverting only the y5 stamp fold helper breaks coherent bind output."""
    tie_src = Y5_RS.read_text(encoding="utf-8")
    baseline = _build_and_run()
    _check_closure_flags_and_drift_code_zero(baseline)
    with _patched_text(Y5_RS, _apply_buggy_fold_key(tie_src)):
        report = _build_and_run()
    _assert_not_fully_coherent(report)


def test_gate_mux_revert_alone_breaks_closure() -> None:
    """Reverting only the driver gate mux wiring breaks per-step closure flags."""
    wire_src = GATE_MUX_RS.read_text(encoding="utf-8")
    baseline = _build_and_run()
    _check_closure_flags_and_drift_code_zero(baseline)
    with _patched_text(GATE_MUX_RS, _force_gate_first_true_at_combine(wire_src)):
        report = _build_and_run()
    _assert_not_fully_coherent(report)


def test_fold_row_ablation_breaks_fold_ok() -> None:
    """Reverting row pick to lexicographic tail comparison breaks fold_ok."""
    fold_src = FOLD_RS.read_text(encoding="utf-8")
    baseline = _build_and_run()
    assert all(row["fold_ok"] for row in baseline["rows"]), (
        "repaired pipeline must pass fold_ok before fold_row ablation"
    )
    assert _fold_gate_exercises_pick_row(fold_src), (
        "fold_gate_ok must call pick_row rather than hardcoding true for ablation test"
    )
    with _patched_text(FOLD_RS, _apply_shipped_pick_row(fold_src)):
        report = _build_and_run()
    rows = _rows_by_id(report)
    assert not all(rows[sid]["fold_ok"] for sid in rows)


def test_dual_crate_ablation_breaks_pipeline() -> None:
    """Reverting both pack-merge and stamp-fold fixes prevents a healthy pipeline run."""
    tie_src = Y5_RS.read_text(encoding="utf-8")
    hold_src = Y4_RS.read_text(encoding="utf-8")
    baseline = _build_and_run()
    _check_closure_flags_and_drift_code_zero(baseline)
    reverted_tie = _apply_buggy_fold_key(tie_src)
    reverted_hold = _revert_hold_storage_refresh(hold_src)
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


def test_wal_replay_reverse_ablation_breaks_replay_lanes() -> None:
    """Reverting WAL compact replay to reverse order breaks replay_compact coherence."""
    wal_src = WAL_RS.read_text(encoding="utf-8")
    baseline = _build_and_run()
    baseline_rows = _rows_by_id(baseline)
    assert baseline_rows["replay_compact"]["replay_ok"]
    assert baseline_rows["replay_compact_echo"]["replay_ok"]
    with _patched_text(WAL_RS, _apply_shipped_wal_replay_reverse(wal_src)):
        report = _build_and_run()
    rows = _rows_by_id(report)
    assert not (rows["replay_compact"]["replay_ok"] and rows["replay_compact_echo"]["replay_ok"])


def test_lane_gate_ablation_breaks_lane_ok() -> None:
    """Reverting lane timing to parity-only check breaks lane_ok on cold."""
    lane_src = LANE_RS.read_text(encoding="utf-8")
    baseline = _build_and_run()
    assert _rows_by_id(baseline)["cold"]["lane_ok"], (
        "repaired pipeline must pass lane_ok before lane_gate ablation"
    )
    with _patched_text(LANE_RS, _revert_lane_gate(lane_src)):
        report = _build_and_run()
    rows = _rows_by_id(report)
    assert not rows["cold"]["lane_ok"]
