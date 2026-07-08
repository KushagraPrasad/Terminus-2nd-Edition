### Decision
GO — Attempt 1. Realized the incremental-build-graph-convergence repair idea as a multi-component Go debugging task: one primary graph module, scheduler/fingerprint module, and manifest module.

### Metadata
- version: 2
- Task name: incremental-build-graph-convergence
- Title: Incremental Build Graph Convergence Failure
- Category: build-and-dependency-management
- Task shape: repair_existing_system
- Languages: ["go", "bash"]
- Difficulty: hard
- Codebase size: minimal
- Subcategories: ["db_interaction", "tool_specific"]
- Tags: ["build", "go", "reconciliation", "fingerprint", "dag"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires repairing three distinct bugs across the incremental build system. NOP runs score 0/3, and making a localized fix in only one area will fail the verifier.
- The bugs include:
  1. Stale edges are retained in the action graph after edits because the graph walker skips unvisited nodes during sequential deletes.
  2. Action fingerprints fail to evaluate exported Go interface metadata, causing downstream scheduling decisions to reuse obsolete actions.
  3. Manifest generation does not synchronize database entries correctly, causing manifest-DB divergence.

### Per-gate Pitfall Inventory
- **Collapse Gate**: Symbols in `construction_manifest.json` are thin and mapped to standard Go module function names.
- **Predictability Gate**: The folder name does not explicitly reveal the patch implementation details, preventing a purely copy-paste fix.
- **Hidden Invariants**: All requirements are declared in `instruction.md` and `output_contract.toml`.

### Initial Draft Commitments
- Shipped code contains three distinct buggy modules: dag.go, fingerprint.go, and registry.go.
- Verifier tests assert:
  - Stale graph edges are successfully pruned after package updates.
  - Downstream targets are correctly triggered when an exported interface changes.
  - Manifest converges with build outputs and DB state.

### Public contract
A miniature incremental build engine succeeds on clean builds but gradually diverges after repeated dependency edits because the persisted dependency graph, artifact manifest, and scheduling state stop converging. Fix the Go build engine under `/app/environment` to ensure correctness across repeated incremental builds.

### Failure topology
The build engine fails to reconcile DAG edges upon package changes, fails to trigger downstream builds on exported interface changes, and manifests drift from the build database after sequential runs.

### Environment shape
A Go workspace. Scaffolding is built using Go, loading build cache and database states under `environment/`.

### Required artifacts
Standard task tree containing task.toml, instruction.md, environment/Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh.

### Test plan
- `test_edge_pruning`
- `test_sequential_package_edits`
- `test_interface_evolution_triggering`
- `test_downstream_dependency_triggering`
- `test_manifest_consistency`
- `test_complete_rebuild_verification`

### Drafting guardrails
Keep instruction.md symptom-focused. Describe symptoms and expected invariants, but do not outline the direct code patch locations.

### satisfiability_risk
- rc2_planned_name_risk: Low
- gx9_contract_risk: Low
- cr1_symbol_frontier_risk: Medium (avoid graph terminology matching implementation identifiers)
- hidden_contract_risk: Low

### task_shape
- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: Sequential graph edits, fingerprint evolution mismatch, and multi-file convergence.
- collapse_risk: Naïve fixes to single components fail multi-file convergence check.

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
- path: environment/dag/dag.go
  role: Graph edge pruning module
- path: environment/scheduler/fingerprint.go
  role: Action fingerprinting module
- path: environment/registry/registry.go
  role: Manifest sync module
- path: environment/scheduler/decoy_executor.go
  role: Decoy scheduler executor module
- path: environment/dag/decoy_sorter.go
  role: Decoy topo sorter module

### fix_frontier
- count: 3
- distribution: environment/dag/dag.go, environment/scheduler/fingerprint.go, environment/registry/registry.go
- naming_policy: standard Go module names
- forbidden_stems: []
- helpers_policy: allowed
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 0
- direct_boolean_assertions_max: 2
- preferred_assertion_styles: ["JSON diff validations", "database records verification"]
- forbidden_assertion_styles: ["shallow print assertions"]

### category_profile
- challenge_family: incremental_build_system
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: "build command, output locations, externally observable build guarantees, output schemas, deterministic behavior requirements, regeneration requirements"
- forbidden_instruction_leaks: "patch location, scheduler name, fingerprint algorithm, dependency traversal implementation, graph serialization details"
- category_specific_hardness_bar: "Verifier performs multiple sequential mutations, restarts, and check steps."
- category_specific_verifier_risks: "None."
- coverage_role: target

### calibration_plan
```yaml
oracle_runs: 3
no_op_runs: 3
target_agent_runs: 20
comparator_agent_runs: 20
human_sanity: Verified that sequential Go rebuilds and json diffs trigger on bugs.
shortcut_audit: Clearing the cache directory fails incremental consistency tests.
ablation_plan: Ablating fingerprint checks and verifying failures on downstream triggers.
pass_rate_target:
  hard_max_pct: 20
  too_easy_threshold_pct: 80
  basis: Worst-model pass rate on platform auto-eval.
```

### verifier_scoring_plan
- metrics:
  - metric: functional_correctness
    weight: 0.40
    criterion: "Passes all incremental build convergence phases."
  - metric: hidden_invariants
    weight: 0.30
    criterion: "Dependency graph correctly prunes stale edges."
  - metric: state_hygiene
    weight: 0.15
    criterion: "Downstream targets correctly trigger on interface change."
  - metric: interface_correctness
    weight: 0.10
    criterion: "Manifest matches build outputs and database state."
  - metric: deliverable_completeness
    weight: 0.05
    criterion: "Action graph converges cleanly."
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
- source_fix_intent_visible: "Fix the build engine under /app/environment."
- generated_output_rule_visible: "artifact_manifest.json"
- exact_formula_home: "environment/docs/build_contract.md"
- schema_home: "output_contract.toml"

### waiver_plan
- waivers_expected: false
- waiver_rationale: "No waivers planned."

### reference_pattern
- justification_if_none: "This task exercises incremental state consistency and scheduling in build engines."

### realism_source
- source_type: real_bug
- evidence_basis: "Bazel/Buck style interface fingerprinting and graph caching issues."
- upstream_or_synthetic_rationale: "Represents standard incremental DAG evolution challenges."
- minimization_preserves: "Graph walker, fingerprinting functions, manifest output loop."
- synthetic_exception_review: "None."

### difficulty_mechanism_plan
- mechanisms: [false_green_intermediate_states, stateful_multi_step_dependencies, cross_file_cross_format_invariants, deceptive_but_valid_local_evidence]
- adversarial_layers_count: 4
- fairness_guardrails: "All invariants and build contracts are documented cleanly."
- mechanism: false_green_intermediate_states
  placement: "Single component patches may compile and pass simple initial build tests but fail on subsequent downstream package edits."
  why_model_misses_it: "Model assumes a local test pass guarantees complete graph convergence."
  fairness_guardrail: "Test suite runs sequential build cycles checking graph serialization."
- mechanism: stateful_multi_step_dependencies
  placement: "Verifier performs mutations, cleanups, restarts, and checks outputs sequentially."
  why_model_misses_it: "Model only fixes the first-step compilation or manifest edit."
  fairness_guardrail: "Step descriptions are mapped to build guarantees."
- mechanism: cross_file_cross_format_invariants
  placement: "Reconciles action_graph.json, artifact_manifest.json, build.db, and generated outputs."
  why_model_misses_it: "Model edits only one output instead of resolving scheduler/manifest code."
  fairness_guardrail: "Convergence contract is detailed in the build contract document."
- mechanism: deceptive_but_valid_local_evidence
  placement: "Cached artifacts appear correct on clean rebuild but diverge after incremental runs."
  why_model_misses_it: "Model rebuilds cleanly or clears caches to bypass debugging the graph walker."
  fairness_guardrail: "Instructions state that complete rebuilds succeed but deterministic incremental behavior must be preserved."

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```
- path: environment/dag/dag.go
  symbol: ReconcileEdges
  kind: method
  signature: func (g *DependencyGraph) ReconcileEdges(newEdges []Edge) error
  purpose: Updates dependency graph edges, pruning stale links correctly.
- path: environment/scheduler/fingerprint.go
  symbol: ComputeActionFingerprint
  kind: function
  signature: func ComputeActionFingerprint(action *Action) (string, error)
  purpose: Computes fingerprint of a build action, including Go interface signatures.
- path: environment/registry/registry.go
  symbol: SyncRegistry
  kind: function
  signature: func SyncRegistry(dbPath string, manifestPath string) error
  purpose: Synchronizes current physical build outputs and registry manifest with database state.
```

#### decoy_manifest
```
- path: environment/scheduler/decoy_executor.go
  kind: file
  rhymes_with: fingerprint.go
  non_fix_purpose: Coordinates build execution threads (decoy scheduler subsystem).
- path: environment/dag/decoy_sorter.go
  kind: file
  rhymes_with: dag.go
  non_fix_purpose: Performs topological sorting of graph nodes for execution queues.
- path: environment/scheduler/db.go
  kind: file
  rhymes_with: fingerprint.go
  non_fix_purpose: Initializes SQLite connection pool and defines tables.
```
