# Recovery transcript contract

This document defines externally tested fields for `/app/output/recovery_transcript.json`.

## Command

The harness regenerates output with:

    python3 /app/environment/runner.py --write /app/output/recovery_transcript.json

## Top-level JSON

- `runs`: array of run objects.
- Each run has:
  - `run_id` (string): stable identifier `run-1` for the bundled scenario.
  - `phase` (string): phase label from `studio/app/data/schedule.json`. The bundled schedule lists `alpha` first, then `beta`.
  - `steps` (array of strings): exactly two labels for that phase, `collect-<phase>` followed by `merge-<phase>`.
  - `entries` (array of objects): one object per artifact slot in phase order.

## Bundled artifacts

`studio/app/data/digest_sources.json` defines `slot-a`, `slot-b`, `slot-c`, and `slot-d`. Phase `alpha` emits `slot-a` and `slot-b` in order; later phases use the remaining slots per the schedule.

Journal/replay helpers accept staging dicts that include a `rows` array of per-artifact records.

## Entry object fields

Each entry includes:

- `artifact` (string): slot name from fixtures (for example `slot-a`, `slot-b`).
- `digest_line` (string): 64 lowercase hex characters (32 bytes of payload material).
- `anchor_head` (string): first 8 lowercase hex characters of `digest_line`.
- `merge_lane` (integer): present for entries whose phase has `"cleanup": true` in the schedule. Formula: `merge_lane = bias + slot_index * 3` where `bias` is the integer `bias` field in `studio/app/data/cleanup_spans.json`, and `slot_index` is the integer map value for that entry's `artifact` in the same file's `slot_index` object.
- `tail_seq` (integer): strictly increases by **exactly 1** for each successive entry in **global** transcript order (first entry is `1`, second is `2`, and so on across all phases).
- `tail_gen` (integer): generation number for the entry's artifact from `studio/app/data/promotion_tails.json` under `tails`.
- `span_head` (string): first 12 lowercase hex characters of the span digest described below.

## Digest rule

For each entry, `digest_line` MUST equal the lowercase hex output of `hashlib.sha256(...).hexdigest()` applied to the raw bytes obtained by `bytes.fromhex(...)` on that artifact's `byte_hex` field inside `studio/app/data/digest_sources.json` under `artifacts` → artifact name → `byte_hex` (even-length hex string).

## Anchor rule

`anchor_head` MUST equal the first eight characters of that entry's `digest_line`.

## Replay span rule

For each entry, `span_head` MUST equal the first 12 lowercase hex characters of `hashlib.sha256(...).hexdigest()` applied to the UTF-8 text:

    <phase>:<artifact>:<tail_gen>:<tail_seq>:<digest_line>

The values are taken from the emitted entry and the containing run's `phase` after global tail ordering has been assigned.

## Module-level probes

Direct library checks may synthesize probe payloads with 16 repeated byte pairs (`00aa` repeated 16 times) or 28 trailing filler hex digits after an 8-character anchor prefix such as `abcd1234` when validating digest and anchor helpers outside the full transcript.

The replay binder `n_bind_w` in `journal_apply/last_apply.py` must compute and attach `merge_lane`, monotonic `tail_seq`, and `span_head` on every row dict it returns, using the formulas in this document. Orchestrator layers must not be the only place those fields are stamped if callers import `n_bind_w` directly.

Digest and anchor helpers (`n_quench_u` on the wal_slots ingest path, `n_stitch_v` in `co_emitters/mid_slice.py`) are probed the same way when validated outside the full transcript run.

## Idempotence

Running the command twice with the same fixtures must produce byte-identical JSON at the output path (tests compare raw file text).
