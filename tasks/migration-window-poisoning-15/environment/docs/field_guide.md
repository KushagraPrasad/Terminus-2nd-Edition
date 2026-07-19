# Field guide (navigation only)

Use this with the audit contract and migration policy. It names subsystems, not source files.

| Subsystem | Fixtures | Report flags touched |
|-----------|----------|----------------------|
| Schedule loader | g0 lane seeds | triage_ok |
| Lane admission | g0 lane seeds | bundle_lane_ok, digest_line_ok (via tally coupling) |
| Overlap hooks | g1 overlap vectors | overlap_quiet_ok, overlap_class_ok |
| Surface tally | h0 summary seeds | digest_line_ok |
| Replay fence | h2 merge seeds | replay_fence_ok, epoch_merge_ok |
| Payload shadow | (probe only) | — |

The driver binary composes gate results into `/app/output/report.json`. Probe harnesses call helpers directly; fixing gate stubs alone is insufficient.
