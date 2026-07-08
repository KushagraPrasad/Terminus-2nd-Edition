### Decision
GO

### Metadata
- Task name: regex-extraction-trace-inference
- Title: Regex Extraction Trace Inference
- Category: data-processing
- Task shape: reverse_engineering
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.regex_runner` rebuilds `/app/output/regex_extraction_trace_inference_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by regex extractor drops capture groups when trace spans cross chunk boundaries.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
