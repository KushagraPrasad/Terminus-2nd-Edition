### Decision
GO

### Metadata
- Task name: data-lineage-invariant-proof
- Title: Data Lineage Invariant Proof
- Category: data-processing
- Task shape: formal_reasoning
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.lineage_runner` rebuilds `/app/output/data_lineage_invariant_proof_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by lineage graph reports closed ancestry while fork edges disagree with durable journals.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
