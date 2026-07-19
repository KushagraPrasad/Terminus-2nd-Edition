# Replay window audit contract

Externally checked behavior for the migration-window replay driver and probe-linked helpers. Patch sites are not named here; map each section to the implementation using fixtures, driver gates, and `/app/environment/config/migration_policy.toml`.

## Output

- Path: `/app/output/report.json`
- Seven integer fields, each `0` or `1`: `triage_ok`, `bundle_lane_ok`, `replay_fence_ok`, `overlap_quiet_ok`, `epoch_merge_ok`, `digest_line_ok`, `overlap_class_ok`
- Regenerate on every driver run; static copies fail.

## Policy inputs

- `/app/environment/config/migration_policy.toml` holds numeric thresholds and stride values referenced below.
- Canned fixtures under `/app/environment/g0/fixtures`, `/app/environment/g1/fixtures`, `/app/environment/h0/fixtures`, and `/app/environment/h2/fixtures` supply the vectors exercised by driver gates.

## Schedule load (`triage_ok`, `sl_load_steps`)

- Honor `accept_padded_json_arrays` when loading lane step arrays from disk.
- `sl_load_steps` must succeed on the lane-seed path used at runtime.

## Lane admission (`bundle_lane_ok`, `pf_z2`)

- When `require_strict_ascending_steps` is set, admitted lane ids must be strictly increasing.
- The driver gate’s canned triple must pass after admission ordering is corrected.

## Replay fence (`replay_fence_ok`, `pf_t7`)

- Apply `marker_sequence_floor`, `marker_low_bit_count`, `use_wall_timestamp_below_floor`, `wall_timestamp_must_be_positive`, and `fold_first_payload_byte` from policy when pairing payload bytes with an epoch.
- Non-empty payloads fold the leading byte; empty payloads return an empty byte vector with the chosen epoch.

## Overlap class (`overlap_class_ok`, `wx_overlap_class`)

- Combine overlap indices using `left_stride` and `right_stride` from policy.
- The driver gate reads overlap `1` and `0` from the canned g1 overlap fixtures and expects class value `4`.

## Overlap quiet (`overlap_quiet_ok`, `pf_q3`, `wx_tail_hint_load`)

- Enforce `barrier_bit_weight` and `overlap_hint_does_not_satisfy_barrier`.
- When `normalize_tail_before_quiet_check` is set, run tail normalization before the quiet decision.
- Tail normalization follows `inactive_sentinel_non_positive`, `coalesce_duplicate_positive`, and `emit_positive_ascending`.
- A non-empty normalized tail blocks admission, including zero-only raw tails passed directly into `pf_q3`.

## Epoch merge surface (`epoch_merge_ok`)

- Large marker sequences with a present wall clock must follow the marker-floor branch from policy in the exercised merge scenario.

## Digest line (`digest_line_ok`, `sf_w9`)

- `sf_w9` must enforce `require_tally_green`, `require_zero_pending`, and `require_zero_journal_drift`.

## Payload shadow (`pf_t7_shadow`)

- When `include_trailing_bytes_beyond_shorter_side` is set, shadow XOR spans the longer payload length.

## Determinism

Two consecutive `/app/bin/mwp_driver` launches at identical environment must emit byte-identical JSON bodies.
