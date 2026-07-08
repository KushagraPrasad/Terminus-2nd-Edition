### Decision
GO — Realized as a single-step **C++** repair task with a Python runner and bench aggregation: multi-module stencil pipeline under `/app/environment` with session journal/cache semantics, row seals, and cross-topology pane fixtures.

### Metadata
- version: 2
- Task name: stencil-equivalence-certificate
- Title: Stencil equivalence certificate repair
- Category: data-processing
- Languages: ["cpp", "python"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["cpp", "numerics", "debugging", "session-replay", "state-recovery", "serialization"]
- Milestones: 0

## Authoring Brief
Step 2a spec for the shipped task under `tasks/stencil-equivalence-certificate/`. Public contract lives in `instruction.md` and environment docs; this file documents hardness, failure modes, and gate expectations only.

### Public contract
Repair the C++ stencil observation pipeline so regenerated observation JSON matches the independent bench on committed pane fixtures and runtime-constructed layouts. Session artifacts under `/app/state` must preserve replay fidelity, journal growth rules, and generation-bound `row_seal` values. Agents regenerate through the published runner; hand-written JSON and harness bypasses are insufficient.

### Failure topology
Drift is distributed across grid indexing, topology-specific neighbor rules, weighted clamp denominators, proof-step ordering, linkage and `strip_echo` recurrence, perimeter tier tagging, cache memoization keyed only on markers, replay paths that recompute seals from live rows, and journal recovery that realigns counters without serving cached bundles. Interior halos may match while perimeter rows, linkage strings, or session counters diverge; replay and mutation scenarios expose stale cache rows when digest keys omit active fixture payloads.

### Environment shape
C++ sources under `environment/src/` (grid indexing, star fold, slot pack, seal chain, session store, pipeline main), Python runner and layout helpers under `environment/app/`, normative contract docs under `environment/app/docs/`, committed pane JSON under `environment/app/data/`, and reference halo aggregation under `environment/app/bench/`. Single-container; Makefile builds `build/stencil_pipeline`.

### category_profile
- challenge_family: data-processing
- profile_name: data_processing_cpp_repair
- allowed_instruction_disclosures: absolute paths, runner invocation, output schema fields, tolerance class, replay and journal invariants, fixture stems via NOTE.txt and contract docs.
- forbidden_instruction_leaks: `/tests/test.sh`, synthetic verifier marker lists, bench CLI as ground-truth oracle path, rubric references to editing `/tests` or `/solution`.
- category_specific_hardness_bar: Agents must reconcile numeric emission, session hygiene, and multi-topology stencil rules without a single-file patch recipe.
- category_specific_verifier_risks: Verifier rebuilds C++ via Makefile; tests compare computed halos and cached replay bytes, not static golden files in environment.

### difficulty_mechanism_plan
- mechanisms: stateful_multi_step_dependencies, buried_local_constraints, rollback_recovery_requirements, cross_file_cross_format_invariants, false_green_intermediate_states
- adversarial_layers_count: 5
- fairness_guardrails: Difficulty from coupled C++ modules, session replay semantics, and contract docs—not hidden harness paths or timing thresholds.
- mechanism: stateful_multi_step_dependencies
  placement: `environment/src/session_store.cpp` and `environment/src/pipeline_main.cpp`
  why_model_misses_it: models fix halo math on one pane while leaving `store_seq`, `journal_applied`, and marker-plus-digest cache keys inconsistent across chained recording emits.
  fairness_guardrail: journal contract and instruction disclose recording vs replay behavior.
- mechanism: buried_local_constraints
  placement: `environment/src/grid_ix.cpp` and weighted clamp denominators in star fold
  why_model_misses_it: agents patch interior halos but miss non-square stride indexing or active-weight denominators on perimeter clamp sites.
  fairness_guardrail: surface_limits.md documents halo formulas, tier rules, and topology behavior.
- mechanism: rollback_recovery_requirements
  placement: `environment/src/session_store.cpp` journal rebuild path
  why_model_misses_it: models realign `journal_applied` after truncated journal recovery but re-derive `row_seal` from live rows instead of serving cached bundles.
  fairness_guardrail: epoch_seal.md and journal contract describe replay and recovery semantics.
- mechanism: cross_file_cross_format_invariants
  placement: `environment/src/slot_pack.cpp`, `environment/src/seal_chain.cpp`, and JSON emission
  why_model_misses_it: locally sorted proof steps or plausible linkage strings fail once `strip_echo` and generation-bound `row_seal` are checked against sorted slot order and session generation counters.
  fairness_guardrail: surface_limits.md and epoch_seal.md publish linkage, strip_echo, and seal merge formulas.
- mechanism: false_green_intermediate_states
  placement: cache memoization in session store and star fold
  why_model_misses_it: agents pass committed-pane regeneration while stale cache rows still serve earlier topology or mutated fixture digests under a reused marker.
  fairness_guardrail: instruction and surface_limits document reuse stress offsets and digest-key invalidation requirements.

### calibration_plan
- oracle_runs: 1x plus 3x stress and 10x repeat for flakiness evidence
- no_op_runs: 1x plus 3x stress baseline at 0.0
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: first-look dry run on instruction plus environment listing only
- shortcut_audit: hand-written JSON, test edits, and bypassing the published runner must fail
- ablation_plan: revert single C++ modules separately; grid indexing, session replay, and seal generation each gate distinct test subsets
- pass_rate_target: hard_max_pct=20 for Python-tagged tasks; empirical label from platform Part E

### verifier_scoring_plan
- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: binary reward 1 only when all pytest cases pass
- reward_output: `/logs/verifier/reward.txt`
- binary_threshold_rule: single failed assertion fails the suite

### subtype_milestone_plan
- subcategories: []
- milestone_count: 0
- sequential_dependency: none
- local_only_data: committed pane JSON, strips sidecar, and session files under `/app/state`
- sidecar_or_protocol_notes: single-container Harbor template; no runtime network

### satisfiability_risk
- rc2_planned_name_risk: frontier modules use neutral engineering names; contract docs avoid verifier harness paths
- gx9_contract_risk: instruction documents schema and invariants without per-scenario answer tables
- hidden_contract_risk: formulas live in environment docs mirrored by instruction references, not only in tests

### actionability_plan
- verifier_command_visible: platform verifier reruns runner emission; pytest compares regenerated JSON to contract
- source_fix_intent_visible: C++ under `/app/environment` must be repaired and rebuilt via Makefile
- generated_output_rule_visible: `/app/output/stencil_emit.json` must come from the published runner
- exact_formula_home: halos, linkage, strip_echo, and row_seal formulas in surface_limits.md and epoch_seal.md
- schema_home: observation_runs and session_meta fields documented in instruction.md and output_contract.toml

### waiver_plan
- waivers_expected: collapse WARN on missing construction manifest for legacy task shape
- waiver_rationale: justify in Step 3b notes if RC2/CR warnings persist after obfuscation cleanup

### reference_pattern
- justification_if_none: No promoted reference in docs/reference_tasks/index.json matches this C++/Python stencil session-replay task; calibration is independent.

### realism_source
- source_type: synthetic_exception
- evidence_basis: Composed from multi-module numeric pipeline and session replay patterns without cloning an external bug report verbatim
- upstream_or_synthetic_rationale: Pane fixtures and session semantics are minimized to what the verifier asserts while preserving cross-module coupling
- minimization_preserves: wrap/reflect/clamp topologies, replay cache fidelity, journal recovery, and generation-bound row seals
- synthetic_exception_review: No live PII; difficulty from coupling and replay semantics, not data sensitivity

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt
- path: output_contract.toml
  role: local output declaration for stencil_emit.json
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed pytest only
- path: tests/test_outputs.py
  role: domain verifier (opaque test_p* names)
- path: solution/solve.sh
  role: oracle applying patch bundle and rebuilding pipeline
- path: environment/Dockerfile
  role: build definition; pre-install toolchain, pytest, tmux, asciinema
- path: construction_manifest.json
  role: local authoring artifact

### task_files

- path: environment/src/grid_ix.cpp
  role: oracle frontier A — grid indexing and stride rules
- path: environment/src/session_store.cpp
  role: oracle frontier B — session journal and replay cache
- path: environment/src/seal_chain.cpp
  role: oracle frontier C — generation-bound row seal merge
- path: environment/src/slot_pack.cpp
  role: oracle frontier D — proof-step ordering and linkage strings
- path: environment/app/docs/surface_limits.md
  role: halo formulas and topology rules
- path: environment/app/docs/epoch_seal.md
  role: row_seal and replay semantics

### fix_frontier

- count: 4
- distribution: environment/src/ module roots for grid, session, seal, slot
- naming_policy: Neutral engineering module names only
- forbidden_stems: [stencil, equivalence, certificate, bench, emit]
- helpers_policy: Python runner and reference aggregation helpers are non-fix; frontier stays at four C++ modules
- symbol_thin_preferred: true

### Triviality Ledger
- Hand-writing observation JSON fails because tests delete output and rerun the runner across fixtures and replay modes.
- Bench CLI spot-checks alone fail because the verifier exercises session hygiene and synthetic layouts not covered by a single stem comparison.
- Fixing only halo math without session store changes fails replay, journal recovery, and marker reuse scenarios.
- Marker-only cache keys fail mutation and cross-topology chained emits even when one pane's interior rows look correct.
