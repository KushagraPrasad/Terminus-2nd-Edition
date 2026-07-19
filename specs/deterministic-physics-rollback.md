### Decision
GO — Attempt 1. Realized the deterministic physics rollback idea as a multi-component TypeScript state synchronization task: state buffer ring, collision manifold cloning, and spatial partition mapping.

### Metadata
- version: 2
- Task name: deterministic-physics-rollback
- Title: Deterministic Physics Rollback
- Category: games
- Task shape: repair_existing_system
- Languages: ["typescript"]
- Difficulty: hard
- Codebase size: minimal
- Subcategories: ["math", "performance"]
- Tags: ["games", "physics", "simulation", "state_machine"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires repairing five interlocking bugs across the game state prediction loop.
- The bugs include:
  1. Off-by-one frame bounding on rollback history extraction.
  2. Overwriting state buffers without properly invalidating future frames.
  3. Leaking collision manifold coordinates via copy-by-reference on deep clone.
  4. Dropping static-to-dynamic transition elements lazily from spatial cell grids during rollback.
  5. Raw floating point error accumulation on step bounds.

### Per-gate Pitfall Inventory
- **Collapse Gate**: The files avoid keywords like "rollback_buffer" or "collision_island", satisfying collapse rules.
- **Predictability Gate**: 3-way component synchronization prevents finding the bug by reading stack traces.
- **Hidden Invariants**: Strict property-based testing and deterministic checks prevent agent hallucination without breaking tests.

### Initial Draft Commitments
- Shipped code contains three distinct buggy modules spanning $\geq 4$ files.
- Verifier tests assert cross-run output stability and isolation without tightly hardcoded metric validation.

### Public contract
You are debugging a 2D prediction game engine that manages client states. The engine uses three major subsystems that must remain perfectly consistent across updates and rollbacks. The simulation is failing deterministic checks under heavy frame rollback loops due to historic buffer management, partition drift, and memory cloning errors. Fix the implementation across the subsystems in `src/` to ensure absolute determinism across high jitter delays.

### Failure topology
The game engine skips rollback frames on high latency bounds, corrupts history when modifying current contact manifolds, drops dynamically transitioned spatial queries, and drifts structurally over thousands of bounds.

### Environment shape
A TypeScript Node.js runtime environment configured strictly offline to test and package pure typescript outputs through `tsc` and `pytest`.

### Required artifacts
Standard task tree containing task.toml, instruction.md, environment/Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh.

### Test plan
- `test_jitter_rollback_determinism`
- `test_island_isolation_regression`
- `test_lazy_grid_invalidation`
- `test_float_drift_prevention`

### Drafting guardrails
Keep instruction.md symptom-focused. Describe symptoms and expected invariants, but do not outline the direct code patch locations.

### satisfiability_risk
- rc2_planned_name_risk: low
- gx9_contract_risk: low
- cr1_symbol_frontier_risk: low
- hidden_contract_risk: low

### task_shape
- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: Distributed cache invalidation, spatial partition mapping and deep isolation cloning.
- collapse_risk: Local fixes to state loops fail grid tracking and rollback boundaries.

### platform_files
- path: task.toml
  role: Task metadata
- path: instruction.md
  role: Task instructions
- path: output_contract.toml
  role: Output schemas
- path: tests/test.sh
  role: Verifier script
- path: tests/test_outputs.py
  role: Verifier test cases
- path: solution/solve.sh
  role: Solution patch script
- path: environment/Dockerfile
  role: Container runtime environment
- path: construction_manifest.json
  role: Mapping manifest

### task_files
- path: environment/subsystem.a/historic_buffer.ts
  role: Historic state buffer ring
- path: environment/subsystem.b/partition_hash.ts
  role: Spatial grid logic
- path: environment/subsystem.c/graph_manifold.ts
  role: Collision isolation logic
- path: environment/subsystem.d/loop_integrator.ts
  role: Physics accumulator logic
- path: environment/subsystem.e/decoy_telemetry.ts
  role: Audit logger decoy module

### fix_frontier
- count: 4
- distribution: environment/subsystem.a/historic_buffer.ts, environment/subsystem.b/partition_hash.ts, environment/subsystem.c/graph_manifold.ts, environment/subsystem.d/loop_integrator.ts
- naming_policy: standard game engine architecture
- forbidden_stems: []
- helpers_policy: allowed
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 0
- direct_boolean_assertions_max: 2
- preferred_assertion_styles: ["metamorphic structural checks", "cross-run hash validations"]
- forbidden_assertion_styles: ["plain boolean return assertions"]

### category_profile
- challenge_family: rollback_synchronization_drift
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: "assets, grid cells, allowed/denied parameters, deterministic constraints."
- forbidden_instruction_leaks: "vulnerable sink, implementation location, exploit primitive, patch rule, specific boundary threshold."
- category_specific_hardness_bar: "Reconciliation of game state across frame predictions and deterministic boundaries."
- category_specific_verifier_risks: "None."
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
- metrics:
  - metric: functional_correctness
    weight: 0.45
    criterion: "Passes deterministic serialization hash."
  - metric: hidden_invariants
    weight: 0.25
    criterion: "Isolation logic does not bleed states into historical logs."
  - metric: state_hygiene
    weight: 0.15
    criterion: "Float boundary errors are constrained below limits."
  - metric: interface_correctness
    weight: 0.10
    criterion: "Static partition grids update dynamic transitions correctly."
  - metric: deliverable_completeness
    weight: 0.05
    criterion: "No syntax errors or uncaught exceptions."
- overall_threshold: 1.0
- reward_output: reward.txt
- binary_threshold_rule: all tests must pass

### subtype_milestone_plan
- subcategories: ["math", "performance"]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: none

### actionability_plan
- verifier_command_visible: npm test
- source_fix_intent_visible: "Fix the rollback loop in src/"
- generated_output_rule_visible: "stdout hash"
- exact_formula_home: instruction
- schema_home: instruction

### waiver_plan
- waivers_expected: false
- waiver_rationale: "No waivers planned."

### reference_pattern
- justification_if_none: "This task implements rollback physics desync checks in a single milestone."

### realism_source
- source_type: real_bug
- evidence_basis: "Inspired by standard GGPO implementations."
- upstream_or_synthetic_rationale: "Represents standard physics accumulation error tracking."
- minimization_preserves: "Physics integrations, ring buffers."
- synthetic_exception_review: "None."

### difficulty_mechanism_plan
- mechanisms: [false_green_intermediate_states, stateful_multi_step_dependencies, cross_file_cross_format_invariants, rollback_recovery_requirements]
- adversarial_layers_count: 4
- fairness_guardrails: "All invariants and build contracts are documented cleanly."
- mechanism: false_green_intermediate_states
  placement: "Single prediction jumps pass basic local validation but fail when multi-step revocations occur."
  why_model_misses_it: "Model targets single cache evictions without verifying buffer capacity boundaries."
  fairness_guardrail: "Instructions specify rollback propagation requirements."
- mechanism: stateful_multi_step_dependencies
  placement: "Verifier runs sequential batches of updates and rolls back."
  why_model_misses_it: "Model assumes clean database cache state on each call."
  fairness_guardrail: "The output contract schema lists sequence histories."
- mechanism: cross_file_cross_format_invariants
  placement: "The grid spatial index and the physics components must remain reconciled."
  why_model_misses_it: "Model fails to update grid nodes after static transitions."
  fairness_guardrail: "The instruction documents expected state consistency boundaries across components."
- mechanism: rollback_recovery_requirements
  placement: "The verifier resets the frames dynamically."
  why_model_misses_it: "Model misses precision accumulation on long horizons."
  fairness_guardrail: "The instructions declare strict float stability and history integrity requirements."
