### Decision
GO — Attempt 1. Realized the wal-segment-pruner-drift repair idea as a single-step Rust debugging task: one primary recovery module (main.rs) with database schemas, tests, and spec checks.

### Metadata
- version: 2
- Task name: wal-segment-pruner-drift
- Title: WAL Segment Pruner Drift
- Category: data-processing
- Task shape: repair_existing_system
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: minimal
- Subcategories: ["state-recovery", "consistency"]
- Tags: ["recovery", "wal", "rust", "sqlite", "atomicity"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires repairing three distinct bugs across the WAL segment pruner lifecycle. NOP runs score 0/3, and making a localized fix in only one area will fail the verifier.
- The bugs include:
  1. Lack of transaction/state idempotency check and padding for under-sized files on staging table drain recovery.
  2. Traversal truncation on tombstoned graph nodes when resolving reachability, and potential recursion stack overflow due to cyclic dependencies.
  3. Processing directory listings in raw inode/readdir order instead of sorting by epoch.
  4. Non-atomic epoch updates causing drift.
  5. Missing database/filesystem reconciliation for unreachable segments whose physical files are missing (crash-consistency bug).

### Per-gate Pitfall Inventory
- **Collapse Gate**: Symbols in `construction_manifest.json` are thin and mapped to standard Rust function names.
- **Predictability Gate**: The folder name does not explicitly reveal the patch implementation details, preventing a purely copy-paste fix.
- **Hidden Invariants**: All requirements are declared in `instruction.md` and `output_contract.toml`.

### Initial Draft Commitments
- Shipped code contains three distinct buggy files under two package roots: resolver.go, state_machine.go, and reconcile.go.
- Verifier tests assert:
  - Staging table recovery doesn't double-count segment bytes upon crash restart.
  - Active segments are not pruned, even if their reachability graph contains intermediate tombstoned nodes.
  - Rolling digests match when processed in chronological epoch order, ignoring random directory listing order.
  - Updates of barriers are atomic and resilient to crashes.

### Public contract
A Write-Ahead Log (WAL) segment pruner manages recovery indices and prunes inactive log segments from a database. Fix the Rust implementation under `/app` to:
1. Ensure staging table drain recovery is idempotent and doesn't double-count bytes.
2. Correctly traverse reachability chains through intermediate tombstoned nodes to resolve dependencies.
3. List and reduce log segment digests in sorted epoch sequence order instead of raw filesystem readdir/inode order.
4. Atomically commit barrier modifications.

### Failure topology
The pruner fails to process recovery idempotently upon restarts (leading to double-counting or trailing mismatch on truncated logs), hangs or stack overflows on cyclic dependencies, halts reachability graph checks early on tombstone nodes (leading to incorrect deletion of active segments), processes files in raw readdir order rather than sorting by epoch, commits barriers non-atomically, and leaves database entries inconsistent for unreachable files already deleted on disk.

### Environment shape
A Rust workspace. Scaffolding is built using Rust/Cargo, loading configuration metadata and database states from `environment/data/wal.db` via the sqlite3 package.

### Required artifacts
Standard task tree containing task.toml, instruction.md, environment/Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh.

### Test plan
- `test_staging_drain_no_double_count`
- `test_staging_recovery_undersized_padding`
- `test_reachability_chain_validation`
- `test_reachability_circular_dependencies`
- `test_epoch_ordered_digest`
- `test_sync_epoch_atomicity_and_idempotency`
- `test_prune_respects_barrier_epoch`
- `test_prune_database_consistency_reconciliation`

### Drafting guardrails
Keep instruction.md symptom-focused. Describe symptoms and expected invariants, but do not outline the direct code patch locations.

### satisfiability_risk
- rc2_planned_name_risk: Low, standard file names.
- gx9_contract_risk: Low, standard verifications.
- cr1_symbol_frontier_risk: Low, clear Rust symbols.
- hidden_contract_risk: Low, no hidden verifications.

### task_shape
- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: Multi-point crash consistency, graph traversal, and filesystem ordering constraints.
- collapse_risk: Listing the exact bug lines or specific fixes collapses the task.

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
  role: Patch application script
- path: environment/Dockerfile
  role: Container runtime definition
- path: construction_manifest.json
  role: Authoring manifest mapping

### task_files
- path: environment/src/main.rs
  role: Main WAL pruner daemon (oracle frontier)
- path: environment/buffer/buffer.rs
  role: Staging table recovery module
- path: environment/graph/graph.rs
  role: Dependency reachability graph traversal module
- path: environment/timeline/timeline.rs
  role: Log segments directory lister and sorting module
- path: environment/src/decoy_catalog.rs
  role: Backup catalog decoy module
- path: environment/src/decoy_utils.rs
  role: Utility helper decoy module
- path: environment/decoy_hash.py
  role: Decoy Python dependency alignment script

### fix_frontier
- count: 3
- distribution: environment/buffer/buffer.rs, environment/graph/graph.rs, environment/timeline/timeline.rs
- naming_policy: standard Rust structure
- forbidden_stems: []
- helpers_policy: allowed
- symbol_thin_preferred: true


### contract_surface
- boolean_fields_max: 0
- direct_boolean_assertions_max: 4
- preferred_assertion_styles: JSON file comparisons, exit codes, and SQLite database check records.
- forbidden_assertion_styles: hardcoded test mappings.

### category_profile
- challenge_family: wal_segment_pruner_drift
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: database schema, directory structures, verifier command, report format.
- forbidden_instruction_leaks: detailed source fix location and exact conditional checks.
- category_specific_hardness_bar: Requires combining idempotent table recoveries, deep reachability node traversals, and epoch directory sorting.
- category_specific_verifier_risks: None.
- coverage_role: target

### calibration_plan
```yaml
oracle_runs: 3
no_op_runs: 3
target_agent_runs: 20
comparator_agent_runs: 20
human_sanity: Author verified task flow to ensure solvability.
shortcut_audit: >
  hardcode verifier return -> fails rerun validations
  solve only reachability -> fails double-count recovery tests
  solve only sorting -> fails reachability tests
ablation_plan: >
  Remove the directory sorting check or graph traversal bug and confirm score changes.
pass_rate_target:
  hard_max_pct: 20
  too_easy_threshold_pct: 80
  basis: Part E worst-model accuracy on platform (GPT-5.5 + Claude Opus 4.8, Jun 12 2026)
```

### verifier_scoring_plan
- metrics:
  - metric: functional_correctness
    weight: 0.45
    criterion: Passes basic WAL segment pruning operations.
  - metric: hidden_invariants
    weight: 0.25
    criterion: Idempotently recovers staging table and sorts log directories under arbitrary filesystems.
  - metric: state_hygiene
    weight: 0.15
    criterion: Reachability traversal is correct through tombstoned elements without leaks.
  - metric: interface_correctness
    weight: 0.10
    criterion: Output JSON matches prune_report schema.
  - metric: deliverable_completeness
    weight: 0.05
    criterion: Generates valid epoch logs and logs clean exit status.
- overall_threshold: 1.0
- reward_output: reward.txt
- binary_threshold_rule: all tests must pass

### subtype_milestone_plan
- subcategories: ["db_interaction"]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: none

### actionability_plan
- verifier_command_visible: pytest
- source_fix_intent_visible: yes
- generated_output_rule_visible: prune_report.json
- exact_formula_home: instruction.md
- schema_home: output_contract.toml

### waiver_plan
- waivers_expected: false
- waiver_rationale: no waivers expected

### reference_pattern
- justification_if_none: This task is built from scratch to model real-world crash recovery and epoch-order listing errors in log-structured storage engines.

### realism_source
- source_type: real_system
- evidence_basis: Based on database replication logs, WAL pruning architectures, and local filesystem traversal order variations.
- upstream_or_synthetic_rationale: Replicates bugs found in production WAL-purging engines.
- minimization_preserves: Complete recovery routines, SQLite transaction commits, reachability traversal, and digest generation.
- synthetic_exception_review: None.

### difficulty_mechanism_plan
- mechanisms: false_green_intermediate_states, cross_file_cross_format_invariants, rollback_recovery_requirements, environment_specific_cli_semantics
- adversarial_layers_count: 4
- fairness_guardrails: Complete recovery and sorting contract details are documented. No timing/latency checks are used.
- mechanism: false_green_intermediate_states
  placement: Intermediate builds and NOP runs pass compile and basic test checks, but fail on multi-step recovery and database-disk crash-consistency reconciliation.
  why_model_misses_it: Model assumes code is correct once compilation succeeds.
  fairness_guardrail: The test suite verifies full crash-recovery consistency and DB reconciliation.
- mechanism: cross_file_cross_format_invariants
  placement: Main database state must agree with physical directory listing digests, and reachability graph traversal must handle circular dependencies.
  why_model_misses_it: Model edits main.rs/graph.rs without handling cycles or database-disk state mismatch.
  fairness_guardrail: Mismatch/overflow errors are logged cleanly in verifier checks.
- mechanism: rollback_recovery_requirements
  placement: The system must recover correctly and idempotently from staging table across crash loops and pad under-sized files.
  why_model_misses_it: Model implements a single-pass drain without checking if records are already committed or if files need zero-padding.
  fairness_guardrail: Test suite implements multiple restarts and checks content offsets.
- mechanism: environment_specific_cli_semantics
  placement: Processing directory entries relies on epoch order rather than raw readdir/inode order.
  why_model_misses_it: Model assumes OS readdir order is chronological.
  fairness_guardrail: The instructions require processing in epoch sequence order.


### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```
- path: environment/buffer/buffer.rs
  symbol: recover_staging
  kind: function
  signature: pub fn recover_staging(db: &mut Connection, dir: &Path) -> Result<(), Box<dyn std::error::Error>>
  purpose: Recover database state from staging table after a crash restart, ensuring idempotency.
- path: environment/graph/graph.rs
  symbol: build_reachability_graph
  kind: function
  signature: pub fn build_reachability_graph(db: &Connection) -> Result<HashSet<String>, rusqlite::Error>
  purpose: Traverse graph dependency nodes to resolve file reachability, ignoring intermediate tombstones.
- path: environment/timeline/timeline.rs
  symbol: list_segments
  kind: function
  signature: pub fn list_segments(dir: &Path) -> Result<Vec<PathBuf>, std::io::Error>
  purpose: List log segment files on disk sorted in ascending order of their epoch suffix.
```

#### flipping_point_contract
```
- location_id: staging_recovery
  path: environment/buffer/buffer.rs
  controls_tests:
    - test_staging_drain_no_double_count
    - test_sync_epoch_atomicity_and_idempotency
- location_id: graph_traversal
  path: environment/graph/graph.rs
  controls_tests:
    - test_reachability_chain_validation
- location_id: segment_sorting
  path: environment/timeline/timeline.rs
  controls_tests:
    - test_epoch_ordered_digest
```

#### decoy_manifest
```
- path: environment/src/decoy_catalog.rs
  kind: file
  rhymes_with: main.rs
  non_fix_purpose: Mock catalog backup registry decoder helper.
- path: environment/src/decoy_utils.rs
  kind: file
  rhymes_with: main.rs
  non_fix_purpose: Mock base64 logging helper logic.
```

#### code_forbidden_tokens
```
- pruner
- recovery
- segments
```
