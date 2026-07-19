### Decision
GO — Create a new C++ scientific-computing task: symplectic-orbit-resonance.

### Metadata
- version: 2
- Task name: symplectic-orbit-resonance
- Title: Symplectic Orbit Resonance
- Category: scientific-computing
- Task shape: repair_existing_system
- Languages: ["cpp"]
- Difficulty: hard
- Codebase size: minimal
- Subcategories: ["math", "physics"]
- Tags: ["scientific-computing", "physics", "simulation", "differential-equations"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires repairing five interlocking bugs across the orbital integration engine.
- The bugs include:
  1. Integrator step ordering violating velocity verlet symplectic half-steps.
  2. Naive time step scaling omitting the required momentum/velocity coordinate ratio updates.
  3. Parenthesization order error in the Kahan float precision accumulator.
  4. Missing soft-core potential epsilon parameters leading to close encounter gravity singularities.
  5. Resonance locking checks using global sine average instead of standard deviation sliding windows.

### Per-gate Pitfall Inventory
- **Collapse Gate**: Files use generic scientific terms, avoiding keywords like "leapfrog_bug" or "kahan_bug".
- **Predictability Gate**: The bugs must be fixed concurrently; fixing only one still fails the verifier checks.

### Public contract
The solver must correct the source code under /app/environment to ensure exact energy conservation and stability across close encounters.

### Failure topology
The orbits drift linearly, close encounters trigger infinite gravitational forces or NaNs, and resonance detection gives false positives.

### task_shape
- type: repair_existing_system
- hardness_source: multi-component interaction, replay semantics
- collapse_risk: Fixes to the integrator without Kahan scaling or soft-cores fail long-term run checks.

### difficulty_mechanism_plan
- mechanisms: [false_green_intermediate_states, stateful_multi_step_dependencies, cross_file_cross_format_invariants, rollback_recovery_requirements]
- adversarial_layers_count: 4
- fairness_guardrails: "All conservation limits and tolerances are documented."
- mechanism: false_green_intermediate_states
  placement: "Short integrations pass but long-term runs drift."
  why_model_misses_it: "Model fails to correct the Kahan accumulator logic which only drifts after millions of steps."
  fairness_guardrail: "Tolerances are documented."
- mechanism: stateful_multi_step_dependencies
  placement: "Close encounters occur sequentially."
  why_model_misses_it: "Model assumes naive step size scaling without coordinate metric transformation."
  fairness_guardrail: "Step size properties are described."
- mechanism: cross_file_cross_format_invariants
  placement: "The integrator, scaler, and precision accumulator must be consistent."
  why_model_misses_it: "Model edits the leapfrog order but fails to update step size velocity scaling."
  fairness_guardrail: "Component relationships are documented."
- mechanism: rollback_recovery_requirements
  placement: "Verification performs long integrations and resets."
  why_model_misses_it: "Model misses coordinate transformations."
  fairness_guardrail: "Integrator requirements are listed."

### satisfiability_risk
- rc2_planned_name_risk: low
- gx9_contract_risk: low
- cr1_symbol_frontier_risk: low
- hidden_contract_risk: low

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
- path: environment/subsystem.a/leapfrog_integrator.cpp
  role: Coordinate integrator
- path: environment/subsystem.b/kahan_accumulator.cpp
  role: Precision accumulator
- path: environment/subsystem.c/step_transformer.cpp
  role: Step size scaler
- path: environment/subsystem.d/simulation_engine.cpp
  role: Sim loop execution

### fix_frontier
- count: 4
- distribution: environment/subsystem.a/leapfrog_integrator.cpp, environment/subsystem.b/kahan_accumulator.cpp, environment/subsystem.c/step_transformer.cpp, environment/subsystem.d/simulation_engine.cpp
- naming_policy: standard orbital mechanics engine
- forbidden_stems: []
- helpers_policy: allowed
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 1
- direct_boolean_assertions_max: 2
- preferred_assertion_styles: ["drift bounds checks", "resonance status checks"]
- forbidden_assertion_styles: ["plain boolean return assertions"]

### category_profile
- challenge_family: precision_conservation_simulation
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: "masses, coordinates, step sizes, softening parameters."
- forbidden_instruction_leaks: "vulnerable sink, implementation location, exploit primitive, patch rule, specific boundary threshold."
- category_specific_hardness_bar: "Long-term relative energy drift conservation bounds checks."
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
    criterion: "Passes energy conservation drift checks."
  - metric: hidden_invariants
    weight: 0.25
    criterion: "Softening potential limits coordinates correctly."
  - metric: state_hygiene
    weight: 0.15
    criterion: "Kahan precision tracking stops drift aggregation."
  - metric: interface_correctness
    weight: 0.10
    criterion: "Resonance detection locks standard deviation."
  - metric: deliverable_completeness
    weight: 0.05
    criterion: "No compile errors or runtime failures."
- overall_threshold: 1.0
- reward_output: reward.txt
- binary_threshold_rule: all tests must pass

### subtype_milestone_plan
- subcategories: ["math", "physics"]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: none

### actionability_plan
- verifier_command_visible: pytest
- source_fix_intent_visible: "Fix the integration step in /app/environment"
- generated_output_rule_visible: "JSON stdout blocks"
- exact_formula_home: instruction
- schema_home: instruction

### waiver_plan
- waivers_expected: false
- waiver_rationale: "No waivers planned."

### reference_pattern
- justification_if_none: "This task implements symplectic n-body orbital integration and resonance detection."

### realism_source
- source_type: real_bug
- evidence_basis: "Inspired by standard orbital mechanics simulations."
- upstream_or_synthetic_rationale: "Represents standard symplectic integration drift."
- minimization_preserves: "Physics integrations, Kahan accumulators."
- synthetic_exception_review: "None."
