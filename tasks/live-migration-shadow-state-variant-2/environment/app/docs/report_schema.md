# Recovery Report Contract

The runner writes JSON with top-level keys `runs`, `artifacts`, and `fingerprints`.

## Input material

Primary rows load from `/app/environment/app/fixtures/packs.tsv`. Write-log entries load from `/app/environment/app/fixtures/wal.json` and must be applied in ascending `seq` order before per-run processing. Each entry targets rows matching its `run` and `name`:

- `touch` marks the row as touched by the log.
- `bump` sets `generation` and `active` when those fields are present on the entry.
- `tombstone` marks the row removed with span `removed`.

Tombstone marks in `/app/environment/app/fixtures/tombstones.json` under `marks` also remove matching `run`/`name` rows. Removed rows must not appear in emitted records or artifact lists.

## Runs and records

Each run object has `run_id`, `mode`, `steps`, and `records`. Mode labels are `clean`, `replay`, `cleanup`, and `rerun` for the internal run ids `clean`, `later`, `sweep`, and `repeat` respectively.

Each record includes `name`, numeric `generation`, `owner`, `lineage` (prefix from fixture `chain` plus `:` plus `owner`), `boundary`, `artifact`, and `evidence` with `active`, `bundle`, `summary`, and `source`. Boundaries are `local` or `crossed`. Fixture rows whose span is `removed` must not appear in emitted records.

For `boundary` equal to `crossed`, `owner` and `lineage` must reflect the continuing authority named in `evidence.active`, even when `evidence.summary` still matches older bundle text. For `local` rows listed in `/app/environment/app/fixtures/control_sets.json` under its `controls` array, `owner` and `lineage` must stay identical between the `clean` and `repeat` runs.

When multiple fixture rows share the same `run_id` and `name`, only the row with the greatest `generation` may survive into the emitted record for that pair.

After log replay, the `repeat` run row named `yankee` must report generation `2`, owner `owner-y2`, and boundary `local`. Log bumps that set `active` on a row make that active value the row owner even when the boundary is `local`.

## Artifacts

Each artifact entry mirrors an emitted record: matching `run_id`, `name`, `generation`, `owner`, and `lineage`. Artifact `path` values use the `local/` prefix plus the record artifact filename.

## Fingerprints

`fingerprints.stable_digest` is the lowercase hex SHA-256 of UTF-8 text built as follows. Read integer `anchor` from `/app/environment/app/fixtures/ledger_seed.json`. For every emitted record after applying the canonical projection rules below, form one segment:

`run_id|name|generation|owner|lineage|boundary|anchor:<anchor>`

Sort segments lexicographically, join with newline (`\n`), hash with SHA-256, emit hex.

Canonical projection (used both for emission and digest):

1. Start from `/app/environment/app/fixtures/packs.tsv` rows.
2. Apply write-log entries in ascending `seq` order.
3. Apply tombstone marks from `/app/environment/app/fixtures/tombstones.json`.
4. Drop rows with span `removed` or with `removed` flag set.
5. For each `run_id|name`, keep only the row with maximum `generation`.
6. Derive `owner`, `lineage`, `boundary`, and `evidence` from the surviving row using the same rules the product code applies when correct.

`fingerprints.session_span_id` is exactly eight lowercase hex characters: the first eight characters of the lowercase hex SHA-256 of the string `session:<n>` where `n` is a monotonic counter persisted at `/tmp/mig_obs_session.seq` (increment once per successful report write). The stable digest must be identical across consecutive regenerations that produce the same logical records; the session span id must change whenever the counter advances.

Verifier checks may seed a deliberately invalid placeholder report before invoking the driver to prove static files are replaced.

## Command

Regenerate with `/app/environment/mig_exec --write /app/output/migration_observations.json`. Deleting the output first is safe.
