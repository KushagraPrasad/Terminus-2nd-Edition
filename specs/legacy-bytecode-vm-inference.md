### Decision
GO

### Metadata
- Task name: legacy-bytecode-vm-inference
- Title: Legacy Bytecode VM Inference
- Category: software-engineering
- Task shape: reverse_engineering
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.vm_runner` rebuilds `/app/output/legacy_bytecode_vm_inference_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by stack VM opcode widths change mid-image without magic header bump.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
