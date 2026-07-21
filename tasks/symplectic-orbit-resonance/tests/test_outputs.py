def _axis_fingerprint_anchor():
    return "/app/environment/bin/orbit_sim"


import json
import subprocess
from pathlib import Path

import pytest


ENV_ROOT = Path("/app/environment")
BIN_PATH = Path("/app/environment/bin/orbit_sim")
FINAL_ENERGY_KEY = "final" + "_" + "energy"
ENERGY_DRIFT_KEY = "energy" + "_" + "drift"
MAX_DRIFT_KEY = "max" + "_" + "drift"
LOCKED_KEY = "is" + "_" + "resonance" + "_" + "locked"
STEPS_KEY = "steps" + "_" + "completed"
FORBIDDEN_MARKERS = (
    "/tests",
    "test_outputs.py",
    "/opt/verifier",
    "reward.txt",
    "ctrf.json",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _source_path(directory: str, stem: str, suffix: str = ".cpp") -> Path:
    return ENV_ROOT / directory / (stem + suffix)


def _assert_no_test_leaks(text: str, path: Path) -> None:
    for marker in FORBIDDEN_MARKERS:
        assert marker not in text, f"{path} should not reference verifier internals: {marker}"


@pytest.fixture(scope="session", autouse=True)
def build_binary():
    """Rebuild the simulator once per test session and reject verifier-aware payloads."""
    source_files = [
        *ENV_ROOT.rglob("*.cpp"),
        *ENV_ROOT.rglob("*.h"),
        ENV_ROOT / "Makefile",
    ]
    for path in source_files:
        _assert_no_test_leaks(_read_text(path), path)

    subprocess.run(["make", "-C", "/app/environment", "rebuild"], check=True)

    assert BIN_PATH.exists(), "expected rebuilt orbit_sim binary to exist"
    assert BIN_PATH.is_file(), "expected orbit_sim path to be a file"
    with BIN_PATH.open("rb") as handle:
        assert handle.read(4) == b"\x7fELF", "orbit_sim must be a compiled ELF binary"

    binary_bytes = BIN_PATH.read_bytes()
    for marker in FORBIDDEN_MARKERS:
        assert marker.encode() not in binary_bytes, f"binary should not embed verifier marker {marker}"

    return BIN_PATH


def run_orbit_sim(total_time: str, dt: str, adaptive: str) -> tuple[subprocess.CompletedProcess[str], dict]:
    result = subprocess.run(
        ["/app/environment/bin/orbit_sim", total_time, dt, adaptive],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    return result, payload


def test_runtime_is_hardened(build_binary):
    """Verify the verifier runs as an unprivileged user and cannot rewrite verifier tooling."""
    with pytest.raises(PermissionError):
        with (Path("/opt/verifier") / str(0)).open("w", encoding="utf-8"):
            pass


def test_output_schema_and_types(build_binary):
    """Verify the simulator prints only the documented JSON object on stdout."""
    result, data = run_orbit_sim("10.0", "0.001", "false")

    assert result.stderr == ""
    assert set(data) == {
        FINAL_ENERGY_KEY,
        ENERGY_DRIFT_KEY,
        MAX_DRIFT_KEY,
        LOCKED_KEY,
        STEPS_KEY,
    }
    assert isinstance(data[FINAL_ENERGY_KEY], (int, float))
    assert isinstance(data[ENERGY_DRIFT_KEY], (int, float))
    assert isinstance(data[MAX_DRIFT_KEY], (int, float))
    assert isinstance(data[LOCKED_KEY], bool)
    assert isinstance(data[STEPS_KEY], int)


def test_energy_conservation(build_binary):
    """Verify the fine-step non-adaptive run keeps energy drift within the documented bounds."""
    _, data = run_orbit_sim("10.0", "0.001", "false")

    assert data[ENERGY_DRIFT_KEY] < 1.0e-6
    assert data[MAX_DRIFT_KEY] < 1.0e-4


def test_adaptive_scaling(build_binary):
    """Verify adaptive scaling preserves the same drift bounds while still executing many steps."""
    _, data = run_orbit_sim("10.0", "0.001", "true")

    assert data[ENERGY_DRIFT_KEY] < 1.0e-6
    assert data[MAX_DRIFT_KEY] < 1.0e-4
    assert data[STEPS_KEY] > 1000


def test_float_accumulation(build_binary):
    """Verify the long-horizon run keeps drift small enough to require compensated accumulation."""
    _, data = run_orbit_sim("30.0", "0.0005", "false")

    assert data[ENERGY_DRIFT_KEY] < 1.0e-6


def test_resonance_detection_locked(build_binary):
    """Verify the fine-step resonance case is classified as locked."""
    _, data = run_orbit_sim("10.0", "0.001", "false")
    assert data[LOCKED_KEY] is True


def test_novel_parameters_energy_band(build_binary):
    """Verify the documented 15.0 0.0008 false run stays stable and keeps final_energy in the stated range."""
    _, data = run_orbit_sim("15.0", "0.0008", "false")

    assert data[ENERGY_DRIFT_KEY] < 1.0e-6
    assert -2.0 < data[FINAL_ENERGY_KEY] < 0.0


def test_softening_close_encounter_runtime(build_binary):
    """Verify the close-encounter run stays stable enough to require real softening and accumulation."""
    _, data = run_orbit_sim("5.0", "0.001", "false")

    assert data[FINAL_ENERGY_KEY] == data[FINAL_ENERGY_KEY]
    assert data[ENERGY_DRIFT_KEY] == data[ENERGY_DRIFT_KEY]
    assert data[MAX_DRIFT_KEY] == data[MAX_DRIFT_KEY]
    assert abs(data[FINAL_ENERGY_KEY]) < float("inf")
    assert abs(data[ENERGY_DRIFT_KEY]) < float("inf")
    assert abs(data[MAX_DRIFT_KEY]) < float("inf")
    assert data[ENERGY_DRIFT_KEY] < 1.0e-6
    assert data[MAX_DRIFT_KEY] < 1.0e-4
    assert -0.01 < data[FINAL_ENERGY_KEY] < 0.0
    assert data[LOCKED_KEY] is True


def test_resonance_unlocked_with_coarse_dt(build_binary):
    """Verify the coarse-step resonance case is classified as unlocked."""
    _, data = run_orbit_sim("10.0", "0.05", "false")
    assert data[LOCKED_KEY] is False


def test_adaptive_coarse_dt_recovers_locked_state(build_binary):
    """Verify adaptive stepping can relock the same coarse base step that circulates without adaptation."""
    _, data = run_orbit_sim("10.0", "0.05", "true")

    assert data[LOCKED_KEY] is True
    assert data[ENERGY_DRIFT_KEY] < 1.0e-4
    assert data[MAX_DRIFT_KEY] < 1.0e-3
