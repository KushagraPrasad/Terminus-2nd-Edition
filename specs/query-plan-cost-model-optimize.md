### Decision
GO

### Metadata
- Task name: query-plan-cost-model-optimize
- Title: Query Plan Cost Model Optimize
- Category: data-processing
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.plan_runner` rebuilds `/app/output/query_plan_cost_model_optimize_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by warehouse planner underestimates join fanout under cardinality caps.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
