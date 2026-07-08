### Decision
GO

### Metadata
- Task name: collision-layer-variant-ladder
- Title: Collision Layer Variant Ladder
- Category: games
- Task shape: formal_reasoning
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.collision_runner` rebuilds `/app/output/collision_layer_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by collision layers disagree on overlap when variant ladder masks swap mid-tick.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
