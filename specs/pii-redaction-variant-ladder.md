### Decision
GO

### Metadata
- Task name: pii-redaction-variant-ladder
- Title: PII Redaction Variant Ladder
- Category: data-processing
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.redact_runner` rebuilds `/app/output/pii_redaction_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by redaction pipeline keeps stale tokens when variant ladder ordering drifts.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
