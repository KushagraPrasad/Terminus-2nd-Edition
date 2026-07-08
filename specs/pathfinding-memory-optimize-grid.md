### Decision
GO

### Metadata
- Task name: pathfinding-memory-optimize-grid
- Title: Pathfinding Memory Optimize Grid
- Category: games
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.path_runner` rebuilds `/app/output/pathfinding_memory_optimize_grid_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by grid pathfinder exceeds memory budget while breaking admissible heuristic guarantees.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
