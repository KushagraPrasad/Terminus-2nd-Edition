### Decision
GO

### Metadata
- Task name: deterministic-chaos-injector
- Title: Deterministic Chaos Injector
- Category: debugging
- Task shape: constrained_build
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.chaos_runner` rebuilds `/app/output/deterministic_chaos_injector_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by chaos injector repeats destructive step without idempotent recovery logging.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
