The simulator writes one json object to stdout.

Its fields are `final_energy`, `energy_drift`, `max_drift`, `is_resonance_locked`, and `steps_completed`.

The first three are floating-point values.

`is_resonance_locked` is boolean and `steps_completed` is an integer.

The verifier rebuilds with `make -C /app/environment rebuild`.

It then runs the binary with these argument triples.

`10.0 0.001 false`
`10.0 0.001 true`
`30.0 0.0005 false`
`15.0 0.0008 false`
`5.0 0.001 false`
`10.0 0.05 false`
`10.0 0.05 true`

For the long runs, `energy_drift` stays below `1.0e-6` and `max_drift` stays below `1.0e-4`.

The adaptive fine-step run also reports more than one thousand completed steps.

The `15.0 0.0008 false` run keeps `final_energy` between negative two and zero.

The `5.0 0.001 false` close pass stays finite, keeps the same tight drift bounds, and finishes with a small negative `final_energy`.

That behavior depends on `epsilon_sq` staying as a strictly positive softening term in both the force path and the total-energy path.

Resonance lock is derived from the resonance-angle series over fifty-sample windows with a stride of ten.

Each window uses its own local mean, wraps deviations back into `[-pi, pi]`, measures the window spread, and averages those spreads across the sampled windows.

`is_resonance_locked` is true when that averaged spread stays below `1.0`.

The fine-step `10.0 0.001 false` run reports locked.

The coarse-step `10.0 0.05 false` run reports unlocked.

The adaptive coarse-base-step `10.0 0.05 true` run recovers the locked classification while still keeping small drift.

Writes under `/opt/verifier` are also expected to fail at runtime.
