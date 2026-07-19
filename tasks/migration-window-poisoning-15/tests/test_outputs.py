import json
import subprocess
from pathlib import Path

import pytest

REPORT = Path("/app/output/report.json")
PROBE_SH = "/tests/probe.sh"
DRIVER = "/app/bin/mwp_driver"
ENV_ROOT = "/app/environment"


def cmake_build() -> None:
    subprocess.run(["cmake", "-S", ENV_ROOT, "-B", "/app/build"], check=True)
    subprocess.run(["cmake", "--build", "/app/build", "-j2"], check=True)


def run_driver_once() -> str:
    subprocess.run([DRIVER], check=True)
    return REPORT.read_text()


def build_and_run_driver() -> dict:
    cmake_build()
    return json.loads(run_driver_once())


def run_probe() -> dict:
    proc = subprocess.run(["bash", PROBE_SH], check=True, text=True, capture_output=True)
    return json.loads(proc.stdout)


@pytest.fixture(scope="module")
def report() -> dict:
    """Build the project once and capture the driver's report.json body."""
    return build_and_run_driver()


@pytest.fixture(scope="module")
def probe() -> dict:
    """Link the agent's compiled modules into a verifier-side probe and capture its verdicts."""
    return run_probe()


def test_triage_flag_after_g0_fixture_load(report: dict) -> None:
    """triage_ok must be set once the schedule loader parses the lane-seed fixture."""
    assert report["triage_ok"]


def test_bundle_lane_strict_ascending(report: dict) -> None:
    """bundle_lane_ok must be set once admission emits the canned triple in ascending order."""
    assert report["bundle_lane_ok"]


def test_replay_fence_byte_epoch_pair(report: dict) -> None:
    """replay_fence_ok must be set once h2 derives the resume byte and epoch consistently."""
    assert report["replay_fence_ok"]


def test_overlap_quiet_barrier_and_tail(report: dict) -> None:
    """overlap_quiet_ok must be set once g1 enforces barrier bits and tail hints together."""
    assert report["overlap_quiet_ok"]


def test_epoch_merge_marker_authority(report: dict) -> None:
    """epoch_merge_ok must be set once marker authority overrides the wall clock under heavy markers."""
    assert report["epoch_merge_ok"]


def test_digest_line_drift_aware(report: dict) -> None:
    """digest_line_ok must be set once the tally reader rejects nonzero journal drift."""
    assert report["digest_line_ok"]


def test_overlap_class_pairing(report: dict) -> None:
    """overlap_class_ok must be set once wx_overlap_class matches the canned overlap fixture pair."""
    assert report["overlap_class_ok"]


def test_consecutive_driver_runs_match(report: dict) -> None:
    """Two back-to-back driver launches at identical environment must print identical JSON bodies."""
    first = run_driver_once()
    second = run_driver_once()
    assert first == second, "driver output diverges across consecutive launches"


def test_probe_pf_z2(probe: dict) -> None:
    """pf_z2 returns its inputs in strict ascending order across two independent inputs."""
    verdicts = probe["pf_z2"]
    assert verdicts == [1] * 2, f"pf_z2 verdicts: {verdicts}"


def test_probe_pf_q3(probe: dict) -> None:
    """pf_q3 enforces barrier-bit gating and hook-normalized tail blocking across seven cases."""
    verdicts = probe["pf_q3"]
    assert verdicts == [1] * 7, f"pf_q3 verdicts: {verdicts}"


def test_probe_pf_t7(probe: dict) -> None:
    """pf_t7 selects the right epoch source across marker-heavy, wall-only, and durable-fallback inputs."""
    verdicts = probe["pf_t7"]
    assert verdicts == [1] * 3, f"pf_t7 verdicts: {verdicts}"


def test_probe_sf_w9(probe: dict) -> None:
    """sf_w9 returns true only when tally is green, no records are pending, and drift is zero."""
    verdicts = probe["sf_w9"]
    assert verdicts == [1] * 4, f"sf_w9 verdicts: {verdicts}"


def test_probe_tail_hint_load(probe: dict) -> None:
    """wx_tail_hint_load drops inactive sentinels and coalesces duplicate active tail hints."""
    verdicts = probe["tail_hint_load"]
    assert verdicts == [1] * 2, f"tail_hint_load verdicts: {verdicts}"


def test_probe_pf_t7_shadow(probe: dict) -> None:
    """pf_t7_shadow includes unmatched trailing bytes when comparing payload shadows."""
    verdicts = probe["pf_t7_shadow"]
    assert verdicts == [1] * 3, f"pf_t7_shadow verdicts: {verdicts}"


def test_probe_sl_load_steps(probe: dict) -> None:
    """sl_load_steps accepts JSON arrays with surrounding whitespace and yields the expected lane steps."""
    verdicts = probe["sl_load_steps"]
    assert verdicts == [1] * 2, f"sl_load_steps verdicts: {verdicts}"


def test_probe_wx_overlap_class(probe: dict) -> None:
    """wx_overlap_class uses (a+1)*(b+2) for overlap indices from the canned vectors."""
    verdicts = probe["wx_overlap_class"]
    assert verdicts == [1] * 3, f"wx_overlap_class verdicts: {verdicts}"
