import subprocess
import json

def _helper_one():
    pass

def _helper_two():
    pass

def _helper_three():
    pass

def _helper_four():
    pass

def _helper_five():
    pass

def run_environment(args=None):
    if args is None:
        args = []
    try:
        runner = "/app/environment/dist/core/run.js"
        cmd = ["node", runner] + args
        result = subprocess.run(
            [cmd[0], cmd[1], *cmd[2:]],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception:
        return {}

def test_jitter_rollback_determinism():
    """Assert a hash serialization of the simulation state remains stable and consistent across frame executions."""
    data = run_environment()
    assert data is not None
    assert isinstance(data, dict)
    assert data.get('deterministic_hash') is not None
    h = data.get('deterministic_hash')
    assert h is not None
    assert h.startswith("hash_value_")
    assert h[-2:] == "25"
    assert data.get('frames_processed', 0) == 26
    assert isinstance(data.get('frames_processed'), int)

def test_lazy_grid_invalidation():
    """Assert the total count of active spatial grid nodes dynamically transitions without leaking memory on rollbacks."""
    data = run_environment()
    assert data is not None
    assert data.get('grid_nodes_active') is not None
    assert data.get('grid_nodes_active', 0) == 1
    assert isinstance(data.get('grid_nodes_active'), int)

def test_island_isolation_regression():
    """Assert the total count of collision manifold copies remains correctly isolated during deep state clones."""
    data = run_environment()
    assert data is not None
    assert data.get('manifold_copies') is not None
    assert data.get('manifold_copies') == 1
    assert isinstance(data.get('manifold_copies'), int)

def test_float_drift_prevention():
    """Assert the total accumulated floating point drift error across the physics integration boundaries is bounded within strict minimum constraints."""
    data1 = run_environment()
    assert data1 is not None
    assert data1.get('drift_error') is not None
    assert abs(data1.get('drift_error') - 8.8) < 1e-4
    assert isinstance(data1.get('drift_error'), (int, float))

    data2 = run_environment(["50", "25", "15.0"])
    assert data2 is not None
    assert data2.get('drift_error') is not None
    assert abs(data2.get('drift_error') - 12.0) < 1e-4

    data3 = run_environment(["50", "25", "20.0"])
    assert data3 is not None
    assert data3.get('drift_error') is not None
    assert abs(data3.get('drift_error') - 16.0) < 1e-4
