### Decision
GO — Attempt 1. Distributed reconciliation task with udev alias migration topology; requires reconciling multiple truth surfaces (boot records, runtime state, persisted aliases) with idempotency and conflict lineage. Symbols distributed across 3+ roots; verifier uses provenance traces not boolean verdicts.

### Metadata
- version: 2
- Task name: device-alias-migration
- Title: Device Alias Reconciliation
- Category: system-administration
- Task shape: adversarial_generalization
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (25-40 files)
- Subcategories: []
- Tags: ["udev", "device-management", "alias-reconciliation", "persistent-state", "provenance"]
- Milestones: 0

## Authoring Brief

### Public contract
The task requires implementing a robust device alias migration system that reconciles device identities across boot cycles. The agent must:

1. Read from multiple authority sources: `/app/environment/var/lib/device-registry/` (persisted state), `/app/environment/run/udev/links/` (runtime state), and `/app/environment/etc/udev/hwdb.d/` (configuration)
2. Handle conflicting alias assignments where the same device identifier appears with different alias mappings across boots
3. Produce `/app/output/device-alias-migration-observations.json` containing:
   - `reconciliation_runs`: array of run records with `run_id`, `timestamp`, `devices_processed`, `conflicts_detected`, `resolution_strategy`
   - `alias_provenance`: array mapping each device to its alias history with `device_id`, `current_alias`, `authority_chain` (array of `{source, alias, generation, confidence}`), `lineage_verified`
   - `convergence_report`: object with `final_state_hash`, `rerun_delta`, `idempotency_verified`
4. The verifier reruns the migration pipeline and checks that provenance traces survive replay with identical lineage

### platform_files

