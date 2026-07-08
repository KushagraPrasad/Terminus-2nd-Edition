import json
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
REPORT = APP / "output" / "report.json"
SEED_DIR = APP / "data" / "seed"
SEED_WA = SEED_DIR / "window_a.json"
SEED_WB = SEED_DIR / "window_b.json"
SEED_WC = SEED_DIR / "window_c.json"
SEED_EPOCH = SEED_DIR / "epoch_slice.txt"
SEED_ALIAS = SEED_DIR / "alias_stream.txt"

_DEFAULT_EPOCH_ROWS: list[tuple[int, int, int]] = [
    (1, 100, 2),
    (1, 200, 1),
    (2, 300, 2),
    (2, 300, 3),
]

_MASK64 = (1 << 64) - 1
_FNV_OFFSET = 1469598103934665603
_FNV_PRIME = 1099511628211


def run_tool() -> dict:
    subprocess.run(["cmake", "-S", "/app", "-B", "/app/build"], check=True)
    subprocess.run(["cmake", "--build", "/app/build", "-j2"], check=True)
    subprocess.run(["/app/bin/snapshot_matrix"], check=True)
    return json.loads(REPORT.read_text())


@pytest.fixture(scope="module")
def report() -> dict:
    return run_tool()


def _fnv_mix64(values: list[int], turn_id: int = 7) -> int:
    """FNV-1a style mix used by the tool's trace step (uint64_t semantics)."""
    h = _FNV_OFFSET
    for v in values:
        h = (h ^ (v + turn_id)) & _MASK64
        h = (h * _FNV_PRIME) & _MASK64
    return h


def _probe_depth_agreement(before: list[int], after: list[int]) -> bool:
    """Shallow vs deep agreement for depth_mode > 0 (length match then element-wise)."""
    shallow = len(before) == len(after)
    if not shallow:
        deep = False
    else:
        deep = all(b == a for b, a in zip(before, after))
    return shallow == deep


def _parse_epoch_rows(text: str) -> list[tuple[int, int, int]]:
    rows: list[tuple[int, int, int]] = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        rows.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return rows


def _read_alias_stream() -> list[int]:
    return [int(x) for x in SEED_ALIAS.read_text().split()]


def expected_report(
    window_a: list[int] | None = None,
    window_b: list[int] | None = None,
    window_c: list[int] | None = None,
    epoch_rows: list[tuple[int, int, int]] | None = None,
    alias_stream: list[int] | None = None,
) -> dict:
    """Independent expectation model: same tick/epoch scenario, seed windows parameterized."""
    wa = window_a if window_a is not None else [10, 11, 12, 13, 14, 15]
    wb = window_b if window_b is not None else [10, 11, 12, 13, 14, 16]
    wc = window_c if window_c is not None else [2, 4, 6, 8, 10, 12]

    edge_mark = 10
    lane = (10 >= edge_mark) and (10 >= edge_mark) and (2 >= 2)
    commit = (11 >= edge_mark) and (11 >= edge_mark) and (3 >= 2)

    rows = list(epoch_rows) if epoch_rows is not None else list(_DEFAULT_EPOCH_ROWS)
    latest: dict[int, tuple[int, int]] = {}
    for slot, alias, epoch in rows:
        if slot not in latest or epoch > latest[slot][0]:
            latest[slot] = (epoch, alias)
    map_ok = latest[1][1] == 100 and latest[2][1] == 300

    alias_in = alias_stream if alias_stream is not None else _read_alias_stream()
    folded = sorted(alias_in)
    alias_ok = all(folded[i - 1] <= folded[i] for i in range(1, len(folded)))

    h = _fnv_mix64(wc, 7)
    horizon_ok = (len(wc) >= 4) and (h % 2 == 0)

    probe_ok = _probe_depth_agreement(wa, wb)

    return {
        "lane_window_consistency": lane,
        "commit_latch_visibility": commit,
        "map_epoch_roundtrip": map_ok,
        "alias_sort_stability": alias_ok,
        "horizon_anchor_trace": horizon_ok,
        "probe_depth_agreement": probe_ok,
    }


def test_lane_window_consistency(report: dict):
    """Lane window check matches independent expectation for the seeded tick frames."""
    exp = expected_report()
    assert report["lane_window_consistency"] == exp["lane_window_consistency"]


