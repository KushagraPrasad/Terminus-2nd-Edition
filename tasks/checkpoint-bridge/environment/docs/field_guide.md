# Field guide

## Command

`/app/environment/exec/run_cycle.sh` rebuilds `/app/output/rebuild_report.json` via the `cycle_run` binary.

Build steps (also used by the verifier before scenarios):

1. `cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release`
2. `cmake --build /app/build -j2`
3. Install `cycle_run` to `/app/bin/cycle_run`

Harness-only flags such as `--ctrf` belong to pytest, not `cycle_run`.

Flags:

- `--scenario <name>` — one of `alpha`, `beta`, `idempo`, `digest`, `overlap`, `fork`
- `--out <path>` — output JSON path (default `/app/output/rebuild_report.json`)
- `--inject-restart` — simulate a single process restart between wave 1 and wave 2
- `--pair-order <0|1>` — phase ordering for paired scenarios
- `--fork-branch <0|1>` — view branch selector for fork scenarios

## Top-level schema

```json
{
  "runs": [
    {
      "run_id": "...",
      "restart_seen": false,
      "waves": [
        {"wave_id": "w0", "health_status": "ok", "gen_marker": 2, "seal_slot": 3}
      ],
      "span_records": [
        {"wave_id": "w0", "kit_id": "kit-alpha", "tag_hex": "abcd...", "source_lane": "secondary", "gen_marker": 2}
      ]
    }
  ]
}
```

## Span tag rule

`tag_hex` is the first 16 hex characters of SHA-256 (`sha256` hexdigest) over:

`authoritative_body + "|" + kit_id + "|" + gen_marker`

Use the bytes from the authoritative lane selected for that wave (`primary_body`, `secondary_body`, or `slice_body`). The reference derivation in `environment/tooling/seq_tool.py` uses Python `hashlib` with the same rule.

Kit-alpha view bodies for verifier scenarios: `primary_body` = `primary-alpha-bytes`, `secondary_body` = `secondary-alpha-bytes`, `slice_body` = `slice-alpha-bytes`, `view_id` = `kit-alpha`.

## Generation markers

Waves use `wave_id` labels `w0`, `w1`, and `w2` (fork scenarios use `w0` and `w1` only). When `--inject-restart` is used, `restart_seen` in the run record must be true (boolean true, not false). After `--inject-restart`, generation markers for waves following the restart boundary must advance relative to the pre-restart wave (`w2.gen_marker` > `w1.gen_marker` for the three-wave restart scenario). Seal slots track `gen_marker + phase_index`.

Scenario `beta` with `--pair-order 0` vs `--pair-order 1` must yield matching final span tags: `spans_a[-1]["tag_hex"] == spans_b[-1]["tag_hex"]` on the paired runs' last `span_records` rows.

## Authority lanes

Three view bodies exist: `primary_body`, `secondary_body`, `slice_body`. The active lane for span material must match the reconciled surface for that scenario phase.

## Regen markers

Verifier scenarios may compare a `regen_fingerprint` derived from sorted `tag_hex` values across all span records in a run.
