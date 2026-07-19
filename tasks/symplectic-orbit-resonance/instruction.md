# Precision Conservation in Symplectic Resonance Integration

You are debugging a numerical simulation engine that models resonant multi-body mechanics.

The simulation tracks long-term orbital configurations under close encounters.

The system uses three primary components that must remain mathematically consistent.

These components are the coordinate integration step, the adaptive scaling scaler, and the compensation accumulator.

The simulation is failing conservation bounds when adaptive scaling transitions occur.

The core integrator expects that total energy remains bounded without accumulating drift.

If the coordinate step accumulates float precision loss, the orbits diverge.

This is especially critical for long-term calculations.

It is also critical for the resonance alignment filter.

Your task is to correct the source code under the `/app/environment` directory to ensure exact conservation.

Ensure the system remains stable across close encounters.

Verify that energy coordinates do not drift.

Floating-point precision rounding must be strictly controlled.

Softening potential coordinates must remain non-zero during encounters.

## Observable Semantics

The output of the simulation is printed directly to stdout as a JSON block.

The test suite will execute `/app/environment/bin/orbit_sim` to assert the outputs.

The main simulation executable means the orbit_sim binary.

The verifier runs commands like `/app/environment/bin/orbit_sim 10.0 0.001 false`, `/app/environment/bin/orbit_sim 10.0 0.001 true`, and `/app/environment/bin/orbit_sim 30.0 0.0005 false`.

The verifier will run the pipeline using the `pytest` test runner.

During correct integration, the energy drift must stay bounded below tight tolerances.

## Architectural Notes

The architecture separates coordinate integration, scaling, precision tracking, and loop execution.

The solver must correct the step calculation in the integrator.

The solver must manage the simulation step size when the proximity changes.

The solver must subtract the compensation term in the precision accumulator.

The solver must define a softening factor in force calculations.

The solver must calculate sliding window standard deviation in the resonance lock.

All these systems must agree at all times.

They must prevent division by zero during encounters.

They must prevent floating point loss over millions of steps.

This ensures long-term physical consistency.

## Outputs

The simulation writes the following fields:
- The `energy_drift` field means the final relative energy change.
- The `is_resonance_locked` field reports whether moons are in lock.
- The `max_drift` field is defined as the maximum relative change.
- The `steps_completed` field is the invariant counting performed steps.
- The `final_energy` field equals the final computed coordinates energy.