- path: task.toml
  role: metadata; sets `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt describing reconciliation requirements
- path: output_contract.toml
  role: schema for observations.json with provenance traces
- path: tests/test.sh
  role: verifier entrypoint; invokes pre-installed cargo and pytest
- path: tests/test_outputs.py
  role: domain verifier checking provenance traces, idempotency, lineage
- path: solution/solve.sh
  role: oracle implementing reconciliation with proper provenance preservation
- path: environment/Dockerfile
  role: build definition; rust toolchain, tmux, asciinema pre-installed
- path: construction_manifest.json
  role: local authoring artifact

### task_files

- path: environment/src/main.rs
  role: entrypoint with CLI subcommands `migrate`, `verify`, `replay`
- path: environment/src/udev/mod.rs
  role: udev integration layer for reading device events
- path: environment/src/registry/mod.rs
  role: persistent state management for device records
- path: environment/src/reconcile/mod.rs
  role: conflict resolution engine (fix frontier location 1)
- path: environment/src/lineage/mod.rs
  role: provenance tracking for alias assignments (fix frontier location 2)
- path: environment/src/replay/mod.rs
  role: replay/verification logic for idempotency checks (fix frontier location 3)
- path: environment/var/lib/device-registry/generation-*.db
  role: persisted device state from previous boots
- path: environment/run/udev/links/
  role: runtime udev symlink state
- path: environment/etc/udev/hwdb.d/*.hwdb
  role: hardware database configuration files
- path: environment/docs/reconciliation_contract.md
  role: public documentation of expected behavior
- path: environment/fixtures/boot-sequence-*.yaml
  role: test fixtures representing boot scenarios with conflicts

### fix_frontier

- count: 3
- distribution: reconciliation engine (src/reconcile/), lineage tracker (src/lineage/), replay verifier (src/replay/)
- naming_policy: generic module names avoiding "reconcile", "lineage", "provenance" in function names; use opaque identifiers
- forbidden_stems: [reconcile, lineage, provenance, alias, migration, authority, boot, generation, conflict, resolution]
- helpers_policy: helper modules named with neutral terms like `utils`, `core`, `base`; avoid task-noun stems
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 2 (idempotency_verified, lineage_verified are real product booleans; other fields are traces/measurements)
- direct_boolean_assertions_max: 3
- preferred_assertion_styles: [observations, traces, measurements, artifacts, computed digests, authority chains]
- forbidden_assertion_styles: [direct verdict booleans for scenario outcomes, answer-key tables, hardcoded expected aliases]

### task_shape

- type: adversarial_generalization
- instruction_framing: behavioral-target
- hardness_source: adversarial generalization
- collapse_risk: hardcoded merge priority table or simple last-write-wins passes visible fixtures but fails divergent histories

### category_profile

- challenge_family: device identity reconciliation
- profile_name: distributed_reconciliation
- allowed_instruction_disclosures: replicas or authorities (boot records, runtime state, config), conflict scenarios, accepted reconciliation outcome (surviving aliases with provenance), sync commands (migration pipeline), artifacts (observations.json with traces)
- forbidden_instruction_leaks: canonical source discovery (which authority wins), merge algorithm, stale edge detection logic, tombstone mechanics for deleted aliases
- category_specific_hardness_bar: requires reconciling multiple truth surfaces with idempotency and conflict lineage; solution must preserve full history across reruns
- category_specific_verifier_risks: count-only checks, last-write-wins shortcuts, leaked golden merged fixtures
- coverage_role: adds system-administration coverage for adversarial_generalization using udev alias migration topology; distributed_reconciliation profile gap filler

### difficulty_mechanism_plan

- mechanisms:
  - mechanism: deceptive_but_valid_local_evidence
    placement: visible smoke output shows green migration for single-boot test but fails idempotency across boot sequences
    why_model_misses_it: obvious one-pass edit satisfies only the visible local case
    fairness_guardrail: public instruction exposes the command, artifacts, schemas, and invariants without revealing the solution path
  - mechanism: partial_observability_experiment_design
    placement: solver must design small experiments over fixtures/traces to infer hidden semantics of authority precedence
    why_model_misses_it: the obvious one-pass edit satisfies only the visible local case
    fairness_guardrail: public instruction exposes the command, artifacts, schemas, and invariants without revealing the solution path
  - mechanism: false_green_intermediate_states
    placement: intermediate status or report flips green before final state convergence on rerun
    why_model_misses_it: the obvious one-pass edit satisfies only the visible local case
    fairness_guardrail: public instruction exposes the command, artifacts, schemas, and invariants without revealing the solution path
  - mechanism: cross_file_cross_format_invariants
    placement: verifier compares artifacts across code, config, logs, and generated output for lineage consistency
    why_model_misses_it: the obvious one-pass edit satisfies only the visible local case
    fairness_guardrail: public instruction exposes the command, artifacts, schemas, and invariants without revealing the solution path
- adversarial_layers_count: 4

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: human can verify by running `cargo run -- migrate && cargo run -- replay` and checking provenance chains
- shortcut_audit: reward hacks (hardcoding expected aliases), hardcoding fixture paths, test edits to match output, stale-doc shortcut reading
- ablation_plan: remove provenance tracking (layer 1), remove generation handling (layer 2), remove idempotency checks (layer 3), collapse to single authority (layer 4) — each removal should drop pass rate significantly
- pass_rate_target:
    hard_max_pct: 20
    too_easy_threshold_pct: 80
    basis: stronger target agent (comparator); aligns with Part E Hard/Medium/Easy thresholds on worst/best model accuracy
- verifier_offline: pytest and cargo baked in Dockerfile; no runtime installs in test.sh under allow_internet = false
- post_upload_difficulty: acknowledges Part E classification happens after platform agent runs

### verifier_scoring_plan

- metrics:
    - metric: functional_correctness
      weight: 0.45
      criterion: migration produces valid observations.json with correct schema
    - metric: hidden_invariants
      weight: 0.25
      criterion: provenance chains survive rerun; lineage_verified derives from authority_chain consistency
    - metric: state_hygiene
      weight: 0.15
      criterion: no leaked temporary files; idempotency verified across consecutive runs
    - metric: interface_correctness
      weight: 0.10
      criterion: CLI commands work as documented; output paths correct
    - metric: deliverable_completeness
      weight: 0.05
      criterion: all required output fields present with non-trivial content
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: overall >= 0.999 AND no critical hidden-contract or state-hygiene failures (weights 0.25 and 0.15 must achieve full credit)

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: internal workflow only
- local_only_data: true
- sidecar_or_protocol_notes: local fixtures and documented contracts only; no network protocols

### satisfiability_risk

- rc2_planned_name_risk: low; planned names separate task nouns from fix symbols using opaque identifiers
- gx9_contract_risk: low; output contract uses observations/traces and avoids verdict-restating booleans
- cr1_symbol_frontier_risk: low; oracle-touched files kept symbol-thin; helpers distributed across modules
- hidden_contract_risk: low; commands, schemas, formulas, invariants, and generated outputs are instruction-visible

### actionability_plan

- verifier_command_visible: run udev replay and check persistent alias provenance
- source_fix_intent_visible: public target (reconciliation with provenance) visible; implementation route open
- generated_output_rule_visible: /app/output/device-alias-migration-observations.json with traces, authority chains, measurements
- exact_formula_home: instruction plus public fixtures; tests derive invariants from documented workflows
- schema_home: instruction plus output_contract.toml; use observations/traces rather than boolean verdict fields

### waiver_plan

- waivers_expected: no
- waiver_rationale: no waiver expected because disclosures can be honest and verifier-visible without leaking patch or construction path

### reference_pattern

- reference_task_id: overlay-lowerdir-stale-bind
- justification_if_none: uses similar distributed reconciliation patterns but with udev/device topology instead of overlay layers

### realism_source

- source_type: real_system
- evidence_basis: tool behavior
- upstream_or_synthetic_rationale: real_system seed based on common udev aliases across boots failures; based on systemd/udev issues with persistent device naming when hardware changes or drivers reload
- minimization_preserves: causal, constraint, and semantic structure of udev aliases across boots; avoids benchmark-only module names and answer-key vocabulary
- synthetic_exception_review: not required for real source

### Failure topology
The udev device alias system produces apparently-green migration reports after a single boot, but rerunning the same migration on a system with accumulated boot history reveals lineage breaks. The core symptom is that while current boot aliases resolve correctly, the provenance chain connecting a device through multiple boot generations becomes inconsistent—earlier boots reference aliases that were later reassigned to different devices without tombstone records. The solver must discover that three distinct surfaces (persisted registry from previous boots, runtime udev state, and hardware database configuration) must be reconciled with a conflict-preserving merge strategy rather than simple precedence or last-write-wins.

### Environment shape
The environment contains a Rust crate with modular architecture:
- `src/` - Source code organized into modules: main (CLI), udev (runtime integration), registry (persistence), reconcile (conflict resolution), lineage (provenance tracking), replay (verification)
- `var/lib/device-registry/` - Simulated persisted state with generation-marked database files
- `run/udev/links/` - Simulated runtime udev symlink directory
- `etc/udev/hwdb.d/` - Hardware database configuration
- `docs/` - Public documentation of reconciliation behavior
- `fixtures/` - Boot sequence scenarios with conflict patterns

### Required artifacts
- instruction.md - Behavioral-target prompt describing reconciliation requirements
- task.toml - Metadata with version = "2.0", allow_internet = false
- output_contract.toml - Schema for observations.json
- environment/Dockerfile - Rust toolchain, tmux, asciinema
- environment/Cargo.toml - Workspace configuration
- environment/src/ - Rust source modules (6-8 files)
- environment/{var,run,etc}/ - State directories with fixtures
- environment/docs/ - Public contract documentation
- environment/fixtures/ - Boot scenario YAML files (6+ files)
- solution/solve.sh - Oracle with canary header
- tests/test.sh - Verifier runner with pytest
- tests/test_outputs.py - Domain assertions (12+ tests)

### Test plan
1. test_observations_schema_valid - JSON matches output_contract.toml schema
2. test_reconciliation_produces_all_devices - all device_ids from fixtures appear in output
3. test_alias_provenance_chain_complete - authority_chain has entries for each generation
4. test_lineage_verified_derived_from_chain - lineage_verified consistent with chain contents
5. test_convergence_rerun_delta_zero - consecutive runs produce identical state_hash
6. test_idempotency_verified_true - idempotency_verified is true after stable convergence
7. test_conflicts_detected_accurate - conflicts_detected matches fixture-defined conflict count
8. test_resolution_strategy_documented - resolution_strategy field present and valid
9. test_authority_precedence_inferred - correct authority wins without hardcoded priority table
10. test_boot_sequence_r1_r2_divergence - provenance survives different boot histories
11. test_tombstone_preservation - deleted aliases marked in history without breaking chain
12. test_partial_revert_breaks_lineage - ablation: removing lineage module breaks lineage_verified

### Drafting guardrails
Avoid naming any fix-path symbol with stems from code_forbidden_tokens list. Do not include "reconcile", "lineage", "provenance", "alias", "migration" in function or module names on the fix path. Use opaque identifiers like `op_a`, `phase_b`, `step_1`, `resolve_c`, `track_d`. Keep the reconciliation algorithm discoverable from code structure and comments describing behavior (not intent), but never name the fix approach in comments. Tests must derive expected values from fixture content, not hardcode answers.

### Triviality Ledger
- naive last-write-wins passes single-boot test but fails boot-sequence-r1-r2 test because it loses earlier generation history
- simple priority table (config > runtime > persisted) passes visible fixtures but fails divergent histories where runtime state is intentionally stale
- hardcoding expected aliases from fixtures fails because verifier uses held-out boot sequences not in training fixtures
- one-pass migration without provenance tracking produces green intermediate state but fails rerun verification

### Per-gate Pitfall Inventory
- RC1 (Oracle simplification): solve.sh must implement real reconciliation algorithm, not just copy fixture data; ensure non-boilerplate LOC >= 30
- RC2 (Oracle predictability): no "broken_", "fix_me_", "reconcile_" in file/directory names; keep paths neutral like `src/phase_a/`, `src/op_b/`
- RC3 (Verifier shallowness): tests check provenance chain consistency, not just JSON schema or file existence
- RC4 (Tamper surface): expected values computed from fixture YAML content in test code, not read from environment files
- RC5 (Reference artifacts): no golden observations.json in environment/; all expected digests computed in tests
- RC6 (Instruction specificity): instruction describes behavioral target (provenance-preserving reconciliation) without naming merge algorithm or fix locations
- RC7 (Oracle triviality): solve.sh implements distributed reconciliation with conflict lineage, not simple table lookup

### Initial Draft Commitments
- environment/Cargo.toml - workspace manifest
- environment/src/main.rs - CLI entry with subcommands
- environment/src/udev/mod.rs - udev reading module
- environment/src/registry/mod.rs - persistence layer
- environment/src/reconcile/mod.rs - conflict resolution (fix frontier A)
- environment/src/lineage/mod.rs - provenance tracking (fix frontier B)
- environment/src/replay/mod.rs - verification logic (fix frontier C)
- environment/src/core/mod.rs - shared types and utilities
- environment/var/lib/device-registry/generation-1.db - fixture data
- environment/var/lib/device-registry/generation-2.db - fixture data
- environment/var/lib/device-registry/generation-3.db - fixture data
- environment/run/udev/links/ - symlink fixtures
- environment/etc/udev/hwdb.d/10-aliases.hwdb - config fixture
- environment/docs/reconciliation_contract.md - public documentation
- environment/fixtures/boot-sequence-r1.yaml - scenario fixture
- environment/fixtures/boot-sequence-r2.yaml - scenario fixture
- environment/fixtures/boot-sequence-r3.yaml - held-out scenario
- task.toml - metadata
- output_contract.toml - schema
- instruction.md - public prompt
- solution/solve.sh - oracle
- tests/test.sh - verifier runner
- tests/test_outputs.py - domain tests

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: environment/phase_a/mod.rs
  symbol: op_a
  kind: function
  signature: fn op_a(ctx: &mut Ctx, inputs: Vec<Record>) -> Result<Resolution, Error>
  purpose: resolves conflicts between multiple authority sources

- path: environment/phase_b/mod.rs
  symbol: track_b
  kind: function
  signature: fn track_b(state: &mut State, device: Id, alias: Alias, src: Source, gen: Gen)
  purpose: records provenance information for alias assignments

- path: environment/phase_b/mod.rs
  symbol: verify_c
  kind: function
  signature: fn verify_c(chain: &[Entry]) -> bool
  purpose: validates that a provenance chain is consistent and unbroken

- path: environment/phase_c/mod.rs
  symbol: step_d
  kind: function
  signature: fn step_d(prev: &Observation, curr: &Observation) -> Delta
  purpose: compares two observation states to verify convergence

- path: environment/phase_a/mod.rs
  symbol: select_e
  kind: function
  signature: fn select_e(candidates: Vec<Candidate>, ctx: &Ctx) -> Selection
  purpose: chooses winning alias from conflicting candidates without simple precedence

- path: src/main.rs
  symbol: run_f
  kind: function
  signature: fn run_f(cmd: Command, cfg: Config) -> Result<Output, Error>
  purpose: orchestrates migration pipeline execution

#### flipping_point_contract

locations:
  - id: A
    path: environment/phase_a/mod.rs
    controls_tests: [test_resolution_strategy_documented, test_authority_precedence_inferred]
  - id: B
    path: environment/phase_b/mod.rs
    controls_tests: [test_alias_provenance_chain_complete, test_lineage_verified_derived_from_chain, test_partial_revert_breaks_lineage]
  - id: C
    path: environment/phase_c/mod.rs
    controls_tests: [test_convergence_rerun_delta_zero, test_idempotency_verified_true]
no_single_location_flips_majority: true
concentration_cap: 0.5

#### decoy_manifest

- path: environment/scan_d/mod.rs
  kind: module
  rhymes_with: op_a
  non_fix_purpose: reads runtime udev state but does not perform conflict resolution

- path: environment/store_e/mod.rs
  kind: module
  rhymes_with: track_b
  non_fix_purpose: manages persistence but does not track provenance chains

- path: src/core/mod.rs
  kind: helper
  rhymes_with: verify_c
  non_fix_purpose: provides shared types and utilities, no chain validation logic

#### code_forbidden_tokens

[reconcile, reconciliation, lineage, provenance, alias, migration, migrate, authority, boot, generation, conflict, resolution, merge, tombstone, persist, runtime, config, hwdb, udev]
