### Decision
GO

### Metadata
- Task name: core-dump-stack-inference
- Title: Core Dump Stack Inference
- Category: debugging
- Task shape: reverse_engineering
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.stack_runner` rebuilds `/app/output/core_dump_stack_inference_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by unwind tables disagree with frame pointer chain on compact cores.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
