### Decision
GO

### Metadata
- Task name: checkpoint-resume-optimizer-state
- Title: Checkpoint Resume Optimizer State
- Category: machine-learning
- Task shape: repair_existing_system
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.train_runner` rebuilds `/app/output/checkpoint_resume_optimizer_state_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by training resume spikes loss when Adam bias correction uses stale global step.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
