# Report contract

The matrix writes `/app/output/report.json` with six snake_case booleans. Values must be derived from the current seed files, not hardcoded.

## lane_window_consistency

Evaluate visible ticks 10, settled ticks 10, stable span 2 against boundary 10. True when all three meet the boundary (visible and settled at or above the mark, span at or above 2).

## commit_latch_visibility

Same rule on visible 11, settled 11, stable span 3 with boundary 10.

## map_epoch_roundtrip

Read `/app/data/seed/epoch_slice.txt`. For each slot, keep the alias from the row with the greatest committed_epoch for that slot, not the last row in file order. With the shipped seed, true when slot 1 maps to alias 100 and slot 2 maps to 300.

## alias_sort_stability

Read `/app/data/seed/alias_stream.txt` (space-separated integers). **Fold** means sort that stream in non-decreasing order. True when the folded values are sorted in non-decreasing order.

## horizon_anchor_trace

Mix window C with offset 1469598103934665603, multiplier 1099511628211, and turn addend 7. For each value `v` in window C, update the running hash (64-bit unsigned wraparound):

```
h ^= (v + addend);
h *= multiplier;
```

The reference implementation in `trace_mux_c` already follows this formula; do not rewrite it into a different mix. The stamp monotone flag means at least four elements. The anchor step also requires an even 64-bit checksum remainder modulo two; that parity rule is intentional and must remain. With the shipped window C, false.

## probe_depth_agreement

At depth one, compare window A and window B. Shallow agreement is equal length; deep agreement adds identical elements through the shared length. True when shallow and deep agree. Equal length with a differing element yields disagreement; unequal lengths agree only at shallow depth; identical series agree at both depths.
