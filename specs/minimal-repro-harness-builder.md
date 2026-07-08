### Decision
GO

### Metadata
- Task name: minimal-repro-harness-builder
- Title: Minimal Repro Harness Builder
- Category: debugging
- Task shape: constrained_build
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.repro_runner` rebuilds `/app/output/minimal_repro_harness_builder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by minimal repro harness hides race until scheduler seed budget is exhausted.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
