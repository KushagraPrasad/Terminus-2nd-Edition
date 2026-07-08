### Decision

GO — Step 2a spec for FFT Resume Corruption seed (cached transform divergence). Rust Cargo mirrored replay-lane JSON sweep calibrated from approved krylov-recycle-drift zip with distinct lane labels, instruction framing, and probe_digest.

### Metadata

- version: 2
- Task name: fft-resume-corruption
- Title: FFT Resume Corruption
- Category: debugging
- Languages: [rust, bash]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: [rust, cargo-workspace, fft-replay, json-report, cache-lineage]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do not leak oracle ordering, patch hunks, or exact per-field answer tables.

### Public contract

The eventual `instruction.md` describes observable drift: FFT checkpoint restores look healthy while parallel replay workers diverge on mixed-generation transform caches; paired replay lanes disagree on closure fields and lane stamps while summaries can look mostly repaired; the solver must repair Rust sources under `/app` so `cargo` plus the `ab` driver regenerate `/app/output/sweep_report.json`. Tests rebuild from current sources, rerun the binary, and validate JSON invariants including digest, span, reload label text, mirror pairs, and sixteen-digit stamps. Framing stays symptoms-only and must not name the replay lineage artifact or canonical reconciliation path directly.

### platform_files

- path: task.toml
  role: metadata
- path: instruction.md
  role: public prompt
- path: output_contract.toml
  role: authoring output declaration
- path: tests/test.sh
  role: verifier entrypoint
- path: tests/test_outputs.py
  role: pytest contract
- path: solution/solve.sh
  role: oracle driver
- path: environment/Dockerfile
  role: image build
- path: construction_manifest.json
  role: local authoring manifest

### task_files

- path: construction_manifest.json
  role: flipping-point and symbol table for collapse tooling
- path: environment/Cargo.toml
  role: workspace root
- path: environment/w0/v79/src/main.rs
  role: sweep driver and digest contract header
- path: environment/w0/v79/src/wire_inval.rs
  role: invalidation gate combine helper
- path: environment/w0/v79/src/wire_pack.rs
  role: column apply entry
- path: environment/w0/v79/src/wire_stamp.rs
  role: co-resident stamp helper (not a flipping-point owner)
- path: environment/z9/x1/src/hold.rs
  role: pack merge
- path: environment/z9/x1/src/body.rs
  role: co-resident crate glue
- path: environment/z9/x1/src/lib.rs
  role: co-resident crate root
- path: environment/z9/x1/src/shape.rs
  role: co-resident layout helpers
- path: environment/z9/x2/src/tie.rs
  role: stamp reconcile
- path: environment/z9/x2/src/body.rs
  role: co-resident crate glue
- path: environment/z9/x2/src/lib.rs
  role: co-resident crate root
- path: environment/z9/x2/src/stamp_help.rs
  role: co-resident stamp utilities
- path: environment/docs/replay_lane_ids.txt
  role: comma-separated replay lane ids
- path: environment/docs/build_hints.txt
  role: verifier argv notes

### fix_frontier

- count: 4
- distribution: `z9/x1`, `z9/x2`, and two modules under `w0/v79/src` share the oracle diff; `core_mesh` supplies numeric scaffolding only.
- naming_policy: Keep neutral Rust identifiers already in tree; parameters avoid instruction metaphor stems listed under forbidden_stems.
- forbidden_stems: fft resume corruption, lineage artifact, reconciliation path, harbor, oracle, patch, tb3bench, transform cache divergence
- helpers_policy: Co-resident helpers include the w0 stamp helper module, both x1 and x2 crate body and lib entrypoints, and shape helpers adjacent to the merge crate; they are read-only context for diagnosis and are not flipping-point owners.
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: digest recomputation from rows, pair equality on stamps and closure booleans read from JSON, integer span from closure code magnitudes
- forbidden_assertion_styles: replay-lane to field to expected literal tables, golden JSON fixtures under environment/

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis across merge, stamp, invalidation gate, and column-apply boundaries after checkpoint rollback and parallel replay
- collapse_risk: static JSON writes, stale prebuilt binary reuse, validating output ranges without generation lineage

### category_profile

- challenge_family: FFT checkpoint replay coherence after parallel transform resume
- bug_family: stale transform caches trusted over rebuilt replay state
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: Build and run commands, output path, JSON top-level shape, replay lane id file path, pointer to module header for formulas, mirror pair tokens, static-output rejection, noop argv anchor text.
- forbidden_instruction_leaks: Exact hunk ordering, internal crate rename map, hidden alternate entrypoint, naming the replay lineage artifact or canonical reconciliation path.
- category_specific_hardness_bar: Close numeric subspace and stamp ordering without naming the defect class.
- category_specific_verifier_risks: Skipping rebuild inside pytest, hand-written JSON.
- coverage_role: Rust workspace repair depth under debugging.

