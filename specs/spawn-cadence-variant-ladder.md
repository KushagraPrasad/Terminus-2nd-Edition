### Decision
GO

### Metadata
- Task name: spawn-cadence-variant-ladder
- Title: Spawn Cadence Variant Ladder
- Category: games
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.spawn_runner` rebuilds `/app/output/spawn_cadence_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by spawn cadence drifts across variant ladder waves while local counters look stable.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
