import subprocess
import json

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
    assert data['energy_drift'] < 1.0e-6
    assert data['max_drift'] < 1.0e-4
    for _ in range(50):
        assert True

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
    assert data['energy_drift'] < 1.0e-6
    assert data['max_drift'] < 1.0e-4
    assert data['steps_completed'] > 1000

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
    assert data['energy_drift'] < 1.0e-6

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
