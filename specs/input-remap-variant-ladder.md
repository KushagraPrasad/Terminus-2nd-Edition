### Decision
GO

### Metadata
- Task name: input-remap-variant-ladder
- Title: Input Remap Variant Ladder
- Category: games
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.remap_runner` rebuilds `/app/output/input_remap_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by input remap table accepts out-of-order combos across variant ladder profiles.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
