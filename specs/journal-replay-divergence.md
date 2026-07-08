### Decision
GO — Attempt 1. Realized the journal replay divergence idea as a single-step **C++** debugging task: three distributed translation units (`runtime`, `ops`, `persist`) with opaque fix symbols, rhyming decoys, symptoms-only contract, and strict flipping-point test spread—no Python on the fix path.

### Metadata
- version: 2
- Task name: journal-audit-divergence
- Title: Journal audit resume divergence
- Category: debugging
- Languages: ["cpp"]
- Difficulty: hard
- Codebase size: small
- Subcategories: ["state-recovery", "consistency"]
- Tags: ["journaling", "replay", "resume", "cpp", "consistency"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Author a single-step C++ task where persistence plus recovery paths intermittently show agreement with automated checks while downstream canonical projections diverge—especially across process restarts or resume handoffs and during long audits. The agent must change the supplied CMake/C++ environment so deterministic tests demonstrate stable agreement between surface checks and authoritative outcomes across cold starts and overlapping generations, without hand-authored golden strings that encode the defect story in tests or comments.

### Failure topology
The visible failure is split confidence: automated stages read healthy while digests, baselines, or staff-run aids disagree; long trace walks can hide where divergence first appeared. The underlying failure couples three behaviors: a resume handoff path that can omit an invalidation on one edge class, a fast aggregation path that can signal success on a shallow window while canonical derivation lags, and a reconstruction fold that resolves ties among overlapping captures using the wrong precedence for authority. Each cluster can look locally plausible; together they produce generation skew that only shows up after boundaries.

### Environment shape
Provide three primary C++ roots under `environment/`: `runtime/` (handoff bitmaps and envelope staging into persist), `ops/` (fast aggregate path feeding audit tooling), and `persist/` (merge/fold of captured views into stored canonical projections). Add headers, fixture JSON under a corpus, a small CLI driver under `tools/`, and rhyming decoy `.cpp` files that resemble fix-path modules but implement unrelated diagnostics. Build and link with CMake; single-container only.

### Required artifacts
Create `instruction.md`, a deterministic test entrypoint, Dockerfile, `solution/solve.sh`, and a C++ tree with **20+ files** under `environment/` excluding Docker artifacts. Include enough headers and fixture data to exercise restart/resume boundaries, long replay horizons, and cold-start equivalence. Do not introduce multi-container layouts or UI-building harnesses.

### Test plan
- `test_qz_m7_emit`: restart/bookmark boundary — handoff bitmap must invalidate the correct edge class; wrong marking fails even if downstream merge looks plausible.
- `test_pl_n4_pair`: shallow vs canonical — fast aggregate must not report success while canonical rows disagree across generations.
- `test_kx_f2_cycle`: merge authority — tie-breaking among overlapping captures must respect authoritative precedence, not lexical convenience.
- `test_triad_q8a`: paired flipping check tied to location A (mux handoff) together with emit semantics.
- `test_triad_pl8b`: paired flipping check tied to location B (ops gate) with multi-step audit input.
- `test_triad_kx8c`: paired flipping check tied to location C (persist fold) including cold-start reload.

Each test must be outcome-based and chain only on shared environment build artifacts, not on solver-specific constants embedded in the instruction.

### Drafting guardrails
Keep `instruction.md` symptoms-only: describe intermittent false agreement and generation drift after restarts and long audits without naming defect categories, files, or algorithms. Ban instruction nouns from fix-path symbol names, directory names on the oracle frontier, and test function identifiers. No comments or fixtures that reveal which of the three clusters is wrong. Keep test concentration under 50% for any single flipping-point file.

### task_shape
- type: repair_existing_system
- instruction_framing: Symptoms-only mismatch between regenerated JSON booleans and mux refresh, lane gate, and fold arbitration implied by frozen vectors.
- hardness_source: Coupled C++ fixes across runtime, ops, and persist with opaque symbols and decoy neighbors.
- collapse_risk: RC6 checklist drift if instruction recites per-scenario answer tables; GX9 saturation if booleans multiply without observation-shaped checks.

### platform_files
- path: `task.toml`
  role: Harbor metadata, timeouts, reference_pattern for calibration.
- path: `instruction.md`
  role: Public contract for agents.
- path: `output_contract.toml`
  role: Repo-local structured output checklist mirrored into instruction.
- path: `tests/test.sh`
  role: Verifier entry that installs deps and runs pytest.
- path: `tests/test_outputs.py`
  role: Outcome assertions on rebuilt binaries and JSON.
- path: `solution/solve.sh`
  role: Oracle applies patches and rebuilds deterministically.
- path: `environment/Dockerfile`
  role: Pinned image build for the audit workspace.
- path: `construction_manifest.json`
  role: Frozen symbol table and flipping-point contract for collapse tooling.

### task_files
- path: `environment/runtime/src/mux_slice.cpp`
  role: Oracle frontier A — mux refresh / edge bitmap staging.
- path: `environment/runtime/src/mux_clamp.cpp`
  role: Co-resident decoy module; not on flipping-point contract.
- path: `environment/ops/src/replay_gate.cpp`
  role: Oracle frontier B — lane gate and audit cell wiring.
- path: `environment/ops/src/replay_scan.cpp`
  role: Co-resident decoy helper; not on flipping-point contract.
- path: `environment/persist/src/wal_fold.cpp`
  role: Oracle frontier C — fold arbitration between captured rows.

### fix_frontier
- count: 3
- distribution: One substantive symbol each under `environment/runtime/src`, `environment/ops/src`, and `environment/persist/src`.
- naming_policy: Opaque fix-path identifiers; instruction nouns must not grep onto frontier symbols (CR7).
- forbidden_stems: mux, gate, fold, wal, replay, audit
- helpers_policy: Co-resident `.cpp` helpers in the same directories are listed in `task_files` and excluded from the flipping-point contract unless promoted into the manifest.
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 1
- direct_boolean_assertions_max: 1
- preferred_assertion_styles: dict equality on full regenerated `/app/output/report.json` versus oracle-shaped expectations.
- forbidden_assertion_styles: scenario-to-key answer grids in instruction text.

### category_profile
- challenge_family: debugging
- profile_name: debugging_cpp_repair
- allowed_instruction_disclosures: absolute paths, JSON key names, scenario knob `JOURNAL_AUDIT_SCENARIO`, timer floor, modulo-seven lane sum rule, verifier rebuild commands.
- forbidden_instruction_leaks: exact file/function patch recipes, answer-key tables, bolded thresholds tied to single edits.
- category_specific_hardness_bar: Agents must align three translation units without naming the fix sites.
- category_specific_verifier_risks: Verifier rebuilds must stay deterministic; no wall-clock assertions.
- coverage_role: Exercises mux bitmap completion, lane timing plus residue, and rank arbitration across profiles.

### difficulty_mechanism_plan
- mechanisms: buried_local_constraints, stateful_multi_step_dependencies, rare_local_vocabulary, cross_file_cross_format_invariants
- adversarial_layers_count: 4
- fairness_guardrails: No timing-as-hardness; NOP baseline stays failing; oracle stays deterministic.

### calibration_plan
- oracle_runs: 1x mean 1.0 for final evidence; 10x repeat for flakiness gate.
- no_op_runs: 1x mean 0.0 baseline.
- target_agent_runs: platform trials recorded outside this repo.
- comparator_agent_runs: not used for this task.
- human_sanity: first-look dry run on instruction plus environment listing only.
- shortcut_audit: agents that only rewrite JSON or tweak literals without rebuilding must fail pytest.
- ablation_plan: flipping-point contract documents single-location revert subsets per gate runbook.
- pass_rate_target: oracle 100 percent on shipped verifier; agents expected hard with partial credit off-repo.

### verifier_scoring_plan
- metrics: functional_correctness weight 0.45; hidden_invariants weight 0.2; state_hygiene weight 0.1; interface_correctness weight 0.15; deliverable_completeness weight 0.1
- overall_threshold: binary reward 1 only if all pytest cases pass.
- reward_output: `/logs/verifier/reward.txt` with 0/1 footer per template.
- binary_threshold_rule: single failed assertion fails the suite.

### subtype_milestone_plan
- subcategories: none beyond standard Edition 2 metadata.
- milestone_count: 0
- sequential_dependency: none
- local_only_data: corpus JSON and CMake sources under `environment/` only.
- sidecar_or_protocol_notes: single-container compose per Harbor template.

### satisfiability_risk
- rc2_planned_name_risk: Mitigated by opaque stems, decoys, and task_files listing helpers explicitly.
- gx9_contract_risk: Boolean keys are product-shaped audit flags; instruction documents schema without enumerating per-profile truth tables.
- cr1_symbol_frontier_risk: Symbol table lists three top-level symbols; helpers declared in task_files.
- hidden_contract_risk: Lane residue rule and verifier commands live in instruction.md, not only tests.

### actionability_plan
- verifier_command_visible: `/app/tests/test.sh` runs `cmake -S /app -B /app/build`, `cmake --build /app/build -j2`, then `pytest` on `/tests/test_outputs.py` with `--ctrf` logging.
- source_fix_intent_visible: Implementation under `/app/environment` must be repaired so `/app/bin/journal_run` regenerates JSON.
- generated_output_rule_visible: Hand-authored `/app/output/report.json` is rejected; rewards require pipeline output.
- exact_formula_home: Lane gate documents sub-ninety-millisecond rejection and unsigned byte-sum congruent to three modulo seven alongside mux completion and fold rank semantics.
- schema_home: Structured JSON report keys and types are mirrored from `output_contract.toml` into `instruction.md` without repeating verdict-shaped spellings here.

### waiver_plan
- waivers_expected: none for collapse WARN band on legacy manifest absence; justify in Step 3b notes if needed.
- waiver_rationale: N/A unless platform requests a waivable hygiene exception.

### reference_pattern
- justification_if_none: No promoted reference in `docs/reference_tasks/index.json` matches this C++/CMake audit task; calibration is documented independently.

### realism_source
- source_type: synthetic_exception
- evidence_basis: Composed from internal multi-module audit patterns without cloning a single external bug report.
- upstream_or_synthetic_rationale: Vectors and thresholds are minimized to what the verifier asserts while keeping cross-module coupling.
- minimization_preserves: Frozen lane snapshots, mux edge refresh, and fold arbitration semantics exercised by pytest.
- synthetic_exception_review: Reviewer confirmed no live PII or proprietary payloads; difficulty comes from coupling, not data sensitivity.

### Triviality Ledger
- Widening the fast aggregate window alone cannot pass: fold tie policy and mux invalidation tests still fail until coordinated.
- Editing only the merge layer cannot pass: bookmark edge omission and shallow-green tests remain red until mux and gate logic align.
- Naive “mark everything dirty” in mux risks failing cold-start equivalence encoded in triad C unless fold pairing remains legal—forces coupled reasoning rather than blunt invalidation.

### Per-gate Pitfall Inventory
- RC1–RC3 / CR*: Spread substantive edits across `runtime/src/mux_slice.cpp`, `ops/src/replay_gate.cpp`, and `persist/src/wal_fold.cpp`; avoid one-file oracle rewrites.
- RC6 / GX9 / GX10: Keep instruction free of algorithm enumerations, answer-key clauses, and polarity contradictions; symptoms and outcomes only.
- RC7 / GX3: Oracle must encode real cross-module coordination (target GX3 edit-distance band), not inflated heredocs with trivial deltas.
- GX1 / GX4 / GX5: Strip corrective vocabulary from env comments; keep derivation of expected values in env C++, not prose or tests alone.
- GX2: Avoid bulk replace templates whose semantic delta is near-zero.
- Static / metadata: Ensure `task.toml` and package lists remain schema-complete when Step 2b authors wire the task folder.

### Initial Draft Commitments
- `tasks/journal-replay-divergence/task.toml`
- `tasks/journal-replay-divergence/output_contract.toml`
- `tasks/journal-replay-divergence/instruction.md`
- `tasks/journal-replay-divergence/tests/test.sh`
- `tasks/journal-replay-divergence/tests/test_outputs.py`
- `tasks/journal-replay-divergence/solution/solve.sh`
- `tasks/journal-replay-divergence/solution/oracle.patch`
- `tasks/journal-replay-divergence/solution/reference/mux_slice.cpp`
- `tasks/journal-replay-divergence/solution/reference/wal_fold.cpp`
- `tasks/journal-replay-divergence/solution/reference/replay_gate.cpp`
- `tasks/journal-replay-divergence/environment/CMakeLists.txt`
- `tasks/journal-replay-divergence/environment/Dockerfile`
- `tasks/journal-replay-divergence/environment/config/runtime.toml`
- `tasks/journal-replay-divergence/environment/config/probe.toml`
- `tasks/journal-replay-divergence/environment/runtime/include/mux_types.hpp`
- `tasks/journal-replay-divergence/environment/runtime/include/envelope.hpp`
- `tasks/journal-replay-divergence/environment/runtime/src/mux_slice.cpp`
- `tasks/journal-replay-divergence/environment/runtime/src/mux_clamp.cpp`
- `tasks/journal-replay-divergence/environment/ops/include/replay_gate.hpp`
- `tasks/journal-replay-divergence/environment/ops/include/audit_vectors.hpp`
- `tasks/journal-replay-divergence/environment/ops/src/replay_gate.cpp`
- `tasks/journal-replay-divergence/environment/ops/src/audit_lane_cells.cpp`
- `tasks/journal-replay-divergence/environment/ops/src/audit_triad_a.cpp`
- `tasks/journal-replay-divergence/environment/ops/src/audit_triad_b.cpp`
- `tasks/journal-replay-divergence/environment/ops/src/audit_triad_c.cpp`
- `tasks/journal-replay-divergence/environment/ops/src/lane_probe.cpp`
- `tasks/journal-replay-divergence/environment/ops/src/replay_scan.cpp`
- `tasks/journal-replay-divergence/environment/persist/include/fold_contract.hpp`
- `tasks/journal-replay-divergence/environment/persist/include/wal_types.hpp`
- `tasks/journal-replay-divergence/environment/persist/src/audit_fold_cells.cpp`
- `tasks/journal-replay-divergence/environment/persist/src/wal_fold.cpp`
- `tasks/journal-replay-divergence/environment/runtime/src/audit_mux_cells.cpp`
- `tasks/journal-replay-divergence/environment/tools/audit/scan_cli.cpp`
- `tasks/journal-replay-divergence/environment/fixtures/corpus/case_a.json`
- `tasks/journal-replay-divergence/environment/fixtures/corpus/case_b.json`
- `tasks/journal-replay-divergence/environment/fixtures/corpus/case_c.json`
- `tasks/journal-replay-divergence/environment/fixtures/corpus/case_d.json`
- `tasks/journal-replay-divergence/environment/schema/layout.toml`
- `tasks/journal-replay-divergence/environment/config/audit_profiles.toml`
- `tasks/journal-replay-divergence/environment/docs/replay_audit_contract.md`
- `tasks/journal-replay-divergence/environment/docs/overview.txt`
- `tasks/journal-replay-divergence/environment/docs/build_matrix.txt`
- `tasks/journal-replay-divergence/environment/config/ci_profile.toml`
- `tasks/journal-replay-divergence/environment/schema/version_stamp.toml`
- `tasks/journal-replay-divergence/environment/runtime/abi_notes.txt`
- `tasks/journal-replay-divergence/environment/ops/callgraph_stub.txt`
- `tasks/journal-replay-divergence/environment/persist/storage_layout.txt`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
- path: environment/runtime/src/mux_slice.cpp
  symbol: qz_ty7
  kind: function
  signature: void qz_ty7(uint64_t x0, std::span<const std::byte> x1)
  purpose: merges incoming staged bytes into the handoff bitmap before the next fold step
- path: environment/ops/src/replay_gate.cpp
  symbol: pl_n4
  kind: function
  signature: bool pl_n4(std::chrono::milliseconds x0, std::span<const uint8_t> x1)
  purpose: computes the fast aggregate used for health signaling in the audit driver
- path: environment/persist/src/wal_fold.cpp
  symbol: kx_f2
  kind: function
  signature: std::vector<std::byte> kx_f2(const std::vector<std::byte>& x0, const std::vector<std::byte>& x1)
  purpose: folds paired captured views into the persisted canonical projection

#### flipping_point_contract
locations:
  - id: A
    path: environment/runtime/src/mux_slice.cpp
    controls_tests: [test_qz_m7_emit, test_triad_q8a]
  - id: B
    path: environment/ops/src/replay_gate.cpp
    controls_tests: [test_pl_n4_pair, test_triad_pl8b]
  - id: C
    path: environment/persist/src/wal_fold.cpp
    controls_tests: [test_kx_f2_cycle, test_triad_kx8c]
no_single_location_flips_majority: true
concentration_cap: 0.5

#### decoy_manifest
- path: environment/runtime/src/mux_clamp.cpp
  kind: module
  rhymes_with: qz_ty7
  non_fix_purpose: bounds-checks unrelated staging buffers for a legacy ingest path that never hits resume boundaries in tests
- path: environment/runtime/src/audit_mux_cells.cpp
  kind: module
  rhymes_with: qz_ty7
  non_fix_purpose: closure-bit probe isolated from lane/fold cells; not a fix site
- path: environment/ops/src/replay_scan.cpp
  kind: helper
  rhymes_with: pl_n4
  non_fix_purpose: performs deterministic byte-range scans for diagnostics without participating in the fast aggregate path
- path: environment/ops/src/lane_probe.cpp
  kind: helper
  rhymes_with: pl_n4
  non_fix_purpose: even-millisecond window probe retained for tooling parity; not wired into journal_run emit
- path: environment/ops/include/audit_vectors.hpp
  kind: module
  rhymes_with: run_audit_emit
  non_fix_purpose: probe API declarations; profile wiring stays in replay_gate.cpp
- path: environment/ops/src/audit_lane_cells.cpp
  kind: module
  rhymes_with: pl_n4
  non_fix_purpose: scenario lane byte spans; profile wiring stays in replay_gate.cpp
- path: environment/ops/src/audit_triad_a.cpp
  kind: module
  rhymes_with: qz_ty7
  non_fix_purpose: combined mux-and-fold triad probe for default/mixed profiles
- path: environment/ops/src/audit_triad_b.cpp
  kind: module
  rhymes_with: pl_n4
  non_fix_purpose: combined mux-and-lane triad probe for mixed profile
- path: environment/ops/src/audit_triad_c.cpp
  kind: module
  rhymes_with: kx_f2
  non_fix_purpose: combined fold-and-lane triad probe for asymmetric profile
- path: environment/persist/src/audit_fold_cells.cpp
  kind: module
  rhymes_with: kx_f2
  non_fix_purpose: rank-pick pairs for default and mixed profiles; not a fix site

#### code_forbidden_tokens
code_forbidden_tokens: [daemon, events, bundle, captures, process, restarts, staff, bookmark, probes, stages, digests, baselines, payloads, implementation, agreement, projections, aids, derivation, continuity, gaps, walks]
