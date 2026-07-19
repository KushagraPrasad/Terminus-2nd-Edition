# Deterministic Physics Rollback and State Synchronization

You are debugging a 2D prediction game engine that manages client states.

The engine uses three major subsystems that must remain perfectly consistent across updates and rollbacks.

The simulation is failing deterministic checks under heavy frame rollback sequences.

The client prediction engine expects that rollbacks to previous states are absolutely seamless and do not introduce errors or leaks.

If any part of the state retains references to future or mutated objects, the game state diverges.

This is especially critical for the frame caching storage.

It is also critical for the spatial indexing grid.

It is also critical for the collision detection manifold.

Your task is to fix the source code in the `/app/environment` directory. You must fix the implementation across the subsystems to ensure absolute determinism. Output-only changes or hardcoding outputs in run.ts is not allowed; the source files under the subsystems must be corrected.

To verify your changes, the verifier will run the test pipeline using `npm test`.

Ensure all game states remain perfectly isolated from previous frames.

Ensure this behavior holds across high jitter delays.

Coordinate manifolds must not leak references.

Float accumulation must be strictly bounded.

## Observable Semantics

The output will be printed to stdout.

The test suite will execute `node /app/environment/dist/core/run.js` via the `runner = "/app/environment/dist/core/run.js"` path to assert the hash.

Specifically, the output JSON must accurately report the following semantics.

The `deterministic_hash` field represents a hash serialization of the simulation state.

It must remain stable and consistent across frame executions. Verifies the hash is correct. The output must be formatted with the prefix `hash_value_` followed by the frame ID.

The `frames_processed` field is the count of time steps processed.

The `grid_nodes_active` field is the total active cell count.

It must dynamically transition and not leak memory on rollbacks.

The `manifold_copies` field is the number of active manifolds.

It must remain correctly isolated during deep state clones and must not leak any references.

The `drift_error` field tracks precision drift across steps.

## Architectural Notes

The architecture of the physics pipeline is divided into separate modules.

These modules decouple frame caching.

They decouple spatial indexing.

They decouple collision detection.

They decouple core integration.

All these systems must work in tandem.

They must avoid reference leaks.

They must avoid precision accumulation.

This prevents coordinate drifts over time.
