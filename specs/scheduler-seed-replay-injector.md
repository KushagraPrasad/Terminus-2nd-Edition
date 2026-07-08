### Decision
GO

### Metadata
- Task name: scheduler-seed-replay-injector
- Title: Scheduler Seed Replay Injector
- Category: debugging
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.sched_runner` rebuilds `/app/output/scheduler_seed_replay_injector_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by scheduler seed replay diverges when injector reorders yield points.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
