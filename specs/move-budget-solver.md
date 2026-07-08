### Decision
GO — Attempt 1. Multi-surface M7 desk regeneration task coupling Rust ladder math, Python emitter checkpoint seeding, journal-scaled DAG folds, and poisoned checkpoint reconciliation.

### Metadata
- version: 2
- Task name: move-budget-solver
- Title: Move budget desk regeneration
- Category: games
- Languages: ["python", "rust", "bash"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["arena", "venue", "stance-hashes", "move-cap", "desk-tooling"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Operators rebuild `/app/output/m7_export.json` from fixture crates via `python3 -m environment.tools.rq_emit` after repairing `/app/environment` sources and rebuilding the native core. Export math must agree with `/app/environment/docs/m7_field_manual.md` across ledger binding, tier ladders, DAG heads, quota slices, checkpoint hygiene, and journal append rules. Poisoned checkpoint desks must reconcile without XORing stale `lane_bias` into digest walks.

### difficulty_mechanism_plan

- mechanisms: stateful_multi_step_dependencies, buried_local_constraints, rollback_recovery_requirements, cross_file_cross_format_invariants, replay_system
- adversarial_layers_count: 5
- fairness_guardrails: deterministic fixtures, published manual formulas, and verifier replay—not timing or hidden literals.
- mechanism: stateful_multi_step_dependencies
  placement: checkpoint state, journal depth, and per-crate digest walks in the emitter pipeline
  why_model_misses_it: models fix export rows while leaving checkpoint `run_seq`, journal scaling, and tag seeding order inconsistent across reruns.
  fairness_guardrail: manual documents monotonic counters and journal append rules.
- mechanism: buried_local_constraints
  placement: native tier increment mask bits versus rolling stamp bytes in the ladder core
  why_model_misses_it: agents read tier mask bits from digest output instead of pre-mix stamp byte zero per the manual.
  fairness_guardrail: field manual states tier increment inputs explicitly.
- mechanism: rollback_recovery_requirements
  placement: poisoned checkpoint fixture and checkpoint touch path
  why_model_misses_it: models XOR stale `lane_bias` into ladder stamps when reconciling poisoned desks instead of resetting bias before emit.
  fairness_guardrail: manual states `lane_bias` is checkpoint hygiene only.
- mechanism: cross_file_cross_format_invariants
  placement: Python emitter, native even-slot ledger, and schema-validated JSON export
  why_model_misses_it: trace and peak digests pass while merge_order, ledger totals, or stance DAG heads disagree across surfaces.
  fairness_guardrail: schemas and manual publish cross-field obligations.
- mechanism: replay_system
  placement: journal-depth DAG fold multiplier and replay-lane quota ordering
  why_model_misses_it: agents apply journal scaling to quota windows on export order instead of canonical pulse order.
  fairness_guardrail: manual separates export merge order from canonical quota math.

### calibration_plan

- oracle_runs: 3/3 stress plus 10/10 repeat for flake detection.
- no_op_runs: 3/3 mean 0.0 baseline.
- pass_rate_target: Python hard ceiling worst-model pass rate ≤ 20% with legitimate multi-surface reasoning failures.
