### Decision

GO — Attempt 1. Bank-ready seed `cross-runtime-float-policy-drift-046` passes idea validation on the approved `overlay-lowerdir-stale-bind` construction mold (`accepted tasks/overlay-lowerdir-stale-bind.zip`), reframed to **security** + **optimization_under_constraints** + **floating_point_numeric_policy** with **false-green compaction after delayed flush** topology. Three mandated discoveries, three coordinated implementation topologies, overlay-style flipping-point ablations, and constraint-complete public obligations (metric, tolerance class, reproducibility rule) without leaking canonical recovery path, replay phase ordering, or reconciliation authority. Distinct from `cross-runtime-float-policy-drift-016` (scientific-computing + config_policy_precedence) via security attestation framing and numeric-policy-first verifier contract.

### Metadata

- version: 2
- Task name: cross-runtime-float-policy-drift-046
- Title: Cross-runtime float policy audit
- Category: security
- Task shape: optimization_under_constraints
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["security", "float-policy", "attestation", "delayed-flush", "cross-runtime", "audit"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract

A hardened numeric attestation gateway exposes **multiple runtime surfaces** for floating-point policy (defaults, workspace profile TOML, environment overrides, CLI mode flags, a runtime session cache, and durable attest ledger bytes replayed after partial recovery). After **delayed flush**, local compaction probes and per-row seal flags can read coherent while **cross-runtime echo lanes** still disagree once reconciliation replays partial state. The agent must align sources under `/app` so a release workspace build and the published driver write `/app/output/policy_audit_report.json`. Scenario ids are listed in `/app/docs/case_ids.txt`.

**Constraint-complete obligations** (also summarized in `/app/environment/docs/surface_contract.md`; reduction rules in the module comment above `/app/m6/k86/src/main.rs`):

1. **Effective float policy (live runs):** for tolerance tier and rounding mode, effective values follow **CLI > environment variables > workspace profile > defaults** whenever multiple surfaces are active in the same run.
2. **Post-recovery authority:** after partial recovery, **durable attest ledger bytes** are the sole authority for merge and materialization decisions; the runtime session cache may inform diagnostics but must not override ledger-selected policy packs.
3. **Cross-format regeneration:** every full pipeline regeneration must pass the **slow cross-format norm reducer**; no fast emit path may produce row-level `seal_hex` or summary `policy_digest` without the same reducer used for compaction-settled rows.

**Numeric policy disclosures (externally tested):**
- **Metric:** per-scenario `norm_skew` is the absolute subspace norm delta between primary and echo material for the active tolerance tier; coherent runs require `norm_skew == 0`.
- **Tolerance class:** documented bands in `surface_contract.md` (`strict`, `balanced`, `relaxed`) with fixed subspace norm ceilings used when deriving zero skew.
- **Reproducibility rule:** `policy_digest` is a deterministic 16-hex digest over sorted row `(scenario_id, seal_hex, norm_skew)` tuples using the reduction in the `main.rs` header; consecutive pipeline runs must match.

**Optimization target (externally tested):** among implementations satisfying obligations 1–3 for every scenario in `case_ids.txt`, **`policy_span` must equal 0** (all `norm_skew` zero) and summary `audit_status` must read `settled`. Incoherent emissions break mirror agreement, leave non-zero `norm_skew`, or leave `audit_status` unsettled.

The report has `rows` and `summary`. Each row records `scenario_id`, three per-row closure booleans, `norm_skew`, and `seal_hex` (exactly 16 lowercase hexadecimal digits). The summary records `rows_total`, `audit_status`, `policy_span`, and `policy_digest`. Mirror pairs are `lowerdir` with `lowerdir_echo`, `upper` with `upper_echo`, and `worker` with `worker_echo`. Coherent runs keep `norm_skew` at 0 on every row, all three per-row closure fields true, matching `seal_hex` on each pair, and `audit_status` reading `settled`. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_hints.txt` for cargo and pytest argv details.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category_profile = "floating_point_numeric_policy"`
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
- path: environment/m6/k86/Cargo.toml
  role: driver crate manifest
- path: environment/m6/k86/src/main.rs
  role: scenario-matrix driver emitting policy_audit_report.json; documents policy_digest and policy_span
- path: environment/m6/k86/src/gate_mux.rs
  role: oracle frontier C — combine ordering for delayed-flush side vs compaction gate callbacks
- path: environment/m6/k86/src/stack_mix.rs
  role: ladder application glue coupling float policy packs to lane material
- path: environment/m6/k86/src/step_key.rs
  role: per-step key material
- path: environment/p8/layer_core/Cargo.toml
  role: shared core crate
- path: environment/p8/layer_core/src/lib.rs
  role: core exports
- path: environment/p8/layer_core/src/mesh.rs
  role: mesh view helpers
- path: environment/p8/layer_core/src/family.rs
  role: family specs for numeric lanes
- path: environment/p8/layer_core/src/row_help.rs
  role: hex16 formatting helper
- path: environment/p8/layer_core/src/norm_reduce.rs
  role: slow cross-format norm reducer (required regeneration path)
- path: environment/p8/layer_core/src/apply.rs
  role: numeric mix helpers (decoy-adjacent)
- path: environment/p8/layer_core/src/probe.rs
  role: runtime session cache helper (decoy)
- path: environment/p8/layer_core/src/kind.rs
  role: kind tagging
- path: environment/p8/layer_core/src/stack.rs
  role: frame stack helpers
- path: environment/p8/layer_core/src/alias_stub.rs
  role: linear algebra stub (non-fix)
- path: environment/p8/y4/Cargo.toml
  role: pack merge crate (durable ledger authority)
- path: environment/p8/y4/src/hold.rs
  role: oracle frontier B — durable pack merge refresh under ledger precedence
- path: environment/p8/y4/src/lib.rs
  role: y4 exports
- path: environment/p8/y4/src/body.rs
  role: counter helpers
- path: environment/p8/y4/src/shape.rs
  role: dimension checks
- path: environment/p8/y5/Cargo.toml
  role: fold material crate
- path: environment/p8/y5/src/tie.rs
  role: oracle frontier A — cross-runtime seal tag fold for seal_hex material
- path: environment/p8/y5/src/lib.rs
  role: y5 exports
- path: environment/p8/y5/src/body.rs
  role: bitmask helpers
- path: environment/p8/y5/src/stamp_help.rs
  role: widen helpers (decoy)
- path: environment/p8/y6/Cargo.toml
  role: stride/cat_lane crate (fast-path trap surface)
- path: environment/p8/y6/src/stride.rs
  role: decoy rhyming with gate ordering (shipped broken ordering helper for ablation)
- path: environment/p8/y6/src/cat_lane.rs
  role: decoy fast cat_lane emit rhyming with norm_reduce (non-fix regeneration shortcut)
- path: environment/p8/y6/src/lib.rs
  role: y6 exports
- path: environment/p8/y6/src/body.rs
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
  role: default tolerance tier and rounding mode
- path: environment/data/ws_layer.toml
  role: workspace profile overrides
- path: environment/data/notes.md
  role: operator notes (no fix recipe)
- path: environment/docs/case_ids.txt
  role: comma-separated scenario ids (mirror triple + base scenarios)
- path: environment/docs/surface_contract.md
  role: tolerance bands, cross-format seal rules, CLI semantics, compaction-settled definition
- path: environment/docs/build_hints.txt
  role: cargo/pytest argv and ablation path hints (paths only, not fixes)
- path: solution/oracle.patch
  role: unified diff applied by solve.sh

### fix_frontier

- count: 3
- distribution: `environment/p8/y5/src/tie.rs`, `environment/p8/y4/src/hold.rs`, `environment/m6/k86/src/gate_mux.rs` (distinct crate roots under p8 and m6)
- naming_policy: Keep opaque Rust identifiers on the fix path (`norm_fold`, `ledger_merge`, `mux_seq`); do not rename to instruction nouns
- forbidden_stems: cross, runtime, float, policy, drift, compaction, compact, flush, delayed, reconciliation, durable, authority, precedence, profile, tolerance, tier, lane, scenario, mirror, coherent, settled, ledger, session, override, workspace, cli, environment, regen, pipeline, rounding, cache, checkpoint, recovery, partial, observer, digest, sync, reducer, cat_lane, matrix, obligation, optimization, minimize, echo, incoherent, numeric, attestation, audit, seal, skew, norm, gateway, hardened, attest, principal, asset, security
- helpers_policy: `cat_lane.rs`, `stride.rs`, `stamp_help.rs`, `probe.rs`, `alias_stub.rs` are decoys or non-fix helpers declared in decoy_manifest
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: policy_digest recomputation, seal_hex mirror pairs, delayed-flush compaction traps, ablation incoherence, pipeline overwrite trap, consecutive run identity, cross-format seal agreement, effective-policy trace derivation, tolerance-band norm_skew checks
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction.md; per-scenario answer rows in docs; boolean answer-key JSON fields named `overall_pass` or `scenario_pass`

### task_shape

- type: optimization_under_constraints
- instruction_framing: constraint-complete
- hardness_source: constrained optimization — satisfy multi-surface float policy precedence and compaction-settled coherence under security attestation constraints without naming which merge rule, combine ordering, or emit path is defective
- collapse_risk: leaking canonical recovery path, replay phase, or reconciliation authority collapses to localized one-file repair

### category_profile

- challenge_family: delayed_flush_attest_lane_divergence
- profile_name: floating_point_numeric_policy
- allowed_instruction_disclosures: metric (norm_skew), tolerance class bands, reproducibility rule (policy_digest reduction), accepted inputs, public artifacts, driver command, optimization target (policy_span zero + audit_status settled), report schema, mirror pairs, deterministic rerun requirement
- forbidden_instruction_leaks: broken reduction order, precision source, cache path, patch function, formula home beyond public header/contract, replay phase ordering bug description, fast-path bypass file name
- category_specific_hardness_bar: numeric policy precedence spans computation, caching, comparison, and cross-runtime materialization surfaces; delayed-flush compaction must coordinate with echo lanes under partial recovery
- category_specific_verifier_risks: brittle exact-equality without documented tolerance class, one epsilon tweak, formula transcription shortcut, hardware-sensitive assertions
- coverage_role: Adds security optimization_under_constraints coverage under floating_point_numeric_policy distinct from scientific-computing config_policy_precedence tasks and repair-shaped archive-repair

### satisfiability_risk

- rc2_planned_name_risk: medium — instruction uses domain nouns; fix path stays opaque neutral crate paths (m6/p8) with `norm_fold` / `ledger_merge` / `mux_seq`
- gx9_contract_risk: low — policy_digest derived from rows; per-row booleans are product-shaped closure fields documented in instruction
- cr1_symbol_frontier_risk: low — three substantive Rust modules plus distributed layer_core support
- hidden_contract_risk: medium — false-green row flags vs summary audit_status during replay ordering require ablation tests; mitigated by surface_contract.md and main.rs header

### actionability_plan

- verifier_command_visible: `cargo build --release --locked` from `/app` and driver at `/app/target/release/mk`; pytest via `/opt/verifier-venv` per build_hints.txt
- source_fix_intent_visible: instruction requires aligning sources to satisfy three obligations and optimization target; does not name `norm_fold`, `ledger_merge`, or `mux_seq`
- generated_output_rule_visible: `/app/output/policy_audit_report.json` path and field names
- exact_formula_home: module comment above `environment/m6/k86/src/main.rs` plus `environment/docs/surface_contract.md` (tolerance class bands, policy_digest reduction, subspace norm threshold 1e-2 for norm_skew zero when documented)
- schema_home: instruction.md public contract + output_contract.toml paths

### waiver_plan

- waivers_expected: no
- waiver_rationale: Overlay mold demonstrates RC2-safe naming; regeneration, flipping-point, and numeric-policy tests avoid hidden-instance puzzles

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/overlay-lowerdir-stale-bind.zip` for verifier shape, flipping-point ablations, pipeline traps, and pytest ablation patterns; reframed to security + floating_point_numeric_policy + optimization_under_constraints with cross-runtime float policy attestation and delayed-flush compaction vocabulary. No promoted `docs/reference_tasks/index.json` entry matches this exact profile combo.

### realism_source

- source_type: synthetic_exception
- evidence_basis: Minimized from hardened attestation gateways and confidential-compute control planes where mixed-precision policy tables, session caches, and checkpoint ledgers disagree after flush-delayed compaction and cross-runtime replay
- upstream_or_synthetic_rationale: Controlled false-green compaction with deterministic replay — avoids hidden-instance “which file is corrupt” puzzles while preserving real numeric-policy + authority-split coupling
- minimization_preserves: Split authority surfaces (runtime cache vs durable ledger), false-green intermediate verifier state after replay ordering, fast-path regeneration bypass of cross-format norm reducer
- synthetic_exception_review: Difficulty from coupled numeric-policy/compaction/attestation semantics and constraint-complete optimization target, not obscure facts; decoys perform real non-fix work

### Failure topology

Cross-runtime float policy drift appears when three authorities disagree: runtime-visible session cache, durable attest ledger bytes replayed after partial recovery, and replay-ordered lane emission after **delayed flush**. Local compaction and per-row seal flags can read coherent while echo lanes re-materialize stale tolerance tiers and a fast cat_lane regeneration path skips the slow cross-format norm reducer—producing a green intermediate verifier state that masks corruption until full pipeline replay. Hardness requires reconciling float policy precedence, numeric materialization, and compaction-settled coherence under the three public obligations and policy_span optimization target without the instruction naming which merge rule, which combine ordering, or which emit path is defective.

### Environment shape

Rust Cargo workspace under `/app` forked from the overlay reference mold: driver crate `m6/k86`, pack crates `p8/y4`–`y6`, shared `p8/layer_core`. Policy fixtures under `environment/data/` (`base_defaults.toml`, `ws_layer.toml`, `seed.json`, `ladder.toml`). Formal contract in `environment/docs/surface_contract.md`. Output at `/app/output/policy_audit_report.json`. Step 2b may fork `accepted tasks/overlay-lowerdir-stale-bind.zip` environment/ then reframe crate roots, docs, field names, and broken semantics for security attestation + float-policy precedence + delayed-flush compaction; do not shrink below 20 non-Docker environment files.

### Required artifacts

instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh, solution/oracle.patch, and the environment tree listed in Initial Draft Commitments.

### Test plan

- `test_crf_r1_table`: report shape; scenario ids match case_ids.txt
- `test_crf_r2_mirror`: paired echo lanes agree on seal_hex and closure fields when coherent
- `test_crf_r3_closure_flags`: coherent run — norm_skew 0 and three row closure fields true on all rows
- `test_crf_r4_summary_settled`: summary audit_status settled when matrix coherent
- `test_crf_r5_span`: policy_span equals max abs norm_skew; optimization target policy_span==0 when coherent
- `test_crf_r6_digest_rule`: summary policy_digest matches driver header reduction from rows
- `test_crf_r7_digest_anchor`: summary policy_digest matches known-good repaired emission
- `test_crf_r8_pattern_format`: seal_hex sixteen lowercase hex chars
- `test_crf_r9_rows_total`: rows_total integer equals len(rows)
- `test_crf_r10_overwrite`: tampered hand-written JSON replaced by pipeline rerun
- `test_crf_r11_idempotent`: consecutive pipeline runs identical
- `test_crf_r12_lowerdir_sensitivity`: mutating lowerdir step table changes seal_hex and policy_digest
- `test_crf_r13_fold_ablation`: reverting norm_fold lineage body breaks cross-runtime seal coherence
- `test_crf_r14_dual_ablation`: reverting ledger merge and norm_fold together breaks pipeline
- `test_crf_r15_order_ablation`: broken gate wiring + stock stride helper breaks compaction closure
- `test_crf_r16_ledger_trap`: echo lane cannot keep stale tolerance tier after ledger replay fixture
- `test_crf_r17_fastpath_trap`: forcing cat_lane-only emit breaks cross-format seal agreement
- `test_crf_r18_precedence_cli`: CLI mode overrides workspace tier for active scenario without breaking echo agreement when coherent
- `test_crf_r19_delayed_flush`: delayed-flush scenario requires side-before-gate ordering to reach audit_status settled
- `test_crf_r20_tolerance_band`: norm_skew zero only when subspace norm within documented strict-band ceiling for active tier

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests.

### Drafting guardrails

Instruction is constraint-complete: state the three obligations, numeric policy disclosures (metric, tolerance class, reproducibility), optimization target, and report contract without naming `norm_fold`, `ledger_merge`, `mux_seq`, replay phase, canonical recovery order, or fast-path module. Do not copy overlay “Repair sources” wording — use optimization language (“align sources so constraints hold”). Tests derive verdicts from regenerated JSON, ledger precedence traps, delayed-flush traps, tolerance-band checks, and ablations—not static answer keys.

### Triviality Ledger

- Hand-writing policy_audit_report.json fails `test_crf_r10_overwrite` because verifier reruns cargo + driver.
- Fixing only norm_fold without ledger_merge fails `test_crf_r14_dual_ablation` and mirror coherence subsets.
- Fixing only gate ordering without stride/gate contract fails `test_crf_r15_order_ablation` and `test_crf_r19_delayed_flush`.
- Satisfying runtime session cache while ignoring ledger precedence fails `test_crf_r16_ledger_trap`.
- Routing regeneration through cat_lane fast emit fails `test_crf_r17_fastpath_trap` even when row flags look green.
- Tweaking one tolerance constant without cross-surface precedence fails `test_crf_r18_precedence_cli` and `test_crf_r20_tolerance_band`.
- Copying reduction formula into one function without cross-format reducer fails `test_crf_r17_fastpath_trap` and `test_crf_r6_digest_rule`.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle patch must change semantics in three roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns listed in code_forbidden_tokens must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays constraint-complete about obligations and numeric policy, not cause-revealing (“ledger_merge omits storage”).
- RC5/RC6: schemas and policy_digest home in main.rs header + surface_contract.md; no boolean answer grid in instruction.
- RC7/GX3: oracle.patch coordinated across tie/hold/gate_mux with substantive bodies (same structural fixes as overlay reference: lineage fold, pack storage refresh, gate order invert).
- GX9/GX10: derived policy_digest and pair equality; no per-scenario expected literals in instruction.
- GX4/GX5: ablation tests patch sources in-container; expectations computed from contract functions in test file.
- hard_difficulty_predictor: ≥3 failure modes including replay semantics and cache invalidation; predicted_worst_model_pass_rate ≤20% (Rust task, no python_medium_blocker).
- Static: run `collapse_check.py --check flipping_point_compliance` and `grep_resistance` after Step 2b.

### Initial Draft Commitments

- tasks/cross-runtime-float-policy-drift-046/task.toml
- tasks/cross-runtime-float-policy-drift-046/instruction.md
- tasks/cross-runtime-float-policy-drift-046/output_contract.toml
- tasks/cross-runtime-float-policy-drift-046/construction_manifest.json
- tasks/cross-runtime-float-policy-drift-046/tests/test.sh
- tasks/cross-runtime-float-policy-drift-046/tests/test_outputs.py
- tasks/cross-runtime-float-policy-drift-046/solution/solve.sh
- tasks/cross-runtime-float-policy-drift-046/solution/oracle.patch
- tasks/cross-runtime-float-policy-drift-046/environment/Dockerfile
- tasks/cross-runtime-float-policy-drift-046/environment/Cargo.toml
- tasks/cross-runtime-float-policy-drift-046/environment/Cargo.lock
- tasks/cross-runtime-float-policy-drift-046/environment/m6/k86/Cargo.toml
- tasks/cross-runtime-float-policy-drift-046/environment/m6/k86/src/main.rs
- tasks/cross-runtime-float-policy-drift-046/environment/m6/k86/src/gate_mux.rs
- tasks/cross-runtime-float-policy-drift-046/environment/m6/k86/src/stack_mix.rs
- tasks/cross-runtime-float-policy-drift-046/environment/m6/k86/src/step_key.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/Cargo.toml
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/lib.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/mesh.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/family.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/row_help.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/norm_reduce.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/apply.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/probe.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/kind.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/stack.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/layer_core/src/alias_stub.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y4/Cargo.toml
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y4/src/lib.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y4/src/hold.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y4/src/body.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y4/src/shape.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y5/Cargo.toml
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y5/src/lib.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y5/src/tie.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y6/Cargo.toml
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y6/src/lib.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y6/src/stride.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y6/src/cat_lane.rs
- tasks/cross-runtime-float-policy-drift-046/environment/p8/y6/src/body.rs
- tasks/cross-runtime-float-policy-drift-046/environment/data/ladder.toml
- tasks/cross-runtime-float-policy-drift-046/environment/data/channel.toml
- tasks/cross-runtime-float-policy-drift-046/environment/data/seed.json
- tasks/cross-runtime-float-policy-drift-046/environment/data/weights.tsv
- tasks/cross-runtime-float-policy-drift-046/environment/data/base_defaults.toml
- tasks/cross-runtime-float-policy-drift-046/environment/data/ws_layer.toml
- tasks/cross-runtime-float-policy-drift-046/environment/data/notes.md
- tasks/cross-runtime-float-policy-drift-046/environment/docs/case_ids.txt
- tasks/cross-runtime-float-policy-drift-046/environment/docs/surface_contract.md
- tasks/cross-runtime-float-policy-drift-046/environment/docs/build_hints.txt

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p8/y5/src/tie.rs
  symbol: norm_fold
  kind: function
  signature: norm_fold(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Derives seal_hex material from step and cross-runtime profile tuple
- path: environment/p8/y4/src/hold.rs
  symbol: ledger_merge
  kind: function
  signature: ledger_merge(state: &mut PackState, incoming: &PackState, stamp_b: u64)
  purpose: Merges incoming durable pack into active state under ledger authority
- path: environment/m6/k86/src/gate_mux.rs
  symbol: mux_seq
  kind: function
  signature: mux_seq<F: FnMut(), G: FnMut()>(side: F, gate: G) -> u32
  purpose: Invokes side and gate callbacks in seeded combine order during delayed-flush replay
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p8/y5/src/tie.rs
    controls_tests: [test_crf_r2_mirror, test_crf_r13_fold_ablation, test_crf_r7_digest_anchor, test_crf_r16_ledger_trap]
  - id: B
    path: environment/p8/y4/src/hold.rs
    controls_tests: [test_crf_r14_dual_ablation, test_crf_r4_summary_settled, test_crf_r10_overwrite, test_crf_r16_ledger_trap]
  - id: C
    path: environment/m6/k86/src/gate_mux.rs
    controls_tests: [test_crf_r15_order_ablation, test_crf_r3_closure_flags, test_crf_r6_digest_rule, test_crf_r17_fastpath_trap, test_crf_r19_delayed_flush]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/p8/y6/src/cat_lane.rs
  kind: module
  rhymes_with: norm_reduce
  non_fix_purpose: Fast cat_lane emit used in fastpath trap; must not satisfy obligation 3 alone
- path: environment/p8/y6/src/stride.rs
  kind: helper
  rhymes_with: mux_seq
  non_fix_purpose: Alternate step_1 ordering helper used in ablation traps, not the fix path
- path: environment/p8/layer_core/src/probe.rs
  kind: helper
  rhymes_with: ledger_merge
  non_fix_purpose: Runtime-visible session cache for diagnostics; not durable ledger authority
- path: environment/p8/y5/src/stamp_help.rs
  kind: helper
  rhymes_with: norm_fold
  non_fix_purpose: Widening utilities for non-fix stamp experiments
```

#### code_forbidden_tokens

```
cross, runtime, drift, compaction, compact, flush, delayed, reconciliation, durable, authority, precedence, tolerance, tier, scenario, mirror, coherent, settled, ledger, session, override, workspace, cli, regen, pipeline, rounding, cache, checkpoint, recovery, partial, digest, sync, reducer, obligation, optimization, minimize, echo, incoherent, numeric, attestation, seal, gateway, hardened, attest, principal, asset, security, lowerdir, upper, worker, materialization, regeneration, merge, closure, emit, fastpath, cat_lane, subspace, strict, balanced, relaxed
```

### difficulty_mechanism_plan

- mechanisms: partial_observability_experiment_design, false_green_intermediate_states, environment_specific_cli_semantics, cross_file_cross_format_invariants, deceptive_but_valid_local_evidence, buried_local_constraints, stateful_multi_step_dependencies
- adversarial_layers_count: 7
- fairness_guardrails: All tested formulas, tolerance bands, and scenario ids are public; deterministic rebuild; no timing/latency thresholds
- mechanism: partial_observability_experiment_design
  placement: runtime session cache visible in driver diagnostics vs durable attest ledger bytes only in recovery fixtures
  why_model_misses_it: models treat live session cache as authoritative after partial recovery instead of ledger bytes
  fairness_guardrail: obligation 2 states ledger precedence explicitly
- mechanism: false_green_intermediate_states
  placement: per-row three closure booleans vs summary audit_status during delayed-flush replay ordering
  why_model_misses_it: agents stop after row-level greens without mirror/policy_digest cross-check
  fairness_guardrail: mirror pairs and policy_digest contract are in instruction and surface_contract.md
- mechanism: environment_specific_cli_semantics
  placement: driver argv modes select which config surfaces participate before compaction scoring
  why_model_misses_it: default mode hides workspace/env conflicts until echo-lane mode runs
  fairness_guardrail: surface_contract.md documents modes without naming internal functions
- mechanism: cross_file_cross_format_invariants
  placement: JSON report vs TOML ladder vs ledger pack bytes must agree on seal_hex linkage
  why_model_misses_it: editing one format leaves orphans that still pass shallow row flags
  fairness_guardrail: cross-format rules in surface_contract.md with worked examples
- mechanism: deceptive_but_valid_local_evidence
  placement: cat_lane fast emit vs norm_reduce slow reducer; runtime cache shows coherent tolerance tier locally
  why_model_misses_it: summary looks settled while seal_hex diverges on echo lanes
  fairness_guardrail: obligation 3 and cross-lane tests
- mechanism: buried_local_constraints
  placement: norm_fold must include prev_family shift, not step_ix alone, for cross-runtime seal material
  why_model_misses_it: looks like optional lineage field
  fairness_guardrail: ablation test reverts norm_fold body
- mechanism: stateful_multi_step_dependencies
  placement: ladder.toml scenarios spanning delayed flush, ledger replay, then echo lanes
  why_model_misses_it: fixing one lane table without merge ordering leaves policy drift
  fairness_guardrail: deterministic case_ids.txt

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert can satisfy three obligations, numeric policy disclosures, and optimization target using surface_contract.md and regenerated report within a few hours
- shortcut_audit: static JSON, test deletion, stale-doc-only edits, reward file writes, digest hardcoding, single-surface precedence table copy, one-constant tolerance tweak
- ablation_plan: revert norm_fold only, ledger_merge only, mux_seq only — each should drop pass rate on disjoint test subsets
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
