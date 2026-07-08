### Decision
GO

### Metadata
- Task name: typestate-protocol-proof
- Title: Typestate Protocol Proof
- Category: software-engineering
- Task shape: formal_reasoning
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.proto_runner` rebuilds `/app/output/typestate_protocol_proof_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by RPC layer accepts requests in wrong session phase after idle timeout.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
