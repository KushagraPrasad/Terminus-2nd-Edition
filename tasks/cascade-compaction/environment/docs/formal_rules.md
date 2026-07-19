# Formal rules

## Driver

Rebuild command pipeline and run:

```bash
cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
cmake --build /app/build -j2
cp /app/build/cc_run /app/bin/cc_run
/app/bin/cc_run --profile <a|b|c|d> --out /app/output/cc_report.json --ledger-dir /app/output/run_logs
```

Clean runs may delete `/app/output/cc_report.json` and `/app/output/run_logs/` before starting. When the report already exists, the driver appends the newly generated run object to the existing top-level `runs` array without rewriting earlier run objects.

Profile `d` combines restart-boundary behavior with conflicting summary surfaces in one run.

## Row key

Each report row contributes a key string:

`{phase}|{gen_stamp}|{sealed_count}`

## Chain fold

Sort the input strings lexicographically, join with `;`, take SHA-256, keep the first 16 lowercase hex characters.

The helper `/app/environment/py/chain_fold.py` implements the same rule for independent recomputation from row keys or anchor parts.

## Manifest chain

Compute chain fold from all row keys in the run. The `manifest_chain_hex` field must equal this value.

## Summary surface

`summary_chain_hex` comes from the bundled summary mux over per-phase cell strings. It may differ from the manifest chain when profiles introduce conflicting surfaces. Successful runs expose `summary_code` as `ok`.

## Session registry

Path: `/app/environment/state/session.registry`

JSON fields:

- `gen_high_water` — highest `gen_stamp` observed across all completed driver invocations in this container session.
- `ledger_anchor_hex` — chained digest anchor across appended ledger records (see Property 6).

After each successful driver invocation, the registry's `ledger_anchor_hex` must equal the `ledger_anchor_hex` field in the ledger object written for that invocation.

After each successful driver invocation, the registry must be updated before the process exits.

## Property 1 — generation monotonicity

After a restart boundary (`restart_seen` true), every post-boundary row must have `gen_stamp` strictly greater than the last pre-boundary row, and `sealed_count` must not decrease across the run.

Formulas:

- Monotone seals: for each index `i > 0`, `rows[i]["sealed_count"] >= rows[i - 1]["sealed_count"]`.
- Restart step: when `restart_seen` is true and `mid = len(rows) // 2`, require `rows[mid]["gen_stamp"] > rows[mid - 1]["gen_stamp"]`. This applies to every restart profile, including profile `d`.
- Last seal versus first: `rows[-1]["sealed_count"] >= rows[0]["sealed_count"]`.

## Property 2 — manifest authority

When `summary_chain_hex` differs from `manifest_chain_hex`, verification must still treat `manifest_chain_hex` as authoritative (derived from row keys, not the summary mux).

## Property 3 — rollback idempotence

For rollback profiles, re-running the driver with the same profile on a clean output tree must yield identical `rows` and `manifest_chain_hex`. Rollback must not zero the replay cursor while `sealed_count` remains below the cursor position.

After a rollback profile completes, the final row's `sealed_count` must be greater than zero. On repeated rollback-profile appends within the same session, the final row `sealed_count` of the latest appended run must not fall below the final row `sealed_count` of an earlier appended run.

## Property 4 — append ledger

Every driver invocation writes one ledger object under `/app/output/run_logs/` for the appended run. Ledger files must not overwrite an earlier invocation, including repeated invocations of the same profile.

Each ledger file is named `run_{run_index:04d}_{profile_id}.json` (for example `run_0000_a.json`, `run_0001_b.json`). Ledger records are discovered by globbing `run_*.json` in sorted lexicographic order.

Each ledger object records the zero-based `run_index`, the `profile_id`, the manifest `fingerprint`, the appended run's `final_sealed_count`, and `ledger_anchor_hex`.

`final_sealed_count` must equal the `sealed_count` of the last row in the corresponding run object within `/app/output/cc_report.json` (matched by zero-based `run_index`).

## Property 5 — session generation floor

Before executing a new run, the stack must load `gen_high_water` from the session registry. Every row in the new run must satisfy `gen_stamp >= gen_high_water` at the time that row is emitted. After the run completes, `gen_high_water` must equal the maximum `gen_stamp` across all rows in all runs completed so far in the session (prior runs plus the new run).

## Property 6 — ledger anchor chain

Let `F` be the manifest fingerprint of the appended run. For run index `0`, `ledger_anchor_hex` must equal `F`. For run index `n > 0`, `ledger_anchor_hex` must equal the chain fold of `[previous_ledger_anchor_hex, F]` where `previous_ledger_anchor_hex` is the anchor stored in the ledger object for run index `n - 1`.

## Cross-artifact equalities

These equalities are part of the public contract:

- Ledger validation: `final_sealed_count == run_rows[-1]["sealed_count"]` for the report run at the same zero-based `run_index`.
- Session registry validation: `session["ledger_anchor_hex"] == logs[-1]["ledger_anchor_hex"]` after each successful invocation.
- Property 3 rollback append validation: `runs[-1]["rows"][-1]["sealed_count"] >= rows[-1]["sealed_count"]`, where `rows` is taken from the first rollback-profile run in the sequence.

## Schemas

- Report rows: `/app/environment/schemas/report_row.schema.json`
- Ledger runs: `/app/environment/schemas/ledger_run.schema.json`
