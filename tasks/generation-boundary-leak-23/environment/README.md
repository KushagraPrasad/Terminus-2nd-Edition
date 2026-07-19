Generator runtime contract
==========================

See `/app/environment/docs/generator_contract.md` for the stamp, seam, carry,
and digest rules. Scenario JSON records use integer `t_left`, `t_right`,
`buf_len`, `epoch_tag`, `epoch`, and `carry_seed` inputs documented in
`config/runtime.toml`. Stage one emits `merged` byte values plus integer `seam0`
and `seam1` fields; stage two emits `carry` bytes.

Rebuild with `cmake -S /app/environment -B /app/build` followed by
`cmake --build /app/build -j 2`. The Python harness under
`/app/environment/harness/` can run the pipeline for local smoke checks.
