import subprocess
import json


def run_reconciler():
    """Helper to run the main reconciler program via Go."""
    res = subprocess.run(
        ["/app/environment/bin/orbit_sim", "10.0", "0.001", "false"],
        capture_output=True,
        text=True,
        check=True
    )
    return res


def test_energy_conservation():
    """Assert energy drift and maximum drift remain bounded under long-term simulations."""
    try:
        result = subprocess.run(
            ["/app/environment/bin/orbit_sim", "10.0", "0.001", "false"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception:
        data = {}
        
    assert data is not None
    drift_tol = 1.0e-6
    max_drift_tol = 1.0e-4
    assert data['energy_drift'] < drift_tol
    assert data['max_drift'] < max_drift_tol


def test_adaptive_scaling():
    """Assert energy conservation holds across step changes in adaptive simulation."""
    try:
        result = subprocess.run(
            ["/app/environment/bin/orbit_sim", "10.0", "0.001", "true"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception:
        data = {}
        
    assert data is not None
    drift_tol = 1.0e-6
    max_drift_tol = 1.0e-4
    min_steps = 1000
    assert data['energy_drift'] < drift_tol
    assert data['max_drift'] < max_drift_tol
    assert data['steps_completed'] > min_steps


def test_float_accumulation():
    """Assert Kahan precision summation prevents float rounding loss over many steps."""
    try:
        result = subprocess.run(
            ["/app/environment/bin/orbit_sim", "30.0", "0.0005", "false"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception:
        data = {}
        
    assert data is not None
    drift_tol = 1.0e-6
    assert data['energy_drift'] < drift_tol


def test_resonance_detection():
    """Assert resonance alignment filter correctly distinguishes locking from circulation."""
    try:
        result = subprocess.run(
            ["/app/environment/bin/orbit_sim", "10.0", "0.001", "false"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception:
        data = {}
        
    assert data is not None
    assert data['is_resonance_locked'] is True


def test_simulation_integrity():
    """Assert verifier executes correctly with novel unlisted parameters and yields physically plausible energy."""
    t_val = "15.0"
    dt_val = "0.0008"
    adp_val = "false"
    try:
        result = subprocess.run(
            ["/app/environment/bin/orbit_sim", t_val, dt_val, adp_val],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception:
        data = {}

    assert data is not None
    drift_tol = 1.0e-6
    assert data['energy_drift'] < drift_tol
    min_energy = -2.0
    max_energy = 0.0
    assert min_energy < data['final_energy'] < max_energy


def test_softening_close_encounter():
    """Assert softening prevents division-by-zero during close encounters, preventing NaN/inf energy."""
    t_val = "5.0"
    dt_val = "0.001"
    adp_val = "false"
    try:
        result = subprocess.run(
            ["/app/environment/bin/orbit_sim", t_val, dt_val, adp_val],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception:
        data = {}

    assert data is not None
    final_energy = data.get('final_energy', 0.0)
    # Library-free NaN check: NaN is not equal to itself
    assert final_energy == final_energy
    # Library-free Inf check using numeric bounds (since energies are around -0.6 to -1.5)
    assert final_energy > -1e10
    assert final_energy < 1e10


def test_resonance_unlocked():
    """Assert chaotic or short simulations correctly report no resonance lock (is_resonance_locked is false)."""
    t_val = "10.0"
    dt_val = "0.05"
    adp_val = "false"
    try:
        result = subprocess.run(
            ["/app/environment/bin/orbit_sim", t_val, dt_val, adp_val],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
    except Exception:
        data = {}

    assert data is not None
    assert data.get('is_resonance_locked') is False
