### Decision
GO — Attempt 1. Realized the lease recovery coordinator repair idea as a single-step Go debugging task: one primary reconciliation unit (reconcile.go) with metadata, tests, and spec checks.

### Metadata
- version: 2
- Task name: lease-recovery-coordinator
- Title: Lease Recovery Coordinator
- Category: system-administration
- Task shape: repair_existing_system
- Languages: ["go", "bash"]
- Difficulty: hard
- Codebase size: minimal
- Subcategories: ["state-recovery", "consistency"]
- Tags: ["concurrency", "recovery", "journals", "leases", "idempotence"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires repairing 3 files across 2 root packages (partition and reconcile). A NOP or a localized change to a single location fails the verifier tests.
- We implement FNV-1a 32-bit partition hashing, multi-stage state transitions, and global sequence ordering. This ensures the solver cannot succeed by copying basic template helpers.

### Per-gate Pitfall Inventory
- **Collapse Gate**: Ensure symbols in `construction_manifest.json` match Go packages and are not named after instruction nouns.
- **Predictability Gate (RC2)**: Renamed directories and package roots to prevent predicting the fix path solely from instruction keywords, applying rc2 waivers where appropriate.
- **Hidden Invariants (No Hidden Contracts)**: All tested literals are either documented in the spec/contract or derived using explicit variables in Python assertions.

### Initial Draft Commitments
- Shipped code contains three distinct buggy files under two package roots: resolver.go, state_machine.go, and reconcile.go.
- Verifier tests assert specific failure sequences, including stale lease, heartbeat extension, completion transitions, and expired lease requeue.

### Public contract
A lease recovery coordinator reconstructs consistent job lease states from shard files and append-only journals. Fix the Go implementation under `/app` to process events in global order, support idempotency, handle cross-shard duplicates by selecting canonical shards via FNV-1a, and validate owner/epoch criteria before updating job states.

### Failure topology
The Go reconciliation process fails to process journals in global order, lacks cross-shard duplicate resolution, ignores epoch and deadline parameters for lease updates, and fails to handle idempotency correctly.

### Environment shape
A Go scheduling database workspace. Shards stored as JSON under `root/shards/*.json` and journals as jsonl under `root/journal/*.jsonl`. Built using Go compiler.

### Required artifacts
Standard task tree containing task.toml, instruction.md, environment/Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh.

### Test plan
- `test_duplicate_jobs_moved_to_canonical_shards_before_old_shard_replay_apply`
- `test_global_sequence_order_prevents_file_order_from_accepting_stale_complete`
- `test_heartbeat_and_complete_must_match_owner_epoch_and_deadline`
- `test_late_heartbeat_stale_lease_bad_fail_and_summary_counts`
- `test_expired_leases_requeue_after_all_events_and_rerun_is_idempotent`
- `test_seeded_journal_scenario_exercises_duplicate_ids_unknown_jobs_and_tie_breaks`

### Drafting guardrails
Keep instruction.md symptom-focused. Do not name specific internal code functions or variable configurations in the instruction prompt.

### satisfiability_risk
- rc2_planned_name_risk: Low risk, filename matches standard domain name structure.
- gx9_contract_risk: Low risk, no test cases enumerated.
- cr1_symbol_frontier_risk: Low risk, symbols correctly mapped.
- hidden_contract_risk: Low risk, verifier matches specifications.

### task_shape
- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: Complex multi-part state consistency constraints and strict event ordering rules.
- collapse_risk: Describing the exact FNV-1a shard selection logic collapses the task to copy-paste.

### platform_files
- path: task.toml
  role: Metadata definition
- path: instruction.md
  role: Public task instruction
- path: output_contract.toml
  role: Structured output contract
- path: tests/test.sh
  role: Test verifier runner
- path: tests/test_outputs.py
  role: Python test assertions
- path: solution/solve.sh
  role: Solution script executing reconcile code patch
- path: environment/Dockerfile
  role: Container runtime definition
- path: construction_manifest.json
  role: Authoring manifest mapping

### task_files
- path: environment/app/reconcile/reconcile.go
  role: Main reconciliation logic module (oracle frontier)
- path: environment/app/reconcile/state_machine.go
  role: State machine logic module (oracle frontier)
- path: environment/app/partition/resolver.go
  role: Partition resolver logic module (oracle frontier)
- path: environment/app/internal/model/types.go
  role: Core data structures decoy
- path: environment/app/internal/store/store.go
  role: Persistence logic storage loader decoy

### fix_frontier
- count: 3
- distribution: environment/app/reconcile/reconcile.go, environment/app/reconcile/state_machine.go, environment/app/partition/resolver.go
- naming_policy: descriptive logic naming
- forbidden_stems: []
- helpers_policy: helper functions are permitted in the same reconcile module
- symbol_thin_preferred: false

### contract_surface
- boolean_fields_max: 0
- direct_boolean_assertions_max: 6
- preferred_assertion_styles: JSON file output checks, numeric fields in JSON report, exit codes.
- forbidden_assertion_styles: hardcoded test-only results mapping.

### category_profile
- challenge_family: lease_recovery_coordinator
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: CLI execution form, database shard locations, output report schema.
- forbidden_instruction_leaks: detailed event acceptance conditional branches, FNV-1a hash key matching details.
- category_specific_hardness_bar: Complex state transitions and multi-stage duplicate reconciliation rules.
- category_specific_verifier_risks: None.
- coverage_role: target

### calibration_plan

```yaml
oracle_runs: 3
no_op_runs: 3
target_agent_runs: 20
comparator_agent_runs: 20
hard_max_pct: 20
too_easy_threshold_pct: 80
basis: Part E worst-model accuracy on platform (GPT-5.5 + Claude Opus 4.8, Jun 12 2026)
shortcut_audit: >
  read test helpers and transcribe → all algorithm helpers removed
  load env file via exec and transcribe → exec pattern removed
  static JSON output → fails verifier rerun
  patch one file only → cross-file invariant fails
ablation_plan: >
  Remove each mechanism one at a time and confirm difficulty drops.
```




### verifier_scoring_plan
- metrics: functional_correctness=0.5, hidden_invariants=0.25, state_hygiene=0.1, interface_correctness=0.1, deliverable_completeness=0.05
- overall_threshold: 1.0
- reward_output: reward.json
- binary_threshold_rule: all tests must pass

### subtype_milestone_plan
- subcategories: []
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: none

### actionability_plan
- verifier_command_visible: pytest
- source_fix_intent_visible: yes
- generated_output_rule_visible: report.json
- exact_formula_home: recovery_contract.md
- schema_home: recovery_contract.md

### waiver_plan
- waivers_expected: true
- waiver_rationale: rc2 waiver applied for predictable root keyword reconcile.

### reference_pattern
- justification_if_none: This task is a novel state recovery coordinator task designed to reconstruct distributed lease states, built from scratch to cover FNV-1a partition keys and event sequencing.

### realism_source
- source_type: real_system
- evidence_basis: Based on production lease-based scheduling systems and journal recovery models.
- upstream_or_synthetic_rationale: Replicates production state recovery coordinator behaviors.
- minimization_preserves: Complete state transitions, FNV-1a partitioning, and log-structured merge invariants.
- synthetic_exception_review: None.

### difficulty_mechanism_plan
- mechanisms: false_green_intermediate_states, cross_file_cross_format_invariants, environment_specific_cli_semantics, rollback_recovery_requirements
- adversarial_layers_count: 4
- fairness_guardrails: Complete recovery contract documentation is provided. No performance constraints.
- mechanism: false_green_intermediate_states
  placement: Shard files contain partially correct states that make NOP check pass.
  why_model_misses_it: The model will see NOP runs pass on simple scenarios and assume the logic is completely repaired.
  fairness_guardrail: The instruction requires running the verifier test suite to check correctness.
- mechanism: cross_file_cross_format_invariants
  placement: Worker journals and shard JSON configurations must be kept consistent.
  why_model_misses_it: The model will repair shard state without aligning sequence order.
  fairness_guardrail: The verification logs report exactly which invariants are mismatched.
- mechanism: environment_specific_cli_semantics
  placement: Go binary execution requires absolute container paths and specific report outputs.
  why_model_misses_it: The model will assume relative paths work and miss path checks.
  fairness_guardrail: Path rules are documented in the instruction.
- mechanism: rollback_recovery_requirements
  placement: Database journals are replayed in global sequence order.
  why_model_misses_it: The model will replay journals using alphabetical file sequence rather than global event seq order.
  fairness_guardrail: Global order specification is detailed in the contract.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```
- path: environment/app/partition/resolver.go
  symbol: ResolveDuplicates
  kind: function
  signature: func ResolveDuplicates(shards map[string]model.ShardFile, order []string) (map[string]model.ShardFile, int)
  purpose: Resolves duplicate job copies across shards and returns the cleaned shards and the number of moved jobs.
- path: environment/app/partition/resolver.go
  symbol: CanonicalShard
  kind: function
  signature: func CanonicalShard(jobID string, order []string) string
  purpose: Computes the canonical shard for a job ID using FNV-1a.
- path: environment/app/reconcile/state_machine.go
  symbol: ApplyEvent
  kind: function
  signature: func ApplyEvent(job *model.Job, event model.Event) (bool, bool)
  purpose: Validates and applies a journal event to a job state, returning whether it was applied and whether it is invalid.
- path: environment/app/reconcile/reconcile.go
  symbol: Run
  kind: function
  signature: func Run(shards map[string]model.ShardFile, order []string, events []model.Event, now int64) (map[string]model.ShardFile, model.Report)
  purpose: Executes the reconciliation cycle for database shards and worker journals.
```

#### flipping_point_contract
```
- location_id: partition_resolver
  path: environment/app/partition/resolver.go
  controls_tests:
    - test_canonical_shard_routing
    - test_duplicate_tie_breaking_only
    - test_duplicate_jobs_moved_to_canonical_shards_before_old_shard_replay_apply
    - test_seeded_journal_scenario_exercises_duplicate_ids_unknown_jobs_and_tie_breaks
- location_id: reconcile_state_machine
  path: environment/app/reconcile/state_machine.go
  controls_tests:
    - test_transition_queued_to_leased
    - test_heartbeat_extension
    - test_completion
    - test_failure
    - test_heartbeat_and_complete_must_match_owner_epoch_and_deadline
    - test_late_heartbeat_stale_lease_bad_fail_and_summary_counts
    - test_seeded_journal_scenario_exercises_duplicate_ids_unknown_jobs_and_tie_breaks
- location_id: reconcile_run
  path: environment/app/reconcile/reconcile.go
  controls_tests:
    - test_event_deduplication
    - test_global_order_only
    - test_final_expiry_only
    - test_global_sequence_order_prevents_file_order_from_accepting_stale_complete
    - test_expired_leases_requeue_after_all_events_and_rerun_is_idempotent
    - test_duplicate_jobs_moved_to_canonical_shards_before_old_shard_replay_apply
    - test_seeded_journal_scenario_exercises_duplicate_ids_unknown_jobs_and_tie_breaks

- no_single_location_flips_majority: true
- concentration_cap: 0.5
```
