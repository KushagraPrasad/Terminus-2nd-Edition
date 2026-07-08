### Decision
GO

### Metadata
- Task name: stream-window-aggregate-drift
- Title: Stream Window Aggregate Drift
- Category: data-processing
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.stream_runner` rebuilds `/app/output/stream_window_aggregate_drift_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by tumbling window aggregates drift when watermark lag crosses shard boundaries.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
