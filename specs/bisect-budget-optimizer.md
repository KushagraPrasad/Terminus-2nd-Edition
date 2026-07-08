### Decision
GO

### Metadata
- Task name: bisect-budget-optimizer
- Title: Bisect Budget Optimizer
- Category: debugging
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.bisect_runner` rebuilds `/app/output/bisect_budget_optimizer_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by git bisect harness exhausts step budget before isolating flaky commit.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
