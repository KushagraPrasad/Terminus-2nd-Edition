### Decision
GO

### Metadata
- Task name: differentiable-pipeline-invariant-proof
- Title: Differentiable Pipeline Invariant Proof
- Category: machine-learning
- Task shape: formal_reasoning
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.pipe_runner` rebuilds `/app/output/differentiable_pipeline_invariant_proof_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by autograd pipeline violates documented gradient sum invariants across fused ops.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
