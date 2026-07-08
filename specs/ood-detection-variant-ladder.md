### Decision
GO

### Metadata
- Task name: ood-detection-variant-ladder
- Title: OOD Detection Variant Ladder
- Category: machine-learning
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.ood_runner` rebuilds `/app/output/ood_detection_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by OOD detector accepts shifted batches on later variant ladder slices.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
