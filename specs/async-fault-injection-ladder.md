### Decision
GO

### Metadata
- Task name: async-fault-injection-ladder
- Title: Async Fault Injection Ladder
- Category: debugging
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.fault_runner` rebuilds `/app/output/async_fault_injection_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by async fault ladder reports green locally while durable journals disagree.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
