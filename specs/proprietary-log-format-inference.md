### Decision
GO

### Metadata
- Task name: proprietary-log-format-inference
- Title: Proprietary Log Format Inference
- Category: data-processing
- Task shape: reverse_engineering
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.decode_runner` rebuilds `/app/output/proprietary_log_format_inference_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by production binary log shards with generation-specific length prefixes and checksum scope.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