### satisfiability_risk

- rc2_planned_name_risk: Low when forbidden stems avoid new identifiers and docs use `replay_lane_ids.txt` naming.
- gx9_contract_risk: Low when spec avoids answer recital tables and relies on header plus instruction prose for boolean semantics.
- cr1_symbol_frontier_risk: Low when helpers_policy lists all co-resident modules adjacent to the frontier.
- hidden_contract_risk: Medium unless `main.rs` header documents digest and span rules tested verbatim.

### actionability_plan

- verifier_command_visible: Instruction cites `cargo` profile hints in `/app/docs/build_hints.txt`, `/app/target/release/ab`, pytest path, optional noop argv line.
- source_fix_intent_visible: Instruction states Rust implementation must be repaired and static JSON rejected.
- generated_output_rule_visible: Instruction states output must be regenerated through the build and driver pipeline.
- exact_formula_home: `environment/w0/v79/src/main.rs` module-level doc comment defines digest reduction and span rule.
- schema_home: Instruction names top-level JSON sections; per-field names live in code header and `output_contract.toml`.

### waiver_plan

- waivers_expected: no
- waiver_rationale: Collapse WARN band is reviewer-documented; no mechanical waivers unless policy shifts.

### reference_pattern

- justification_if_none: No promoted reference in docs/reference_tasks/index.json matches this Rust Cargo mirrored replay-lane JSON sweep; calibration follows the approved krylov-recycle-drift zip mold with FFT checkpoint replay framing, distinct lane labels, and probe_digest.

### realism_source

- source_type: synthetic_exception
- evidence_basis: Composed from FFT checkpoint / transform-cache divergence patterns minimized into a deterministic numeric driver.
- upstream_or_synthetic_rationale: Synthetic without live services; reproduces cached transform divergence class from FFT Resume Corruption seed.
- minimization_preserves: Mirror disagreement, digest sensitivity, rebuild requirement.
- synthetic_exception_review: Captured only in this Reviewer Appendix.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, cross_file_cross_format_invariants, buried_local_constraints, stateful_multi_step_dependencies
- adversarial_layers_count: 4
- fairness_guardrails: Deterministic builds, no verifier network, formulas visible in header or instruction.
- mechanism: false_green_intermediate_states
  placement: checkpoint restores pass local replay checks while rows still disagree on replay.
  why_model_misses_it: agents stop after partial JSON tweaks.
  fairness_guardrail: tests rebuild and run the release binary each time.
- mechanism: cross_file_cross_format_invariants
  placement: numeric closure ties to stamp monotonicity and per-step masks across crates.
  why_model_misses_it: single-file edits fix one symptom and break digest.
  fairness_guardrail: digest recomputed in tests from visible rules.
- mechanism: buried_local_constraints
  placement: pack merge branch when stamp bands change after rollback across mixed checkpoint generations.
  why_model_misses_it: obvious conditional edits miss paired effects.
  fairness_guardrail: mirror pairs amplify divergence.
- mechanism: stateful_multi_step_dependencies
  placement: driver consumes ordered tuples; terminal state feeds residual check.
  why_model_misses_it: parallel replay reordering shifts digest without compile failures.
  fairness_guardrail: tuples are fixed in source.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: one engineer can pass with Rust tooling and the module header.
- shortcut_audit: static JSON, test-only edits, doc-only edits, skipping `cargo` in verifier.
- ablation_plan: drop each manifest hunk class and confirm targeted tests fail.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=target agent trials

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when every pytest test passes.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step task.
- local_only_data: true
- sidecar_or_protocol_notes: none; Rust workspace only.

### Failure topology

FFT checkpoint replay advances a family index while the merge pack, stamp reconcile, invalidation gate, and column apply paths interact. Transform caches can survive rollback replay across mixed checkpoint generations; partial repairs leave mirror replay pairs diverged or digest inconsistent while surface stability checks still look green.

### Environment shape

Rust workspace under `environment/` with `z9` crates and `w0/v79` binary `ab`, plus `data/` and `docs/` fixtures. No auxiliary services.

### Required artifacts

Canonical single-step layout including `construction_manifest.json` mirroring the manifest section below.

### Test plan

