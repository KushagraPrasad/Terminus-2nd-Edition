### Decision
GO

### Metadata
- Task name: watchdog-restart-boundary-debug
- Title: Watchdog Restart Boundary Debug
- Category: debugging
- Task shape: repair_existing_system
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.watch_runner` rebuilds `/app/output/watchdog_restart_boundary_debug_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by watchdog restart leaves half-upgraded state across boundary transitions.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
