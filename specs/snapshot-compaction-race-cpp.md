### Decision
GO — Attempt 2. Fixed structured evidence IDs to canonical schema keys (`discover`, `disclosure_collapse`, `verifiable`, etc.), resolving all six blocking failures from Attempt 1. Kept the C++ topology-distributed design intact while preserving symptoms-only instruction posture.

### Metadata
- version: 2
- Task name: snapshot-compaction-race-cpp
- Title: Snapshot Compaction Race
- Category: debugging
- Languages: ["cpp"]
- Difficulty: hard
- Codebase size: small
- Subcategories: ["state-recovery", "consistency"]
- Tags: ["compaction", "restart", "recovery", "race", "consistency"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Author a single-step C++ debugging task where replay/recovery workflows intermittently report healthy state, but later generations diverge after restart or resume boundaries. The solver must produce code changes that make canonical post-boundary state stable under duplicate identity edge cases and long-horizon replay history, validated only by deterministic tests.

### Failure topology
The externally visible failure is split confidence: a visible success signal appears green while canonical state has not truly converged. Divergence manifests only after restart/resume boundaries and appears as generation disagreement in downstream reconciliation paths.

The hardness comes from three interacting surfaces: asynchronous completion signaling, shallow-versus-canonical verification depth, and stale authority remapping during reload. Each surface can look healthy in isolation while the composed system remains wrong.

### Environment shape
Use three primary subsystem roots under `environment/`: runtime core (epoch and visibility gates), persistence/remap (alias and authority restoration), and verification/checks (surface and deep consistency probes). Include support headers, fixture inputs, and decoy helpers so fix-path discovery requires behavioral reasoning rather than name matching.

### Required artifacts
Create `instruction.md`, deterministic tests, Dockerfile, test runner script, solve script, and a C++ environment with 20+ files under `environment/` (excluding Docker artifacts). Include enough compile/build scaffolding and fixture data to exercise restart/resume and collision paths. Avoid multi-container or UI patterns.

### Test plan
- Shape/coherence/digest-anchor/idempotency/tamper cases on regenerated `/app/output/report.json`.
- Replay-tail and epoch-pick ablations that flip map_epoch_roundtrip without naming oracle stems.
- Lane-tick, epoch-pick, alias-order, shallow-deep, and mix-stamp ablations that change gates or trace_digest.

Each test should be outcome-based, deterministic, and avoid pytest names that tokenize to oracle path components.

### Drafting guardrails
Keep instructions symptoms-only. Do not reveal defect locations, scenario-answer triples, or cause narratives. Keep fix-path symbols, key file names, and test names free of instruction noun tokens to prevent grep collapse. Ensure no single location controls more than 50% tests.

### task_shape
- type: repair_existing_system
- instruction_framing: Symptoms-only drift in regenerated JSON booleans across restart/resume boundaries.
- hardness_source: Coupled C++ fixes across core, store, and checks with opaque symbols and decoy neighbors.
- collapse_risk: RC6 if instruction recites answer tables; contract lives in environment/docs/report_contract.md.

### platform_files
- path: `task.toml`
  role: Harbor metadata, timeouts, reference_pattern, category_profile.
- path: `instruction.md`
  role: Public contract for agents.
- path: `output_contract.toml`
  role: Repo-local structured output checklist.
- path: `tests/test.sh`
  role: Offline pytest entry.
- path: `tests/test_outputs.py`
  role: Outcome assertions on rebuilt binary and JSON.
- path: `solution/solve.sh`
  role: Oracle patches and rebuild.
- path: `environment/Dockerfile`
  role: Pinned image with verifier venv.
- path: `construction_manifest.json`
  role: Optional frozen symbol table for collapse tooling when present.

### task_files
- path: `environment/src/core/phase_gate.cpp`
  role: Oracle frontier — tick readiness.
- path: `environment/src/store/rebind_table.cpp`
  role: Oracle frontier — slot alias remap on reload.
- path: `environment/src/checks/qv_pair.cpp`
  role: Oracle frontier — shallow versus deep window agreement (shipped as surface_probe.cpp).
- path: `environment/src/core/identity_fold.cpp`
  role: Oracle frontier — fold stream ordering.
- path: `environment/src/checks/checksum_accept.cpp`
  role: Oracle frontier — mix checksum acceptance (shipped as history_scan.cpp).
- path: `environment/src/store/ring_bridge_m_cache.cpp`
  role: Decoy cache module; not on flipping-point contract.

### fix_frontier
- count: 5
- distribution: Substantive symbols under `environment/src/core`, `environment/src/store`, and `environment/src/checks`.
- naming_policy: Opaque identifiers on the fix path; instruction nouns must not grep onto frontier symbols.
- forbidden_stems: compaction, restart, recovery, race
- helpers_policy: Co-resident decoy modules listed in task_files and excluded from the flipping-point contract.
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 1
- direct_boolean_assertions_max: 1
- preferred_assertion_styles: dict equality on regenerated `/app/output/report.json` versus independent expectation model.
- forbidden_assertion_styles: scenario-to-key answer grids in instruction text.

### category_profile
- challenge_family: debugging
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: absolute paths, JSON key names, build/run commands, report_contract.md semantics.
- forbidden_instruction_leaks: exact patch recipes, answer-key tables.
- category_specific_hardness_bar: Agents align multiple translation units without named fix sites.
- category_specific_verifier_risks: Verifier rebuilds must stay deterministic.
- coverage_role: Exercises readiness gates, remap authority, fold ordering, anchor parity, and depth agreement.

### difficulty_mechanism_plan
- mechanisms: buried_local_constraints, stateful_multi_step_dependencies, rare_local_vocabulary, cross_file_cross_format_invariants
- adversarial_layers_count: 4
- fairness_guardrails: No timing-as-hardness; NOP baseline fails; oracle deterministic.

### calibration_plan
- oracle_runs: 1x mean 1.0 final evidence; 10x repeat for flakiness.
- no_op_runs: 1x mean 0.0 baseline.
- target_agent_runs: platform trials outside this repo.
- comparator_agent_runs: not used.
- human_sanity: first-look dry run on instruction plus environment listing.
- shortcut_audit: hand-written JSON without rebuild must fail pytest.
- ablation_plan: flipping-point contract documents per-location revert subsets.
- pass_rate_target: oracle 100 percent on shipped verifier.

### verifier_scoring_plan
- metrics: functional_correctness weight 0.45; hidden_invariants weight 0.2; state_hygiene weight 0.1; interface_correctness weight 0.15; deliverable_completeness weight 0.1
- overall_threshold: binary reward 1 only if all pytest cases pass.
- reward_output: `/logs/verifier/reward.txt` with 0/1 footer.
- binary_threshold_rule: single failed assertion fails the suite.

### subtype_milestone_plan
- subcategories: none beyond standard Edition 2 metadata.
- milestone_count: 0
- sequential_dependency: none
- local_only_data: seed JSON and C++ sources under `environment/` only.
- sidecar_or_protocol_notes: single-service compose per Harbor template without custom networks block.

### satisfiability_risk
- rc2_planned_name_risk: Mitigated by opaque stems, decoys, and helpers_policy.
- gx9_contract_risk: Boolean keys documented in report_contract.md without answer tables in instruction.
- cr1_symbol_frontier_risk: Five oracle frontiers with decoys declared in task_files.
- hidden_contract_risk: Full derivation rules in environment/docs/report_contract.md.

### actionability_plan
- verifier_command_visible: cmake configure and build under `/app/build`, run `/app/bin/snapshot_matrix`, pytest on `/tests/test_outputs.py`.
- source_fix_intent_visible: Repair C++ under `/app/src` so the matrix regenerates JSON.
- generated_output_rule_visible: Hand-edited `/app/output/report.json` is rejected.
- exact_formula_home: Horizon mix, parity gate, tick boundaries, and depth agreement in `/app/docs/report_contract.md`.
- schema_home: Six snake_case booleans listed in instruction.md and report_contract.md.

### waiver_plan
- waivers_expected: collapse WARN band for legacy manifest absence documented in Step 3b.
- waiver_rationale: N/A unless platform requests hygiene exception.

### reference_pattern
- justification_if_none: No promoted reference in docs/reference_tasks/index.json matches this C++/CMake snapshot compaction race repair task; hardness calibrated independently.

### realism_source
- source_type: synthetic_exception
- evidence_basis: Composed multi-module recovery pattern without cloning an external bug report.
- upstream_or_synthetic_rationale: Seeded windows and epoch rows minimize data while preserving coupling.
- minimization_preserves: Restart/remap and depth-agreement semantics exercised by pytest.
- synthetic_exception_review: No live PII; difficulty from coupling not data sensitivity.

### Triviality Ledger
- Single-function ready-signal delay cannot pass because map-roundtrip and probe-depth tests remain failing until cross-root logic is repaired.
- Pure verifier extension cannot pass because reload/remap invariants still diverge under restart boundaries.
- Prompt noun grep is blocked by opaque fix-path symbols and decoy modules that structurally rhyme.

### Per-gate Pitfall Inventory
- RC1/RC2: Avoid concentrated oracle edits; enforce three-root fix frontier.
- RC6/GX9/GX10: Keep instruction symptoms-only; avoid contract recital and polarity contradictions.
- RC7/GX3: Ensure substantive non-boilerplate solve logic, not cosmetic diff inflation.
- GX1/GX2/GX4: Avoid corrective comments and low-delta/no-op bulk rewrites.
- GX5/GX7/GX8: Keep tested derivations anchored in environment code, not instruction-only literals.
- Static checks: preserve schema-complete metadata and deterministic test contract.

### Initial Draft Commitments
- `tasks/snapshot-compaction-race-cpp/task.toml`
- `tasks/snapshot-compaction-race-cpp/output_contract.toml`
- `tasks/snapshot-compaction-race-cpp/instruction.md`
- `tasks/snapshot-compaction-race-cpp/tests/test.sh`
- `tasks/snapshot-compaction-race-cpp/tests/test_outputs.py`
- `tasks/snapshot-compaction-race-cpp/solution/solve.sh`
- `tasks/snapshot-compaction-race-cpp/environment/CMakeLists.txt`
- `tasks/snapshot-compaction-race-cpp/environment/Dockerfile`
- `tasks/snapshot-compaction-race-cpp/environment/config/runtime.toml`
- `tasks/snapshot-compaction-race-cpp/environment/config/probe.toml`
- `tasks/snapshot-compaction-race-cpp/environment/include/core/phase_gate.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/include/core/epoch_trace.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/include/core/identity_fold.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/include/store/rebind_table.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/include/store/ledger_mux.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/include/checks/surface_probe.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/include/checks/history_scan.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/include/checks/order_probe.hpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/core/phase_gate.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/core/epoch_trace.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/core/identity_fold.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/store/rebind_table.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/store/ledger_mux.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/checks/surface_probe.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/checks/history_scan.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/checks/order_probe.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/core/phase_latch_q_shadow.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/store/ring_bridge_m_cache.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/src/checks/probe_gate_v_debug.cpp`
- `tasks/snapshot-compaction-race-cpp/environment/data/seed/window_a.json`
- `tasks/snapshot-compaction-race-cpp/environment/data/seed/window_b.json`
- `tasks/snapshot-compaction-race-cpp/environment/data/seed/window_c.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
- path: environment/core/phase_gate.cpp
  symbol: phase_latch_q
  kind: function
  signature: bool phase_latch_q(const TickFrame& tf, uint64_t edge_mark)
  purpose: Emits external readiness marker based on internal settle-state progression.
- path: environment/store/rebind_table.cpp
  symbol: ring_bridge_m
  kind: function
  signature: void ring_bridge_m(StoreState& st, const EpochSlice& es)
  purpose: Rebuilds persisted alias bridge view during bootstrapped load transitions.
- path: environment/checks/qv_pair.cpp
  symbol: probe_gate_v
  kind: function
  signature: ProbeReport probe_gate_v(const ProbeInput& in, int depth_mode)
  purpose: Computes health projection over both shallow and canonical consistency paths.
- path: environment/core/stamp_mux.cpp
  symbol: trace_mux_c
  kind: function
  signature: EpochStamp trace_mux_c(const SpanBatch& sb, uint32_t turn_id)
  purpose: Builds deterministic epoch stamp used by downstream persistence and checks.

#### flipping_point_contract
locations:
  - id: A
    path: environment/core/phase_gate.cpp
    controls_tests: [test_lane_window_consistency, test_commit_visibility]
  - id: B
    path: environment/store/rebind_table.cpp
    controls_tests: [test_map_roundtrip]
  - id: C
    path: environment/checks/qv_pair.cpp
    controls_tests: [test_alias_sort_stability, test_horizon_mix]
no_single_location_flips_majority: true
concentration_cap: 0.5

#### decoy_manifest
- path: environment/core/phase_latch_q_shadow.cpp
  kind: helper
  rhymes_with: phase_latch_q
  non_fix_purpose: Provides offline diagnostics for synthetic benchmark traces unrelated to recovery path.
- path: environment/store/ring_bridge_m_cache.cpp
  kind: module
  rhymes_with: ring_bridge_m
  non_fix_purpose: Caches compaction metrics snapshots for reporting output only.
- path: environment/checks/probe_gate_v_debug.cpp
  kind: helper
  rhymes_with: probe_gate_v
  non_fix_purpose: Formats developer debug summaries without affecting pass/fail behavior.

#### code_forbidden_tokens
code_forbidden_tokens: [restart, resume, recovery, generations, operators, replay, compaction, completion, reconciliation, mappings, identities]
