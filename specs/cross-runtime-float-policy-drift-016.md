### Decision

GO — Attempt 1. Bank-ready seed validated on approved `overlay-lowerdir-stale-bind` construction mold (`accepted tasks/_ref/overlay-lowerdir-stale-bind/` / `overlay-lowerdir-stale-bind.zip`), reframed to `scientific-computing` + `optimization_under_constraints` + `config_policy_precedence` with **false-green compaction after delayed flush** topology. Three non-trivial discoveries, three coordinated implementation topologies, overlay-style flipping-point ablations, and constraint-complete public obligations without leaking canonical recovery path, replay phase, or reconciliation authority.

### Metadata

- version: 2
- Task name: cross-runtime-float-policy-drift-016
- Title: Cross-runtime float policy lanes
- Category: scientific-computing
- Task shape: optimization_under_constraints
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["scientific-computing", "float-policy", "precedence", "compaction", "delayed-flush", "reconciliation"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract

A scientific matrix runner exposes **multiple configuration surfaces** for numeric policy (defaults, workspace profile TOML, environment overrides, CLI mode flags, a runtime session cache, and durable ledger bytes replayed after partial recovery). After **delayed flush**, local compaction checks and row-level profile flags can look settled while **cross-runtime echo lanes** still disagree once reconciliation replays partial state. The agent must align sources under `/app` so a release workspace build and the published driver write `/app/output/matrix_report.json`. Scenario ids are listed in `/app/docs/sweep_ids.txt`.

**Constraint-complete obligations** (also summarized in `/app/environment/docs/surface_contract.md`; reduction rules in the module comment above `/app/m2/k81/src/main.rs`):

1. **Effective policy precedence (live runs):** for tolerance tier and rounding class, effective values follow **CLI > environment variables > workspace profile > defaults** whenever multiple surfaces are active in the same run.
2. **Post-recovery authority:** after partial recovery, **durable ledger bytes** are the sole authority for merge/materialization decisions; the runtime session cache may inform diagnostics but must not override ledger-selected policy packs.
3. **Cross-format regeneration:** every full pipeline regeneration must pass the **slow cross-format lane reducer**; no fast cat_lane emit path may produce row-level `lane_hex` or summary `trace_digest` without the same reducer used for compaction-settled rows.

**Optimization target (externally tested):** among implementations satisfying obligations 1–3 for every scenario in `sweep_ids.txt`, **`tier_span` must equal 0** (all `drift_code` zero) and summary `compact_status` must read `settled`. Incoherent emissions break mirror agreement, leave non-zero `drift_code`, or leave `compact_status` unsettled.

The report has `rows` and `summary`. Each row records scenario_id, three per-row closure booleans, drift_code, and lane_hex (exactly 16 lowercase hexadecimal digits). The summary records `rows_total`, `compact_status`, `tier_span`, and `trace_digest`. Mirror pairs are `lowerdir` with `lowerdir_echo`, `upper` with `upper_echo`, and `worker` with `worker_echo`. Coherent runs keep `drift_code` at 0 on every row, all three per-row closure fields true, matching `lane_hex` on each pair, and `compact_status` reading `settled`. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_hints.txt` for cargo and pytest argv details.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category_profile = "config_policy_precedence"`
- path: instruction.md
  role: natural public task prompt (constraint-complete obligations; must not name patch sites or canonical recovery order)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl/uv bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation and pipeline traps
- path: solution/solve.sh
  role: oracle applying patch then release build + driver
- path: environment/Dockerfile
  role: build definition; pre-install cargo, pytest, and locked toolchain
- path: construction_manifest.json
  role: local authoring artifact mirroring construction manifest below

### task_files

- path: environment/Cargo.toml
  role: workspace root
- path: environment/Cargo.lock
  role: locked dependency graph
- path: environment/m2/k81/Cargo.toml
  role: driver crate manifest
- path: environment/m2/k81/src/main.rs
  role: scenario-matrix driver emitting matrix_report.json; documents trace_digest and tier_span
- path: environment/m2/k81/src/gate_mux.rs
  role: oracle frontier C — combine ordering for delayed-flush side vs compaction gate callbacks
- path: environment/m2/k81/src/stack_mix.rs
  role: ladder application glue coupling float policy packs to lane material
- path: environment/m2/k81/src/step_key.rs
  role: per-step key material
- path: environment/p7/layer_core/Cargo.toml
  role: shared core crate
- path: environment/p7/layer_core/src/lib.rs
  role: core exports
- path: environment/p7/layer_core/src/mesh.rs
  role: mesh view helpers
- path: environment/p7/layer_core/src/family.rs
  role: family specs for numeric lanes
- path: environment/p7/layer_core/src/row_help.rs
  role: hex16 formatting helper
- path: environment/p7/layer_core/src/mix_stamp.rs
  role: slow cross-format lane reducer (required regeneration path)
- path: environment/p7/layer_core/src/apply.rs
  role: numeric mix helpers (decoy-adjacent)
- path: environment/p7/layer_core/src/kind.rs
  role: kind tagging
- path: environment/p7/layer_core/src/stack.rs
  role: frame stack helpers
- path: environment/p7/layer_core/src/alias_stub.rs
  role: linear algebra stub (non-fix)
- path: environment/p7/y4/Cargo.toml
  role: pack merge crate (durable ledger authority)
- path: environment/p7/y4/src/hold.rs
  role: oracle frontier B — durable pack merge refresh under ledger precedence
- path: environment/p7/y4/src/lib.rs
  role: y4 exports
- path: environment/p7/y4/src/body.rs
  role: counter helpers
- path: environment/p7/y4/src/shape.rs
  role: dimension checks
- path: environment/p7/y5/Cargo.toml
  role: fold material crate
- path: environment/p7/y5/src/tie.rs
  role: oracle frontier A — cross-runtime lane tag fold for lane_hex material
- path: environment/p7/y5/src/lib.rs
  role: y5 exports
- path: environment/p7/y5/src/body.rs
  role: bitmask helpers
- path: environment/p7/y5/src/stamp_help.rs
  role: widen helpers (decoy)
- path: environment/p7/y6/Cargo.toml
  role: stride/cat_lane crate (fast-path trap surface)
- path: environment/p7/y6/src/stride.rs
  role: decoy rhyming with gate ordering (shipped broken ordering helper for ablation)
- path: environment/p7/y6/src/cat_lane.rs
  role: decoy fast cat_lane emit rhyming with mix_stamp (non-fix regeneration shortcut)
- path: environment/p7/y6/src/lib.rs
  role: y6 exports
- path: environment/p7/y6/src/body.rs
  role: clip helpers
- path: environment/data/ladder.toml
  role: per-scenario delayed-flush + compaction replay tables (cross-runtime echo lanes)
- path: environment/data/channel.toml
  role: channel weights for numeric mix
- path: environment/data/seed.json
  role: seeded profile/tolerance fixtures across runtimes
- path: environment/data/weights.tsv
  role: weight table for core mix
- path: environment/data/base_defaults.toml
  role: default tolerance tier and rounding class
- path: environment/data/ws_layer.toml
  role: workspace profile overrides
- path: environment/data/notes.md
  role: operator notes (no fix recipe)
- path: environment/docs/sweep_ids.txt
  role: comma-separated scenario ids (mirror triple + base scenarios)
- path: environment/docs/surface_contract.md
  role: precedence ladder, cross-format lane rules, CLI semantics, compaction-settled definition
- path: environment/docs/build_hints.txt
  role: cargo/pytest argv and ablation path hints (paths only, not fixes)
- path: solution/oracle.patch
  role: unified diff applied by solve.sh

### fix_frontier

- count: 3
- distribution: `environment/p7/y5/src/tie.rs`, `environment/p7/y4/src/hold.rs`, `environment/m2/k81/src/gate_mux.rs` (distinct crate roots under p7 and m2)
- naming_policy: Keep opaque Rust identifiers on the fix path (`tag_mix`, `pack_refresh`, `gate_order`); do not rename to instruction nouns
- forbidden_stems: cross, runtime, float, policy, drift, compaction, compact, flush, delayed, reconciliation, durable, authority, precedence, profile, tolerance, tier, lane, scenario, mirror, coherent, settled, ledger, session, override, workspace, cli, environment, regen, pipeline, rounding, cache, checkpoint, recovery, partial, observer, trace, digest, sync, emit, reducer, cat_lane, matrix, regen, obligation, optimization, minimize, echo, incoherent
- helpers_policy: `cat_lane.rs`, `stride.rs`, `stamp_help.rs`, `probe.rs`, `alias_stub.rs` are decoys or non-fix helpers declared in decoy_manifest
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: trace_digest recomputation, lane_hex mirror pairs, delayed-flush compaction traps, ablation incoherence, pipeline overwrite trap, consecutive run identity, cross-format lane agreement, effective-policy trace derivation
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction.md; per-scenario answer rows in docs; boolean answer-key JSON fields named `overall_pass` or `scenario_pass`

### task_shape

- type: optimization_under_constraints
- instruction_framing: constraint-complete
- hardness_source: constrained optimization — satisfy multi-surface policy precedence and compaction-settled coherence without naming which merge rule, combine ordering, or emit path is defective
- collapse_risk: leaking canonical recovery path, replay phase, or reconciliation authority collapses to localized one-file repair

### category_profile

- challenge_family: delayed_flush_lane_matrix_divergence
- profile_name: config_policy_precedence
- allowed_instruction_disclosures: config surfaces, conflict scenarios, public precedence outcomes, reload/recovery behavior, effective-policy and compaction artifacts, driver command, optimization target (tier_span zero + compact_status settled), report schema, mirror pairs, trace_digest definition header, deterministic rerun requirement
- forbidden_instruction_leaks: lookup path, broken layer, internal precedence table implementation, exact source file/function, patch order, which module is canonical by default, replay phase ordering bug description, fast-path bypass file name
- category_specific_hardness_bar: effective numeric policy must derive across CLI, environment, workspace files, defaults, runtime session cache, and durable ledger after partial recovery; delayed-flush compaction must coordinate with cross-runtime echo lanes
- category_specific_verifier_risks: policy-table transcription, one config file shortcut, hidden unstated cases, clean-start-only tests, brittle float exact-equality without documented tolerance class
- coverage_role: Adds scientific-computing optimization_under_constraints coverage under config_policy_precedence distinct from repair-shaped layered-policy-reload-drift and formal_reasoning revocation-cache-authority-split-012

### satisfiability_risk

- rc2_planned_name_risk: medium — instruction uses domain nouns; fix path stays opaque neutral crate paths (m2/p7) with `tag_mix` / `pack_refresh` / `gate_order`
- gx9_contract_risk: low — trace_digest derived from rows; per-row booleans are product-shaped closure fields documented in instruction
- cr1_symbol_frontier_risk: low — three substantive Rust modules plus distributed layer_core support
- hidden_contract_risk: medium — false-green row flags vs summary compact_status during replay ordering require ablation tests; mitigated by surface_contract.md and main.rs header

### actionability_plan

- verifier_command_visible: `cargo build --release --locked` from `/app` and driver at `/app/target/release/mk`; pytest via `/opt/verifier-venv` per build_hints.txt
- source_fix_intent_visible: instruction requires aligning sources to satisfy three obligations and optimization target; does not name `tag_mix`, `pack_refresh`, or `gate_order`
- generated_output_rule_visible: `/app/output/matrix_report.json` path and field names
- exact_formula_home: module comment above `environment/m2/k81/src/main.rs` plus `environment/docs/surface_contract.md` (tolerance class bands, trace_digest reduction, subspace norm threshold 1e-2 for drift_code zero when documented)
- schema_home: instruction.md public contract + output_contract.toml paths

### waiver_plan

- waivers_expected: no
- waiver_rationale: Overlay mold demonstrates RC2-safe naming; regeneration, flipping-point, and precedence/compaction tests avoid hidden-instance puzzles

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/_ref/overlay-lowerdir-stale-bind/` (`overlay-lowerdir-stale-bind.zip`) for verifier shape, flipping-point ablations, pipeline traps, and pytest ablation patterns; reframed to scientific-computing + config_policy_precedence + optimization_under_constraints with cross-runtime float policy and delayed-flush compaction vocabulary. No promoted `docs/reference_tasks/index.json` entry matches this exact profile combo.

### realism_source

- source_type: synthetic_exception
- evidence_basis: Minimized from HPC / simulation control planes where mixed-precision policy tables, session caches, and checkpoint ledgers disagree after flush-delayed compaction and cross-runtime replay
- upstream_or_synthetic_rationale: Controlled false-green compaction with deterministic replay — avoids hidden-instance “which file is corrupt” puzzles while preserving real precedence + numeric-policy coupling
- minimization_preserves: Split authority surfaces (runtime cache vs durable ledger), false-green intermediate verifier state after replay ordering, fast-path regeneration bypass of cross-format lane reducer
- synthetic_exception_review: Difficulty from coupled precedence/numeric-policy/compaction semantics and constraint-complete optimization target, not obscure facts; decoys perform real non-fix work

### difficulty_mechanism_plan

- mechanisms: partial_observability_experiment_design, false_green_intermediate_states, environment_specific_cli_semantics, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, buried_local_constraints, stateful_multi_step_dependencies
- adversarial_layers_count: 7
- fairness_guardrails: All tested formulas and scenario ids are public; deterministic rebuild; no timing/latency thresholds
- mechanism: partial_observability_experiment_design
  placement: runtime session cache visible in driver diagnostics vs durable ledger bytes only in recovery fixtures
  why_model_misses_it: models treat live session cache as authoritative after partial recovery
  fairness_guardrail: obligation 2 states ledger precedence explicitly
- mechanism: false_green_intermediate_states
  placement: per-row three per-row closure booleans vs summary compact_status during delayed-flush replay ordering
  why_model_misses_it: agents stop after row-level greens without mirror/trace_digest cross-check
  fairness_guardrail: mirror pairs and trace_digest contract are in instruction and surface_contract.md
- mechanism: environment_specific_cli_semantics
  placement: driver argv modes select which config surfaces participate before compaction scoring
  why_model_misses_it: default mode hides workspace/env conflicts until echo-lane mode runs
  fairness_guardrail: surface_contract.md documents modes without naming internal functions
- mechanism: deceptive_but_valid_local_evidence
  placement: cat_lane fast emit vs mix_stamp slow reducer; runtime cache shows coherent tolerance tier locally
  why_model_misses_it: summary looks settled while lane_hex diverges on echo lanes
  fairness_guardrail: obligation 3 and cross-lane tests
- mechanism: cross_file_cross_format_invariants
  placement: JSON report vs TOML ladder vs ledger pack bytes must agree on lane_hex linkage
  why_model_misses_it: editing one format leaves orphans that still pass shallow row flags
  fairness_guardrail: cross-format rules in surface_contract.md with worked examples
- mechanism: buried_local_constraints
  placement: tag_mix must include prev_family shift, not step_ix alone, for cross-runtime lane material
  why_model_misses_it: looks like optional lineage field
  fairness_guardrail: ablation test reverts tag_mix body
- mechanism: stateful_multi_step_dependencies
  placement: ladder.toml scenarios spanning delayed flush, ledger replay, then echo lanes
  why_model_misses_it: fixing one lane table without merge ordering leaves echo policy drift
  fairness_guardrail: deterministic sweep_ids.txt

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert can satisfy three obligations and optimization target using surface_contract.md and regenerated report within a few hours
- shortcut_audit: static JSON, test deletion, stale-doc-only edits, reward file writes, digest hardcoding, single-surface precedence table copy
- ablation_plan: revert tag_mix only, pack_refresh only, gate_order only — each should drop pass rate on disjoint test subsets
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=Part E worst-model accuracy on platform
- verifier_offline: pytest and cargo locked in Dockerfile; test.sh performs no runtime network installs under allow_internet=false
- post_upload_difficulty: final Hard/Medium/Easy label follows platform agent runs (Part E)

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward 1 only when all pytest cases pass

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: n/a — single-step task
- local_only_data: true
- sidecar_or_protocol_notes: single-container Rust workspace; no compose services
- long_context_token_floor: n/a

### Failure topology

Cross-runtime float policy drift appears when three authorities disagree: runtime-visible session cache, durable ledger bytes replayed after partial recovery, and replay-ordered lane emission after **delayed flush**. Local compaction and row-level profile flags can read coherent while echo lanes re-materialize stale tolerance tiers and a fast cat_lane regeneration path skips the slow cross-format reducer—producing a green intermediate verifier state that masks corruption until full pipeline replay. Hardness requires reconciling precedence, numeric-policy materialization, and compaction-settled coherence under the three public obligations and tier_span optimization target without the instruction naming which merge rule, which combine ordering, or which emit path is defective.

### Environment shape

Rust Cargo workspace under `/app` forked from the overlay reference mold: driver crate `m2/k81`, pack crates `p7/y4`–`y6`, shared `p7/layer_core`. Policy fixtures under `environment/data/` (`base_defaults.toml`, `ws_layer.toml`, `seed.json`, `ladder.toml`). Formal contract in `environment/docs/surface_contract.md`. Output at `/app/output/matrix_report.json`. Step 2b may fork `accepted tasks/_ref/overlay-lowerdir-stale-bind/environment/` then reframe docs, field names, and broken semantics for float-policy precedence + delayed-flush compaction; do not shrink below 20 non-Docker environment files.

### Required artifacts

instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh, solution/oracle.patch, and the environment tree listed in Initial Draft Commitments.

### Test plan

- `test_fpd_r1_table`: report shape; scenario ids match sweep_ids.txt
- `test_fpd_r2_mirror`: paired echo lanes agree on lane_hex and closure fields when coherent
- `test_fpd_r3_closure_flags`: coherent run — drift_code 0 and three row closure fields true on all rows
- `test_fpd_r4_compact_status`: summary compact_status settled when matrix coherent
- `test_fpd_r5_tier`: tier_span equals max abs drift_code; optimization target tier_span==0 when coherent
- `test_fpd_r6_digest_rule`: summary trace_digest matches driver header reduction from rows
- `test_fpd_r7_digest_anchor`: summary trace_digest matches known-good repaired emission
- `test_fpd_r8_pattern_format`: lane_hex sixteen lowercase hex chars
- `test_fpd_r9_rows_total`: rows_total integer equals len(rows)
- `test_fpd_r10_overwrite`: tampered hand-written JSON replaced by pipeline rerun
- `test_fpd_r11_idempotent`: consecutive pipeline runs identical
- `test_fpd_r12_lowerdir_sensitivity`: mutating lowerdir step table changes lane_hex and trace_digest
- `test_fpd_r13_tag_ablation`: reverting tag_mix lineage body breaks cross-runtime lane coherence
- `test_fpd_r14_dual_ablation`: reverting pack refresh and tag_mix together breaks pipeline
- `test_fpd_r15_order_ablation`: broken gate wiring + stock stride helper breaks compaction closure
- `test_fpd_r16_ledger_trap`: echo lane cannot keep stale tolerance tier after ledger replay fixture
- `test_fpd_r17_fastpath_trap`: forcing cat_lane-only emit breaks cross-format lane agreement
- `test_fpd_r18_precedence_cli`: CLI mode overrides workspace tier for active scenario without breaking echo agreement when coherent
- `test_fpd_r19_delayed_flush`: delayed-flush scenario requires side-before-gate ordering to reach compact_status settled

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests.

### Drafting guardrails

Instruction is constraint-complete: state the three obligations, optimization target, and report contract without naming `tag_mix`, `pack_refresh`, `gate_order`, replay phase, canonical recovery order, or fast-path module. Do not copy overlay “Repair sources” wording — use optimization language (“align sources so constraints hold”). Tests derive verdicts from regenerated JSON, ledger precedence traps, delayed-flush traps, and ablations—not static answer keys.

### Triviality Ledger

- Hand-writing matrix_report.json fails `test_fpd_r10_overwrite` because verifier reruns cargo + driver.
- Fixing only tag_mix without pack_refresh fails `test_fpd_r14_dual_ablation` and mirror coherence subsets.
- Fixing only gate ordering without stride/gate contract fails `test_fpd_r15_order_ablation` and `test_fpd_r19_delayed_flush`.
- Satisfying runtime session cache while ignoring ledger precedence fails `test_fpd_r16_ledger_trap`.
- Routing regeneration through cat_lane fast emit fails `test_fpd_r17_fastpath_trap` even when row flags look green.
- Copying precedence table literals from instruction into one TOML file fails `test_fpd_r18_precedence_cli` when CLI/env surfaces disagree in echo mode.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle patch must change semantics in three roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns listed in code_forbidden_tokens must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays constraint-complete about obligations, not cause-revealing (“pack_refresh omits storage”).
- RC5/RC6: schemas and trace_digest home in main.rs header + surface_contract.md; no boolean answer grid in instruction.
- RC7/GX3: oracle.patch coordinated across tie/hold/gate_mux with substantive bodies (same structural fixes as overlay reference: lineage fold, pack storage refresh, gate order invert).
- GX9/GX10: derived trace_digest and pair equality; no per-scenario expected literals in instruction.
- GX4/GX5: ablation tests patch sources in-container; expectations computed from contract functions in test file.
- Static: run `collapse_check.py --check flipping_point_compliance` and `grep_resistance` after Step 2b.

### Initial Draft Commitments

- tasks/cross-runtime-float-policy-drift-016/task.toml
- tasks/cross-runtime-float-policy-drift-016/instruction.md
- tasks/cross-runtime-float-policy-drift-016/output_contract.toml
- tasks/cross-runtime-float-policy-drift-016/construction_manifest.json
- tasks/cross-runtime-float-policy-drift-016/tests/test.sh
- tasks/cross-runtime-float-policy-drift-016/tests/test_outputs.py
- tasks/cross-runtime-float-policy-drift-016/solution/solve.sh
- tasks/cross-runtime-float-policy-drift-016/solution/oracle.patch
- tasks/cross-runtime-float-policy-drift-016/environment/Dockerfile
- tasks/cross-runtime-float-policy-drift-016/environment/Cargo.toml
- tasks/cross-runtime-float-policy-drift-016/environment/Cargo.lock
- tasks/cross-runtime-float-policy-drift-016/environment/m2/k81/Cargo.toml
- tasks/cross-runtime-float-policy-drift-016/environment/m2/k81/src/main.rs
- tasks/cross-runtime-float-policy-drift-016/environment/m2/k81/src/gate_mux.rs
- tasks/cross-runtime-float-policy-drift-016/environment/m2/k81/src/stack_mix.rs
- tasks/cross-runtime-float-policy-drift-016/environment/m2/k81/src/step_key.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/Cargo.toml
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/lib.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/mesh.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/family.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/row_help.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/mix_stamp.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/apply.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/probe.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/kind.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/stack.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/layer_core/src/alias_stub.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y4/Cargo.toml
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y4/src/lib.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y4/src/hold.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y4/src/body.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y4/src/shape.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y5/Cargo.toml
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y5/src/lib.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y5/src/tie.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y6/Cargo.toml
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y6/src/lib.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y6/src/stride.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y6/src/cat_lane.rs
- tasks/cross-runtime-float-policy-drift-016/environment/p7/y6/src/body.rs
- tasks/cross-runtime-float-policy-drift-016/environment/data/ladder.toml
- tasks/cross-runtime-float-policy-drift-016/environment/data/channel.toml
- tasks/cross-runtime-float-policy-drift-016/environment/data/seed.json
- tasks/cross-runtime-float-policy-drift-016/environment/data/weights.tsv
- tasks/cross-runtime-float-policy-drift-016/environment/data/base_defaults.toml
- tasks/cross-runtime-float-policy-drift-016/environment/data/ws_layer.toml
- tasks/cross-runtime-float-policy-drift-016/environment/data/notes.md
- tasks/cross-runtime-float-policy-drift-016/environment/docs/sweep_ids.txt
- tasks/cross-runtime-float-policy-drift-016/environment/docs/surface_contract.md
- tasks/cross-runtime-float-policy-drift-016/environment/docs/build_hints.txt

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p7/y5/src/tie.rs
  symbol: tag_mix
  kind: function
  signature: tag_mix(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Derives lane_hex material from step and cross-runtime profile tuple
- path: environment/p7/y4/src/hold.rs
  symbol: pack_refresh
  kind: function
  signature: pack_refresh(state: &mut PackState, incoming: &PackState, stamp_b: u64)
  purpose: Merges incoming durable pack into active state under ledger authority
- path: environment/m2/k81/src/gate_mux.rs
  symbol: gate_order
  kind: function
  signature: gate_order<F: FnMut(), G: FnMut()>(side: F, gate: G) -> u32
  purpose: Invokes side and gate callbacks in seeded combine order during delayed-flush replay
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p7/y5/src/tie.rs
    controls_tests: [test_fpd_r2_mirror, test_fpd_r13_tag_ablation, test_fpd_r7_digest_anchor, test_fpd_r16_ledger_trap]
  - id: B
    path: environment/p7/y4/src/hold.rs
    controls_tests: [test_fpd_r14_dual_ablation, test_fpd_r4_compact_status, test_fpd_r10_overwrite, test_fpd_r16_ledger_trap]
  - id: C
    path: environment/m2/k81/src/gate_mux.rs
    controls_tests: [test_fpd_r15_order_ablation, test_fpd_r3_closure_flags, test_fpd_r6_digest_rule, test_fpd_r17_fastpath_trap, test_fpd_r19_delayed_flush]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/p7/y6/src/cat_lane.rs
  kind: module
  rhymes_with: mix_stamp
  non_fix_purpose: Fast cat_lane emit used in fastpath trap; must not satisfy obligation 3 alone
- path: environment/p7/y6/src/stride.rs
  kind: helper
  rhymes_with: gate_order
  non_fix_purpose: Alternate step_1 ordering helper used in ablation traps, not the fix path
- path: environment/p7/layer_core/src/probe.rs
  kind: helper
  rhymes_with: pack_refresh
  non_fix_purpose: Runtime-visible session cache for diagnostics; not durable ledger authority
- path: environment/p7/y5/src/stamp_help.rs
  kind: helper
  rhymes_with: tag_mix
  non_fix_purpose: Widening utilities for non-fix stamp experiments
```

#### code_forbidden_tokens

```
cross, runtime, policy, drift, compaction, compact, flush, delayed, reconciliation, durable, authority, precedence, tolerance, tier, scenario, mirror, coherent, settled, ledger, session, override, workspace, cli, regen, pipeline, rounding, cache, checkpoint, recovery, partial, observer, digest, sync, reducer, matrix, obligation, optimization, minimize, echo, incoherent, numeric, scientific
```
