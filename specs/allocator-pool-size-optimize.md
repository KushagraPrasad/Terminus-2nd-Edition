### Decision
GO

### Metadata
- Task name: allocator-pool-size-optimize
- Title: Allocator Pool Size Optimize
- Category: software-engineering
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.alloc_runner` rebuilds `/app/output/allocator_pool_size_optimize_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by pool allocator fragments under size-class budget while reporting healthy reuse.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
