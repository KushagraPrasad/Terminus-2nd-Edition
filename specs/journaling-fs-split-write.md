### Decision
GO — Attempt 1. Realized the journaling-fs-split-write recovery task as a C debugging task.

### Metadata
- version: 2
- Task name: journaling-fs-split-write
- Title: Journaling Filesystem Split Write Recovery
- Category: system-administration
- Task shape: repair_existing_system
- Languages: ["c"]
- Difficulty: hard
- Codebase size: minimal
- Subcategories: ["state-recovery", "consistency"]
- Tags: ["c", "filesystem", "recovery", "linux", "systems"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires repairing the recovery logic in journal.c to handle split writes and maintain invariants without corruption. NOP runs score 0/3.
- The bugs include:
  1. Incorrect 4KB boundary split write check in recovery.
  2. Failure to rollback secondary checksum tree perfectly during transaction recovery failure.
  3. Resetting daemon states incorrectly causing subsequent write panics.

### Per-gate Pitfall Inventory
- **Collapse Gate**: Symbol table and manifest mapping targets are thin.
- **Predictability Gate**: Folder name is domain-oriented.
- **Hidden Invariants**: All requirements are declared in instruction.md.

### Initial Draft Commitments
- Shipped code is under environment/ and contains fs_daemon.c, journal.c, inode.c, and fs.h.

### Public contract
A userspace filesystem daemon implements a simple WAL. During crash recovery, the daemon must handle split writes on 4KB boundaries, rollback the secondary checksum tree correctly on failure, remain idempotent, and support immediate writing of new data after recovery.

### Failure topology
The daemon recoveries lead to corruption or panic during subsequent writes due to incorrect split-write boundaries, lack of perfect rollback, and improper state reset.

### Environment shape
C runtime environment compiled with Makefile.

### Required artifacts
Standard task tree containing task.toml, instruction.md, environment/Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh.

### Test plan
- test_split_write_recovery
- test_checksum_tree_preservation
- test_immediate_write_after_recovery
- test_idempotent_recovery

### Drafting guardrails
Symptom-only instruction.md.

### satisfiability_risk
- rc2_planned_name_risk: low
- gx9_contract_risk: low
- cr1_symbol_frontier_risk: low
- hidden_contract_risk: low

### task_shape
- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: C filesystem recovery, journal replay and checksum tree rollbacks.
- collapse_risk: Fixes to rollback must handle boundary checks perfectly.

### platform_files
- path: task.toml
  role: Task metadata
- path: instruction.md
  role: Public contract
- path: output_contract.toml
  role: Output contract specifications
- path: tests/test.sh
  role: Verifier script
- path: tests/test_outputs.py
  role: Verifier assertions
- path: solution/solve.sh
  role: Solution script
- path: environment/Dockerfile
  role: Pinned Docker image
- path: construction_manifest.json
  role: Mapping manifest

### task_files
- path: environment/fs_daemon.c
  role: CLI daemon interface
- path: environment/journal.c
  role: Journal recovery logic
- path: environment/inode.c
  role: Inode management

### fix_frontier
- count: 3
- distribution: environment/journal.c
- naming_policy: symbols
- forbidden_stems: recovery, split
- helpers_policy: inline
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 1
- direct_boolean_assertions_max: 1
- preferred_assertion_styles: exit-code and state verification
- forbidden_assertion_styles: scenario tables

### category_profile
- challenge_family: system-administration
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: recover CLI command, 4KB boundary, transaction format, super block layout.
- forbidden_instruction_leaks: patch locations or direct fix recipes.
- category_specific_hardness_bar: Idempotency and perfect rollback of checksum tree must be achieved.
- category_specific_verifier_risks: verifier must run in container, tempfile isolated environments.

### calibration_plan
- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: "verified functional recovery of journal entries"
- shortcut_audit: "Attempting to bypass recovery tests by writing dummy states directly fails state-hygiene verification."
- ablation_plan: "Disabling checksum tree validation reduces verification coverage."

### verifier_scoring_plan
- metrics:
  - metric: functional_correctness
    weight: 0.45
    criterion: "Passes all journal recovery and split-write checks."
  - metric: hidden_invariants
    weight: 0.25
    criterion: "Idempotent recovery invariants are maintained."
  - metric: state_hygiene
    weight: 0.15
    criterion: "Secondary checksum tree is preserved perfectly."
  - metric: interface_correctness
    weight: 0.10
    criterion: "Daemon supports writing new data after recovering."
  - metric: deliverable_completeness
    weight: 0.05
    criterion: "Rebuilt binaries run cleanly."
- overall_threshold: 1.0
- reward_output: reward.txt
- binary_threshold_rule: all tests must pass

### subtype_milestone_plan
- subcategories: ["state-recovery", "consistency"]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: none

### actionability_plan
- verifier_command_visible: "pytest"
- source_fix_intent_visible: "Fix fs_daemon C source files under /app/environment"
- generated_output_rule_visible: "disk.bin recovery"
- exact_formula_home: instruction
- schema_home: instruction

### waiver_plan
- waivers_expected: false
- waiver_rationale: "No waivers planned."

### reference_pattern
- justification_if_none: "This task implements C-based userspace journaling recovery, split write handling, and secondary checksum tree verification, which has no direct matching template in the reference tasks."

### realism_source
- source_type: real_bug
- evidence_basis: "Inspired by filesystem journaling recovery failures under power loss / split writes."
- upstream_or_synthetic_rationale: "FS journaling recovery failure and secondary metadata corruption."
- minimization_preserves: "Journal recovery loops and checksum tree metadata."
- synthetic_exception_review: "None."

### difficulty_mechanism_plan
- mechanisms: [false_green_intermediate_states, stateful_multi_step_dependencies, cross_file_cross_format_invariants, rollback_recovery_requirements]
- adversarial_layers_count: 4
- fairness_guardrails: "All invariants and formats are documented."
- mechanism: false_green_intermediate_states
  placement: "journal.c"
  why_model_misses_it: "overlooks boundary split checks"
  fairness_guardrail: "super block and journal format specifications"
- mechanism: stateful_multi_step_dependencies
  placement: "journal.c"
  why_model_misses_it: "drops final block recovery"
  fairness_guardrail: "transaction log details"
- mechanism: cross_file_cross_format_invariants
  placement: "journal.c"
  why_model_misses_it: "corrupts secondary tree"
  fairness_guardrail: "checksum verification rules"
- mechanism: rollback_recovery_requirements
  placement: "journal.c"
  why_model_misses_it: "ignores rollback ordering"
  fairness_guardrail: "monotonic check specifications"
