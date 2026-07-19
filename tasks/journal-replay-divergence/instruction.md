After a journal bounce, the replay audit banner around `/app` no longer matches the counters implied by the bundled ladder vectors and WAL segments. Echo case lanes disagree on closure and facet output while the summary can look mostly fine.

Repair sources under `/app` so the workspace release build and `/app/bin/journal_run` write `/app/output/report.json`. Lane ids are in `/app/docs/case_lane_ids.txt`.

The report has rows and summary. Each row records scenario_id, replay_ok, lane_ok, fold_ok, seal_ok, drift_code, and facet_hex (exactly 16 lowercase hexadecimal digits). The summary records rows_total, sync_status, tier_span, and trace_digest. Mirror pairs are cold with cold_echo, replay_compact with replay_compact_echo, and wal_restart with wal_restart_echo. Coherent runs keep drift_code at 0 on every row, all four closure booleans true, matching facet_hex on each pair, and sync_status reading settled. Incoherent runs break at least one of those conditions. The module comment above `/app/m2/k81/src/main.rs` defines tier_span and trace_digest reduction; read that header instead of hand-writing JSON. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_hints.txt` for cargo and pytest argv details.
