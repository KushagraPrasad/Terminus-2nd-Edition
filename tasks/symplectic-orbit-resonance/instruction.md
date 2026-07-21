Repair the C++ orbital simulator under `/app/environment` so the rebuilt `/app/environment/bin/orbit_sim` behaves like a stable resonant model again.

The verifier rebuilds from source with `make -C /app/environment rebuild` before it runs the program.

Output-only shortcuts, shell-script stand-ins, and verifier-aware payloads are not valid fixes.

The program should emit one json object on stdout.

Long runs still need to preserve very small drift, including the stdout contract details `energy_drift < 1.0e-6` and `max_drift < 1.0e-4`.

The adaptive coarse-step path also needs to stay stable.

Keep the compiled fix inside the existing integrator, accumulation, adaptive-step, and simulation-loop code instead of bypassing that pipeline.

The runtime is also expected to stay hardened enough that writes under `/opt/verifier` fail.

Public run profiles are documented in `/app/environment/contract_notes.md`.

That note also describes the output fields and the numeric acceptance ranges the repaired binary still has to satisfy.
