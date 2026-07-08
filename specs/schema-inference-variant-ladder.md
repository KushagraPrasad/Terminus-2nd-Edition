### Decision
GO

### Metadata
- Task name: schema-inference-variant-ladder
- Title: Schema Inference Variant Ladder
- Category: data-processing
- Task shape: reverse_engineering
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.schema_runner` rebuilds `/app/output/schema_inference_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by schema inference mis-orders nullable fields across variant ladder cases.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
