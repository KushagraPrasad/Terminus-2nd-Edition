### Decision
GO

### Metadata
- Task name: procedural-level-variant-ladder
- Title: Procedural Level Variant Ladder
- Category: games
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.level_runner` rebuilds `/app/output/procedural_level_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by procedural generator emits illegal spawn tiles on later variant ladder steps.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
