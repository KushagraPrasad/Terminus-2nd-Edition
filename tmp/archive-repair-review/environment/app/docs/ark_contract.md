# Ark observation contract

## Command

`/app/bin/ark_run` writes `/app/output/ark_trace.json`.

Flags:

- `--scenario <name>` — one of `m7`, `n4`, `idempo`, `f2`, `pl_n8`, `fork_x9`
- `--out <path>` — output JSON path (default `/app/output/ark_trace.json`)
- `--inject-restart` — simulate a single process restart between wave 1 and wave 2
- `--pair-order <0|1>` — replay phase ordering for paired scenarios
- `--fork-branch <0|1>` — kit branch selector for fork scenarios

## Verifier rebuild

The verifier configures and builds from `/app/environment` with CMake before executing scenarios:

1. `cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release`
2. `cmake --build /app/build -j2`
3. Install `/app/build/ark_run` to `/app/bin/ark_run`

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
      "principal_transitions": [
        {"actor_id": "svc-reader", "from_wave": "w0", "to_wave": "w1", "outcome": "ok"}
      ],
      "digest_records": [
        {"wave_id": "w0", "kit_id": "kit-alpha", "link_hex": "abcd...", "source_lane": "envelope", "gen_marker": 2}
      ]
    }
  ]
}
```

## Digest linkage

`link_hex` is the first 16 hex characters of SHA-256 (`sha256` hexdigest) over:

`envelope_bytes + "|" + kit_id + "|" + gen_marker`

Use the bytes from the authoritative lane selected for that wave (catalog, envelope, or slice bodies from the loaded kit). The reference derivation in `app/tools/link_ref.py` uses Python `hashlib` with the same rule.

## Freshness tag

`fresh_tag(actor_id, wave_id, gen_marker)` is the first 12 hex characters of SHA-256 over:

`actor_id + "|" + wave_id + "|" + gen_marker`

## Principal transitions

`principal_transitions` records one row for each adjacent wave transition after
`w0`. Actor IDs come from `/app/environment/app/data/principals.json` in file
order, keyed by the destination wave index and wrapping if a scenario has more
transitions than actors. For example, the transition into `w1` uses
`svc-writer`, and the transition into `w2` uses `svc-audit`.

## Generation markers

Waves use `wave_id` labels `w0`, `w1`, and `w2` (and `w0` only for two-wave fork scenarios). When `--inject-restart` is used, `restart_seen` in the run record must be true (boolean true, not false). Generation markers for waves following the restart boundary must advance relative to the pre-restart wave (`w2.gen_marker` > `w1.gen_marker` for the three-wave restart scenario).

## Seal slots

Each wave record includes `seal_slot`, computed as `gen_marker + phase_index` where `phase_index` is the zero-based position of the wave in its run sequence (0 for w0, 1 for w1, etc.). This rule holds for every scenario and every `--pair-order` value, including paired replay orderings where internal phase reordering differs from the wave index.

## Paired replay convergence

Scenario `n4` with `--pair-order 0` vs `--pair-order 1` must satisfy all of the following on the paired runs' `digest_records` rows:

- **Intermediate divergence:** the first row's `gen_marker` values must differ between the two orderings (`links_a[0]["gen_marker"] != links_b[0]["gen_marker"]`).
- **Final convergence:** the last row's `link_hex` values must match (`links_a[-1]["link_hex"] == links_b[-1]["link_hex"]`).
- **Correct linkage:** the shared final `link_hex` must equal the SHA-256 linkage tag computed from the authoritative lane bytes, `kit_id`, and that row's `gen_marker`.

On the final wave of scenario `n4`, generation-marker advancement must use the normalized phase index `phase_count - 1` (not the reordered intermediate phase index) so both pair orderings converge on the same final digest while earlier waves remain order-dependent.

## Idempotent reruns

Successive invocations of scenario `idempo` with the same built binary and
fixtures must produce byte-identical JSON observation reports.

## Authority lanes

Three kit bodies exist: `catalog_body`, `envelope_body`, `slice_body`. The active lane for digest material must match the reconciled surface for that scenario phase.

`reconcile_b` maps `mode_flag` to lane index as follows:

| `mode_flag` | Lane index | Kit body field   | `source_lane` label |
|-------------|------------|------------------|---------------------|
| 0           | 0          | `catalog_body`   | `catalog`           |
| 1           | 1          | `envelope_body`  | `envelope`          |
| 2           | 2          | `slice_body`     | `slice`             |

Scenario drivers set `mode_flag` from the active run (for example `pl_n8` uses `2`, `f2` and `fork_x9` use `1`, restart-injection runs use `1` on post-restart phases, and catalog otherwise).