def test_commit_visibility(report: dict):
    """Commit latch check matches independent expectation for the seeded tick frames."""
    exp = expected_report()
    assert report["commit_latch_visibility"] == exp["commit_latch_visibility"]


def test_map_roundtrip(report: dict):
    """Alias map reconstruction preserves canonical slot mapping across epochs."""
    exp = expected_report()
    assert report["map_epoch_roundtrip"] == exp["map_epoch_roundtrip"]


def test_alias_sort_stability(report: dict):
    """Duplicate identity ordering remains deterministic after fold and probe."""
    exp = expected_report()
    assert report["alias_sort_stability"] == exp["alias_sort_stability"]


def test_horizon_mix(report: dict):
    """Horizon anchor trace matches independent expectation for the seeded window."""
    exp = expected_report()
    assert report["horizon_anchor_trace"] == exp["horizon_anchor_trace"]


def test_depth_agreement(report: dict):
    """Deep vs shallow probe agreement matches independent expectation for the seeded pair."""
    exp = expected_report()
    assert report["probe_depth_agreement"] == exp["probe_depth_agreement"]


def test_report_tracks_seed_file_contents():
    """Changing on-disk seed data must change derived checks; static JSON cannot pass both layouts."""
    backups = {
        SEED_WA: SEED_WA.read_text(),
        SEED_WB: SEED_WB.read_text(),
        SEED_WC: SEED_WC.read_text(),
        SEED_EPOCH: SEED_EPOCH.read_text(),
        SEED_ALIAS: SEED_ALIAS.read_text(),
    }
    try:
        # Default A/B unchanged; alternate C flips checksum parity vs shipped seed.
        SEED_WC.write_text("1 0 0 0\n")
        data = run_tool()
        exp = expected_report(window_c=[1, 0, 0, 0])
        assert data["lane_window_consistency"] == exp["lane_window_consistency"]
        assert data["commit_latch_visibility"] == exp["commit_latch_visibility"]
        assert data["map_epoch_roundtrip"] == exp["map_epoch_roundtrip"]
        assert data["alias_sort_stability"] == exp["alias_sort_stability"]
        assert data["horizon_anchor_trace"] == exp["horizon_anchor_trace"]
        assert data["probe_depth_agreement"] == exp["probe_depth_agreement"]
        # Guard: this mutation must flip horizon vs the default seed expectation.
        assert exp["horizon_anchor_trace"] != expected_report()["horizon_anchor_trace"]

        # Alternate alias stream: correct fold (sort) yields true; identity fold yields false.
        alt_alias = [9, 1, 8, 2]
        SEED_ALIAS.write_text(" ".join(str(x) for x in alt_alias) + "\n")
        data_alias = run_tool()
        exp_alias = expected_report(alias_stream=alt_alias)
        assert data_alias["alias_sort_stability"] == exp_alias["alias_sort_stability"]
        assert exp_alias["alias_sort_stability"] is True

        # Restore alias; identical A/B forces probe_depth_agreement to match a true expectation model.
        SEED_ALIAS.write_text(backups[SEED_ALIAS])
        SEED_WC.write_text(backups[SEED_WC])
        identical = [10, 11, 12, 13, 14, 15]
        SEED_WA.write_text(" ".join(str(x) for x in identical) + "\n")
        SEED_WB.write_text(" ".join(str(x) for x in identical) + "\n")
        data_ab = run_tool()
        exp_ab = expected_report(window_a=identical, window_b=identical)
        assert data_ab["probe_depth_agreement"] == exp_ab["probe_depth_agreement"]
        assert data_ab["probe_depth_agreement"] != expected_report()["probe_depth_agreement"]

        # Restore A/B; epoch rows with a higher-epoch alias for slot 1 flip map_epoch_roundtrip.
        SEED_WA.write_text(backups[SEED_WA])
        SEED_WB.write_text(backups[SEED_WB])
        alt_epoch = "1 999 5\n1 200 1\n2 300 2\n2 300 3\n"
        SEED_EPOCH.write_text(alt_epoch)
        data_map = run_tool()
        exp_map = expected_report(epoch_rows=_parse_epoch_rows(alt_epoch))
        assert data_map["map_epoch_roundtrip"] == exp_map["map_epoch_roundtrip"]
        assert exp_map["map_epoch_roundtrip"] != expected_report()["map_epoch_roundtrip"]
    finally:
        for path, text in backups.items():
            path.write_text(text)
