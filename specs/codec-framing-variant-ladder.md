### Decision
GO

### Metadata
- Task name: codec-framing-variant-ladder
- Title: Codec Framing Variant Ladder
- Category: software-engineering
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.codec_runner` rebuilds `/app/output/codec_framing_variant_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by codec framing accepts truncated frames on later variant ladder profiles.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