- test_report_rows_and_scenario_table
- test_paired_mirror_agreement
- test_all_closure_flags_and_tilt_code_zero
- test_summary_reload_status_aligned
- test_generation_span_matches_tilt_codes
- test_probe_digest_matches_driver_contract
- test_probe_digest_matches_known_good_output
- test_hex_field_width
- test_summary_rows_total_integer
- test_pipeline_overwrites_hand_written_json
- test_consecutive_pipeline_runs_are_identical
- test_radix_row_reacts_to_driver_plan_edit
- test_b_lineage_fix_required_for_coherent_emission
- test_joint_cache_fixes_jointly_required_for_pipeline
- test_invalidation_gate_fix_required_for_closure_flags

### Drafting guardrails

Keep instruction symptoms-only; keep `/bin/true` noop wording synchronized with `tests/test_outputs.py` and `build_hints.txt`.

### Triviality Ledger

- Hand-writing JSON fails digest and rebuild tests.
- Doc-only header edits without code fail closure tests.
- Single-crate edits fail mirror or digest subsets.

### Per-gate Pitfall Inventory

- RC6/GX9: avoid answer tables; keep dense identifiers in code header, not instruction.
- RC7/GX3: oracle patch stays substantive across four files.
- Static checks: preserve `tests/test.sh` template; Dockerfile exposes `python3` for oracle snippet.
- Collapse WARNs: borderline oracle LOC and concentration documented for Step 3b.

### Initial Draft Commitments

- instruction.md
- task.toml
- output_contract.toml
- construction_manifest.json
- tests/test.sh
- tests/test_outputs.py
- solution/solve.sh
- solution/oracle.patch
- environment/Dockerfile
- environment/Cargo.toml
- environment/Cargo.lock
- environment/w0/v79/src/main.rs
- environment/w0/v79/src/wire_inval.rs
- environment/w0/v79/src/wire_pack.rs
- environment/w0/v79/src/wire_stamp.rs
- environment/z9/x1/src/hold.rs
- environment/z9/x2/src/tie.rs
- environment/docs/replay_lane_ids.txt
- environment/docs/build_hints.txt

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: environment/z9/x1/src/hold.rs
  symbol: merge_pack
  kind: function
  signature: "pub fn merge_pack(state: &mut PackState, stamp_a: u64, stamp_b: u64, dim_m: usize, incoming: &[[f64; 4]; 3]) -> [[f64; 4]; 3]"
  purpose: Merge incoming columns into pack state across stamp transitions.
- path: environment/z9/x2/src/tie.rs
  symbol: reconcile_b
  kind: function
  signature: "pub fn reconcile_b(step_ix: usize, family_ix: u32, prev_family: u32) -> u64"
  purpose: Combine step and family indices into a stamp ordering key.
- path: environment/w0/v79/src/wire_inval.rs
  symbol: wire_combine
  kind: function
  signature: "pub fn wire_combine<F: FnMut(), G: FnMut()>(side: F, gate: G) -> u32"
  purpose: Combine side effects with gate callback to produce per-step mask bits.
- path: environment/w0/v79/src/wire_pack.rs
  symbol: apply_columns
  kind: function
  signature: "pub fn apply_columns(pack: &mut PackState, tag_a: u64, tag_b: u64, incoming: &[[f64; 4]; 3]) -> [[f64; 4]; 3]"
  purpose: Entry that forwards into merge after tag mixing work.

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/z9/x1/src/hold.rs
    controls_tests: [test_paired_mirror_agreement, test_generation_span_matches_tilt_codes]
  - id: B
    path: environment/z9/x2/src/tie.rs
    controls_tests: [test_hex_field_width, test_probe_digest_matches_known_good_output]
  - id: C
    path: environment/w0/v79/src/wire_inval.rs
    controls_tests: [test_all_closure_flags_and_tilt_code_zero, test_summary_reload_status_aligned]
  - id: D
    path: environment/w0/v79/src/wire_pack.rs
    controls_tests: [test_probe_digest_matches_driver_contract, test_report_rows_and_scenario_table, test_summary_rows_total_integer]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

- path: environment/z9/x3/src/catalog.rs
  kind: module
  rhymes_with: label tables
  non_fix_purpose: Static label table for tooling; not on the numeric fix path.
- path: environment/z9/core_mesh/src/mesh.rs
  kind: module
  rhymes_with: merge_pack
  non_fix_purpose: Shared numeric mesh helpers reused across runs.

#### code_forbidden_tokens

```
code_forbidden_tokens: [lineage_artifact, reconciliation, harbor, tb3bench, fft_resume_corruption, transform_cache_divergence]
```

## Reviewer Appendix

Seed: option_a_step2a_ready_seed_bank.md § FFT Resume Corruption (cached transform divergence; trajectory=Coherence; cluster=Complex-System-Builds).
