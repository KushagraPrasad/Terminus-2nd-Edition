### Decision

GO — Attempt 2. Fixed contract_surface array types in evidence JSON; retained four-root Cargo workspace constrained-build topology with weak-dep fold, path-edge leak, cross-format dep-info bridge, permuted first-build order driver, false-green health probe, and perm_order generalization.

### Metadata

- version: 2
- Task name: cargo-workspace-feature-unification-order
- Title: Workspace feature unification
- Category: software-engineering
- Task shape: constrained_build
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["rust", "cargo-workspace", "feature-unification", "resolver-v2", "build-order", "false-green", "offline-build"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, per-scenario answer tables, or narrative causal chains that name fix coordinates.

### Public contract

Complete the offline `/app/bin/fm_run` feature-matrix driver for the Cargo workspace under `/app/environment` so shared dependency features unify consistently regardless of which workspace member triggers the first build.

Public obligations live in `/app/environment/docs/formal_rules.md`.

The feature unification contract requires five coupled outcomes:

1. **Order independence** — permuted first-build member sequences must yield identical unified feature fingerprints for each shared path dependency.
2. **Mirror targets** — each primary member target must agree with its echo twin on sixteen-digit facet material and three closure counters in the emitted report.
3. **Cross-artifact binding** — JSON report rows must match rustc dep-info feature tokens and captured metadata sidecars under `/app/output/meta/` for the same build order seed.
4. **Offline rebuild** — all checks use the locked offline Cargo workflow only; live registry access is unsupported.
5. **Recovery** — after destructive clean drills encoded in `/app/environment/data/perm_seq.toml`, rerunning the documented workflow must converge to the same terminal matrix outcome.

Run the locked build workflow and driver as documented to emit `/app/output/feature_matrix_report.json`, trace files under `/app/output/run_traces/`, and refreshed metadata sidecars. Row and summary shapes are defined in `formal_rules.md`. Primary target ids are in `/app/environment/docs/tgt_ids.txt`; operator argv patterns are in `/app/environment/docs/operator_cmds.txt` (environment-specific CLI semantics for phased replay hooks).

Mirror pairs bind `alpha` with `alpha_echo`, `beta` with `beta_echo`, and `gamma` with `gamma_echo`. Coherent runs keep per-row lag at zero on every row, `feat_rc`, `dep_rc`, and `ord_rc` at `1` on all rows, matching sixteen-digit `facet_hex` on each mirror pair, `sync_label` reading `settled`, and summary `matrix_digest` matching the reduction documented in the module comment above `/app/environment/h5k/src/main.rs`. The module comment defines `span_band` and `matrix_digest`; read it instead of hand-writing JSON.

**Generalization:** A correct implementation must survive every permutation scenario encoded in `/app/environment/data/perm_seq.toml`. Instruction names the file and the generalization rule only—not individual held-out rows or per-target facet answers.

Complete Rust modules and workspace manifests under `/app/environment` so driver output and module behavior satisfy all contract properties. Rebuild `/app/bin/fm_run` from modified sources per `formal_rules.md` before validating. Static or manual JSON writes are insufficient; copying outputs without the normal driver pipeline will not pass.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "software-engineering"`
- path: instruction.md
  role: natural public design-brief prompt (mirrors Public contract above)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation, permutation, and pipeline traps
- path: solution/solve.sh
  role: oracle applying coordinated multi-module fix
- path: environment/Dockerfile
  role: build definition; pre-install pinned rustc/cargo, pytest, tmux, asciinema, and locked deps
- path: construction_manifest.json
  role: local authoring artifact mirroring Construction manifest below

### task_files

- path: environment/w2k/src/seed_mux.rs
  role: oracle frontier A — weak dependency feature fold
- path: environment/w2k/src/stub_help.rs
  role: decoy weak-edge logger (non-fix)
- path: environment/w2k/src/lib.rs
  role: w2k crate root exports
- path: environment/p3n/src/lane_mux.rs
  role: oracle frontier B — path dependency edge normalization
- path: environment/p3n/src/lane_help.rs
  role: decoy path table pretty-printer (non-fix)
- path: environment/p3n/src/lib.rs
  role: p3n crate root exports
- path: environment/c8r/src/row_mux.rs
  role: oracle frontier C — JSON row vs dep-info sidecar bridge
- path: environment/c8r/src/byte_help.rs
  role: decoy byte scan helper (non-fix)
- path: environment/c8r/src/lib.rs
  role: c8r crate root exports
- path: environment/h5k/src/slot_mux.rs
  role: oracle frontier D — first-build sequence permutation driver
- path: environment/h5k/src/main.rs
  role: fm_run entry and matrix_digest reduction header
- path: environment/engine/src/orch_v2.rs
  role: multi-phase fm_run orchestration
- path: environment/engine/src/tbl_r9.rs
  role: workspace metadata table reader
- path: environment/engine/src/ph_seed.rs
  role: weak-fold phase wiring
- path: environment/engine/src/ph_lane.rs
  role: path-edge phase wiring
- path: environment/engine/src/ph_row.rs
  role: dep-info fold phase wiring
- path: environment/engine/src/mini_sha.rs
  role: offline digest helper
- path: environment/engine/src/mini_toml.rs
  role: offline toml parse helper
- path: environment/engine/src/lib.rs
  role: engine crate root exports
- path: environment/engine/src/view_mux.rs
  role: false-green health/status subcommand surface
- path: environment/members/a1/src/lib.rs
  role: alpha library surface
- path: environment/members/b2/src/lib.rs
  role: beta library surface
- path: environment/members/g3/src/lib.rs
  role: gamma library surface
- path: environment/k9m/s4/src/lib.rs
  role: common dependency crate feature gates
- path: environment/docs/formal_rules.md
  role: formal properties, schema references, build/replay commands
- path: environment/docs/tgt_ids.txt
  role: primary target id table (held-out permutations excluded)
- path: environment/docs/operator_cmds.txt
  role: operator argv patterns for fm_run hooks
- path: environment/data/perm_seq.toml
  role: held-out first-build permutation scenario table
- path: environment/data/edge_seed.toml
  role: weak and strong edge seed rows
- path: environment/data/ladder.toml
  role: feature ladder weights for sensitivity drills
- path: environment/schemas/row_v4.schema.json
  role: feature_matrix_report row shape

### fix_frontier

- count: 5
- distribution: `environment/w2k/src/seed_mux.rs`, `environment/p3n/src/lane_mux.rs`, `environment/c8r/src/row_mux.rs`, `environment/h5k/src/slot_mux.rs`, `environment/engine/src/view_mux.rs` (distinct roots w2k, p3n, c8r, h5k, engine)
- naming_policy: Opaque identifiers (`fn_w2`, `fn_p3`, `fn_c8`, `fn_h5`, `emit_status_view`) on neutral parameter names; no instruction nouns on fix path
- forbidden_stems: feature, unification, order, workspace, member, dependency, resolver, matrix, mirror, pairs, coherent, facet, digest, sync, permutation, audit, driver, offline, locked, metadata, sidecar, binding, fingerprint, sequence, trigger, obligation, contract, independence, permute, settled, generalization, scenario, alpha, beta, gamma, echo, lag, closure, counter, hexadecimal, regenerating, manifests, emitted, refreshed, captured, agreement, identical, unified, consistently, regardless, primary, twin, targets, shapes, summary, rows, documented, cross-artifact, dep-info, tokens, workflow, reduction, survives, first-build, sidecars, fingerprints, perm_seq, fm_run, feature_matrix_report, matrix_digest, sync_label, facet_hex, feat_rc, dep_rc, ord_rc, tgt_ids, operator_cmds, formal_rules, run_traces
- helpers_policy: Decoys in w2k and p3n perform credible adjacent diagnostics; frontier stays thin at five symbols with orchestration wiring separate
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: regenerated JSON rows, integer rc counters, derived matrix_digest, mirror echo equality, perm_seq traps, ablation incoherence, pipeline overwrite, dep-info byte cross-check
- forbidden_assertion_styles: scenario-key expected tables in instruction.md; static golden feature_matrix_report under tests/; readiness fields named `*_ok` in instruction prose tied 1:1 to fix-path grep

### task_shape

- type: constrained_build
- instruction_framing: design-brief
- hardness_source: design search across coupled Cargo workspace feature resolution under permuted first-build order
- collapse_risk: blank-canvas build with no binding cross-component constraints

### category_profile

- challenge_family: cargo workspace feature resolution
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: locked offline Cargo commands, feature_matrix_report artifact identity, perm_seq generalization rule, mirror pair coherence predicates, operator_cmds argv, formal_rules schema, matrix_digest formula home in main.rs header
- forbidden_instruction_leaks: weak-vs-strong fold site, path-edge leak location, workspace resolver override wiring, patch functions, per-scenario facet answers, canonical recovery sequence
- category_specific_hardness_bar: Lockfile, workspace manifests, common path-dep feature table, sequence driver, dep-info sidecars, and cache-visible probes must coordinate; one version bump or one manifest row cannot pass ablation and perm_seq suites
- category_specific_verifier_risks: pin-one-dep fix, clean-build-only pass, static JSON satisfying format without rebuild, false-green health subcommand without durable sidecar convergence
- coverage_role: Strengthens build_dependency_toolchain coverage via cargo workspace feature unification order constrained-build topology

### difficulty_mechanism_plan

- mechanisms: deceptive_but_valid_local_evidence, false_green_intermediate_states, cross_file_cross_format_invariants, rollback_recovery_requirements, stateful_multi_step_dependencies
- adversarial_layers_count: 5
- fairness_guardrails: Public contract states every externally tested phase outcome, schema, and command without naming fix-path symbols or construction recipes; deceptive layers remain discoverable from traces, meta sidecars, and ablation flips
- mechanism: deceptive_but_valid_local_evidence
  placement: environment/engine/src/view_mux.rs health/status subcommand
  why_model_misses_it: models trust settled sync_label from fm_run probe while durable dep-info sidecars and mirror pairs still disagree under permuted first-build order
  fairness_guardrail: instruction names cross-check against metadata sidecars; test_q19_premature requires terminal convergence with matching matrix_digest
- mechanism: false_green_intermediate_states
  placement: environment/c8r/src/byte_help.rs intermediate row material before dep-info commit
  why_model_misses_it: models declare report complete when JSON rows look well-formed but dep-info tokens still diverge
  fairness_guardrail: verifier requires terminal pipeline rerun and test_q10_rerun_flow overwrites hand-written JSON
- mechanism: cross_file_cross_format_invariants
  placement: environment/c8r/src/row_mux.rs JSON rows tied to /app/output/meta/*.dep-info bytes
  why_model_misses_it: models fix JSON emitters without reconciling rustc metadata sidecar feature tokens
  fairness_guardrail: instruction names cross-artifact binding obligation; tests recompute digests from visible formula home
- mechanism: rollback_recovery_requirements
  placement: environment/engine/src/orch_v2.rs destructive clean step before perm_seq replay
  why_model_misses_it: models repeat destructive cargo clean without idempotent journal reconstruction, passing happy path only
  fairness_guardrail: formal_rules.md documents idempotent recovery rerun; perm_seq drills require same terminal matrix_digest after recovery
- mechanism: stateful_multi_step_dependencies
  placement: environment/h5k/src/slot_mux.rs permuted first-build sequences across members a1/b2/g3
  why_model_misses_it: models stop after first member builds green without finishing full order permutation closure required for build/CI failure recovery under varying cache warm states
  fairness_guardrail: operator_cmds lists required argv sequence; each order seed appends trace rows verified by test_q20_hook_flow

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert Rust build engineer reproduces incoherent feature_matrix_report under stock scaffold, applies coordinated four-module fix, reruns fm_run offline across perm_seq seeds to settled convergence
- shortcut_audit: block hardcoded feature_matrix_report.json, test edits, stale-doc-only changes, single-member default-features tweak, wrapper-only view_mux patch
- ablation_plan: remove deceptive probe layer, then weak fold, then path-edge normalization, then order driver—each ablation should drop pass rate materially
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=aligns with Part E Hard/Medium/Easy thresholds on worst-model accuracy; verifier-offline: pytest and cargo baked in Dockerfile with tests/test.sh using no runtime apt/pip/curl; post-upload difficulty classification runs only after successful agent+verifier cycles per PLATFORM_AUTO_EVAL.md

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward 1 only when all weighted metrics pass; any ablation flip or pipeline trap failure yields 0

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: single-container local verifier only; offline Cargo with pinned fixtures under environment/data/fix_stash if needed

### satisfiability_risk

- rc2_planned_name_risk: low — opaque crate roots h5k/p3n/w2k/c8r and neutral fn_* symbols committed
- gx9_contract_risk: low — tests derive verdicts from matrix_digest recompute and mirror equality, not per-target answer tables in instruction
- cr1_symbol_frontier_risk: low — four substantive Rust modules plus explicit flipping-point contract
- hidden_contract_risk: medium — cross-artifact dep-info invariants live in runtime sidecars; instruction states binding obligation without byte-level recipe

### actionability_plan

- verifier_command_visible: locked cargo build/test workflow and `/app/bin/fm_run` documented in operator_cmds.txt and formal_rules.md
- source_fix_intent_visible: yes — complete sources under `/app/environment` without naming modules
- generated_output_rule_visible: `/app/output/feature_matrix_report.json`, `/app/output/run_traces/`, `/app/output/meta/` sidecars; regeneration required
- exact_formula_home: module comment above `environment/h5k/src/main.rs`
- schema_home: `environment/schemas/row_v4.schema.json` plus formal_rules.md

### waiver_plan

- waivers_expected: false
- waiver_rationale: Hardness from coupled Cargo feature-graph behavior and observation-shaped contracts; deterministic offline rebuilds avoid harness brittleness waivers

### reference_pattern

- justification_if_none: No promoted entry in `docs/reference_tasks/index.json` matches cargo workspace feature unification under resolver-2 weak-dep semantics with permuted first-build order. Incremental-build and hermetic-sandbox molds share verifier trap patterns but differ in topology; this spec commits a distinct four-root Rust/Cargo workspace design without cloning a reference task file tree.

### realism_source

- source_type: real_system
- evidence_basis: open-source issue
- upstream_or_synthetic_rationale: Minimized from production Cargo/Rust workspace resolver-2 discussions where weak dependency features, default-features=false members, and workspace-level resolver settings yield order-dependent unified feature sets
- minimization_preserves: Weak-vs-strong unification split, path-dep feature leak despite default-features disable, workspace-root resolver precedence over member tables, false-green cargo check-style probes, cross-format JSON vs dep-info invariants
- synthetic_exception_review: not required

### Failure topology

Local health probes and intermediate JSON rows can read settled while unified feature fingerprints still drift when workspace members build in different first-build orders. Resolver-2 weak dependency edges can activate feature tokens through a different path than strong dependency edges, so identical feature names in manifests do not guarantee identical unified sets. A member with default-features disabled can still inherit shared-crate features when a sibling path-dependency edge re-enables them transitively. Workspace-root resolver metadata can override per-member feature tables when the order seed changes, breaking mirror-pair equality and dep-info sidecar agreement. Hardness requires reconciling weak fold, path-edge normalization, cross-format emit, and order-driver scheduling under deterministic offline rebuilds—without the instruction naming which subsystem mis-unifies or which authority wins.

### Environment shape

Rust Cargo workspace rooted at `/app/environment` with opaque crates under `w2k` (weak fold), `p3n` (path edges), `c8r` (cross-format emit), `h5k` (sequence driver), `engine` (orchestration and false-green probe), `members/` (a1, b2, g3), and `k9m/s4` (common path dependency). Seed data in `environment/data/`; operator docs in `environment/docs/`. Single-container only; ≥28 non-Docker environment files committed. Step 2b ships a partial scaffold with broken/incomplete fn_w2, fn_p3, fn_c8, fn_h5 implementations—not a blank canvas.

### Required artifacts

Standard TB3 task tree under `tasks/cargo-workspace-feature-unification-order/`: instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile with locked cargo/pytest/tmux/asciinema, tests/test.sh, tests/test_outputs.py (≥20 tests), solution/solve.sh + oracle.patch, full environment workspace per Initial Draft Commitments.

### Test plan

- test_q1_shape_vecs: JSON layout; primary target ids match tgt_ids.txt
- test_q2_hex_agree: mirror echo targets agree on facet material and rc fields when coherent
- test_q3_rc_all: coherent run — lag zero and three rc fields at 1 on all rows
- test_q4_lbl_set: summary sync_label reads settled when matrix coherent
- test_q5_span_max: span_band equals max abs lag magnitude
- test_q6_dig_reduce: summary matrix_digest matches main.rs header reduction from rows
- test_q7_anchor_hex: matrix_digest matches known-good repaired emission
- test_q8_hex_lower: facet_hex sixteen lowercase hex chars
- test_q9_len_vecs: rows_total integer equals row vector length
- test_q10_rerun_flow: tampered hand-written JSON replaced by pipeline rerun
- test_q11_twice_same: consecutive pipeline runs identical
- test_q12_sens_mut: mutating ladder.toml data changes facet material and digest
- test_q13_flip_w2: reverting fn_w2 weak fold breaks coherence
- test_q14_flip_both: reverting fn_p3 and fn_w2 together breaks pipeline
- test_q15_flip_p3: broken fn_p3 edge wiring + stock lane_help decoy breaks closure
- test_q16_all_perms: every held-out permutation scenario in perm_seq.toml survives after fix
- test_q17_flip_c8: reverting fn_c8 dep-info cross-check breaks dep_rc vs sidecar bytes
- test_q18_reg_first: tbl_r9 durable read precedes runtime probe after profile_a drill
- test_q19_premature: view_mux settled label with disagreeing mirror pairs fails until order permutations finish
- test_q20_hook_flow: operator_cmds argv sequence required for fm_run hook success

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests (cap 0.5).

### Drafting guardrails

Instruction is design-brief complete about report schema, mirror pairs, coherence predicates, cross-artifact binding, and perm_seq generalization—without naming `fn_w2`, `fn_p3`, `fn_c8`, `fn_h5`, weak-vs-strong wiring, path-edge leak site, or workspace metadata override sequence. Ban instruction nouns from fix-path code symbols and test identifiers. No boolean readiness verdict fields in planned outputs. Do not reduce task to blank-canvas spec transcription or single-manifest knob filling.

### Triviality Ledger

- Hand-writing feature_matrix_report.json fails test_q10_rerun_flow because verifier reruns locked cargo + fm_run.
- Fixing only fn_w2 without fn_p3 path-edge normalization fails test_q14_flip_both and mirror coherence subsets.
- Fixing only fn_p3 without fn_w2 weak fold fails test_q15_flip_p3 and test_q16_all_perms.
- Trusting view_mux settled label while mirror pairs disagree fails test_q19_premature until order permutations and dep-info sidecars converge.
- Copying one row from a golden fixture fails test_q7_anchor_hex and test_q12_sens_mut.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle must change semantics in four roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays design-brief without cause-revealing wiring sentences.
- RC5/RC6: schemas and digest home in main.rs header; no boolean answer grid in instruction.
- RC7/GX3: solve.sh coordinated across four modules with substantive bodies (target ≥80 LOC semantic delta).
- GX9/GX10: derived digests and echo equality over scenario boolean tables.
- GX4/GX5: ablation tests patch sources in-container; expectations computed in test file.
- CR1/CR2: honor symbol table and flipping-point concentration cap 0.5.

### Initial Draft Commitments

- tasks/cargo-workspace-feature-unification-order/task.toml
- tasks/cargo-workspace-feature-unification-order/instruction.md
- tasks/cargo-workspace-feature-unification-order/output_contract.toml
- tasks/cargo-workspace-feature-unification-order/construction_manifest.json
- tasks/cargo-workspace-feature-unification-order/tests/test.sh
- tasks/cargo-workspace-feature-unification-order/tests/test_outputs.py
- tasks/cargo-workspace-feature-unification-order/solution/solve.sh
- tasks/cargo-workspace-feature-unification-order/environment/Dockerfile
- tasks/cargo-workspace-feature-unification-order/environment/w2k/src/seed_mux.rs
- tasks/cargo-workspace-feature-unification-order/environment/w2k/src/stub_help.rs
- tasks/cargo-workspace-feature-unification-order/environment/w2k/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/w2k/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/p3n/src/lane_mux.rs
- tasks/cargo-workspace-feature-unification-order/environment/p3n/src/lane_help.rs
- tasks/cargo-workspace-feature-unification-order/environment/p3n/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/p3n/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/c8r/src/row_mux.rs
- tasks/cargo-workspace-feature-unification-order/environment/c8r/src/byte_help.rs
- tasks/cargo-workspace-feature-unification-order/environment/c8r/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/c8r/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/h5k/src/slot_mux.rs
- tasks/cargo-workspace-feature-unification-order/environment/h5k/src/main.rs
- tasks/cargo-workspace-feature-unification-order/environment/h5k/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/orch_v2.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/tbl_r9.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/ph_seed.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/ph_lane.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/ph_row.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/mini_sha.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/mini_toml.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/engine/src/view_mux.rs
- tasks/cargo-workspace-feature-unification-order/environment/members/a1/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/members/a1/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/members/b2/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/members/b2/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/members/g3/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/members/g3/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/k9m/s4/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/k9m/s4/src/lib.rs
- tasks/cargo-workspace-feature-unification-order/environment/docs/formal_rules.md
- tasks/cargo-workspace-feature-unification-order/environment/docs/tgt_ids.txt
- tasks/cargo-workspace-feature-unification-order/environment/docs/operator_cmds.txt
- tasks/cargo-workspace-feature-unification-order/environment/data/perm_seq.toml
- tasks/cargo-workspace-feature-unification-order/environment/data/edge_seed.toml
- tasks/cargo-workspace-feature-unification-order/environment/data/ladder.toml
- tasks/cargo-workspace-feature-unification-order/environment/schemas/row_v4.schema.json
- tasks/cargo-workspace-feature-unification-order/environment/Cargo.toml
- tasks/cargo-workspace-feature-unification-order/environment/Cargo.lock

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: environment/w2k/src/seed_mux.rs
  symbol: fn_w2
  kind: function
  signature: fn fn_w2(seed: u32, edge_tbl: &[(u32, u32)], weak_rows: &[u8]) -> (u32, Vec<u8>)
  purpose: Fold weak dependency feature tokens into canonical byte vector for a build seed
- path: environment/p3n/src/lane_mux.rs
  symbol: fn_p3
  kind: function
  signature: fn fn_p3(member_tag: u8, path_tbl: &[(String, String)], gate: u16) -> (u8, Vec<String>)
  purpose: Normalize path-dependency feature edges after default-features disable on sibling members
- path: environment/c8r/src/row_mux.rs
  symbol: fn_c8
  kind: function
  signature: fn fn_c8(row_tbl: &[u8], dep_path: &Path, meta_dir: &Path) -> (u32, String)
  purpose: Materialize report facet material cross-checking dep-info sidecar bytes
- path: environment/h5k/src/slot_mux.rs
  symbol: fn_h5
  kind: function
  signature: fn fn_h5(order_seed: u32, member_ids: &[&str], hook_tbl: &[(u32, u32)]) -> (u32, Vec<(String, u32)>)
  purpose: Schedule first-build member sequence and aggregate per-seed unified fingerprints
- path: environment/engine/src/view_mux.rs
  symbol: emit_status_view
  kind: function
  signature: fn emit_status_view(report_path: &Path) -> Value
  purpose: Status subcommand view deriving label and pairs_aligned from report mirror material

#### flipping_point_contract

locations:
  - id: A
    path: environment/w2k/src/seed_mux.rs
    controls_tests: [test_q12_sens_mut, test_q13_flip_w2, test_q16_all_perms]
  - id: B
    path: environment/p3n/src/lane_mux.rs
    controls_tests: [test_q14_flip_both, test_q15_flip_p3, test_q3_rc_all]
  - id: C
    path: environment/c8r/src/row_mux.rs
    controls_tests: [test_q6_dig_reduce, test_q7_anchor_hex, test_q8_hex_lower, test_q17_flip_c8]
  - id: D
    path: environment/h5k/src/slot_mux.rs
    controls_tests: [test_q1_shape_vecs, test_q2_hex_agree, test_q4_lbl_set, test_q5_span_max, test_q9_len_vecs, test_q10_rerun_flow, test_q11_twice_same, test_q18_reg_first, test_q20_hook_flow]
  - id: E
    path: environment/engine/src/view_mux.rs
    controls_tests: [test_q19_premature]
no_single_location_flips_majority: true
concentration_cap: 0.5

#### decoy_manifest

- path: environment/w2k/src/stub_help.rs
  kind: helper
  rhymes_with: fn_w2
  non_fix_purpose: Logs weak-edge candidates for diagnostics without canonical fold output
- path: environment/p3n/src/lane_help.rs
  kind: helper
  rhymes_with: fn_p3
  non_fix_purpose: Pretty-prints path dependency tables without normalizing feature edges

#### code_forbidden_tokens

code_forbidden_tokens: [feature, unification, order, workspace, member, dependency, resolver, matrix, mirror, pairs, coherent, facet, digest, sync, permutation, audit, driver, offline, locked, metadata, sidecar, binding, fingerprint, sequence, trigger, obligation, contract, independence, permute, settled, generalization, scenario, alpha, beta, gamma, echo, lag, closure, counter, hexadecimal, regenerating, manifests, emitted, refreshed, captured, agreement, identical, unified, consistently, regardless, primary, twin, targets, shapes, summary, rows, documented, cross-artifact, dep-info, tokens, workflow, reduction, survives, first-build, sidecars, fingerprints, perm_seq]
