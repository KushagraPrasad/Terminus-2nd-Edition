After replay maintenance, `/app/output/recovery_transcript.json` no longer matches the bundled fixtures: digest lines disagree with raw probe bytes, anchor heads drift from digest material, cleanup merge lanes and tail sequencing break, and promotion generations no longer align with `promotion_tails.json`.

Fix the Rust workspace under `/app` so `/app/bin/rx` (after a release build per `/app/docs/build_hints.txt`) emits a coherent transcript. The verifier always rebuilds from sources and reruns the driver; hand-written JSON will not count.

## Deliverable

Write `/app/output/recovery_transcript.json` with top-level `runs` and `summary`. Each run follows the phase order in `/app/data/schedule.json`. Every entry must include artifact, digest_line, anchor_head, tail_seq, tail_gen, and span_head; cleanup phases also need merge_lane. The summary must report roll_digest, phases_total, and tail_span.

## Reference

Field formulas, fixture paths, and the roll_digest reduction are documented in `/app/docs/contract.md`. Phase labels appear in `/app/docs/phase_lane_ids.txt`. Trace digest routing, coil stitching, latch replay binding, and tier loading across the `p7` and `m2` crates rather than patching only the driver shell.
