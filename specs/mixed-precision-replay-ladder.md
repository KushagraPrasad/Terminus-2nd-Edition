### Decision
GO

### Metadata
- Task name: mixed-precision-replay-ladder
- Title: Mixed Precision Replay Ladder
- Category: machine-learning
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.mprec_runner` rebuilds `/app/output/mixed_precision_replay_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by mixed-precision replay ladder diverges when loss scaling skips micro-batch edges.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
