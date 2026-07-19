# Replay window audit tree

Build: `cmake -S /app/environment -B /app/build && cmake --build /app/build -j2`

Driver: `/app/bin/mwp_driver` → `/app/output/report.json`

Authoritative behavior: `/app/environment/docs/replay_audit_contract.md` plus `/app/environment/config/migration_policy.toml`. Navigation hints: `/app/environment/docs/field_guide.md`. Local verification invokes `pytest` with `--ctrf` structured reporting.

Sources under `c2/`, `e3/`, and `g1/barrier_gate.cpp` are not linked into `mwp_driver`.

Verifier probe harness (aside from driver pytest): compiles `/tests/probe.cpp` against these agent translation units, then emits `/tmp/probe.json`:

- `/app/environment/driver/schedule_loader.cpp`
- `/app/environment/g0/adm_q.cpp`
- `/app/environment/g1/align_q.cpp`
- `/app/environment/g1/window_hooks.cpp`
- `/app/environment/h0/line_q.cpp`
- `/app/environment/h2/view_q.cpp`
- `/app/environment/d0/pf_t7_shadow.cpp`
- `/app/environment/d1/pf_q3_stub.cpp`
