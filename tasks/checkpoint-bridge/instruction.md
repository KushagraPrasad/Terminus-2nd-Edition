# Checkpoint bridge drift

You maintain an incremental rebuild bridge that synchronizes checkpointed artifact trees with durable ledger metadata inside a single-container coordinator. Regenerate `/app/output/rebuild_report.json` (top-level `runs`) by running the normal coordinator entrypoint (`/app/bin/cycle_run`) across its restart/rollback scenarios; the verifier reconfigures and rebuilds from `/app/environment` before running scenarios.

Intermediate health summaries must not be treated as final proof: generation counters, tombstone maps, and cross-format span digests must agree across a single process restart boundary and through rollback phases documented in `/app/environment/docs/field_guide.md`. You must repair C++ source files under `/app/environment` so the pipeline regenerates the report; static/manual JSON writes are insufficient, and module-level behavior must match the same contract as the CLI. View fixtures live under `/app/environment/fixtures/`.
