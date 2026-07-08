### Decision

GO — Attempt 1. Bank-ready seed validated on the approved `overlay-lowerdir-stale-bind` construction mold (`accepted tasks/_ref/overlay-lowerdir-stale-bind/` / `overlay-lowerdir-stale-bind.zip`), reframed to `scientific-computing` + `optimization_under_constraints` + `security_authority_split` with **numeric cache invalidation divergence after namespace-restore replay loops**. Three mandated discoveries, three coordinated implementation topologies, overlay-style flipping-point ablations, and constraint-complete public obligations without leaking canonical recovery path, replay phase, or reconciliation authority.

### Metadata

- version: 2
- Task name: namespace-restore-replay-loop-028
- Title: Namespace restore replay cycles
- Category: scientific-computing
- Task shape: optimization_under_constraints
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["scientific-computing", "namespace-restore", "cache-invalidation", "authority-split", "replay-loop", "optimization"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract

After namespace-restore cycles, local cache probes and row closure flags can look coherent while echo lanes still carry stale invalidation generations once the replay loop finishes. Summary loop_status may disagree with mirror pairs until the obligations below hold.

Repair sources under `/app` so the workspace release build and `/app/target/release/mk` write `/app/output/restore_loop_report.json`. Scenario ids are in `/app/docs/cycle_ids.txt`.

The report has rows and summary. Each row records scenario_id, three per-row closure booleans, skew_code, and cache_key_hex (exactly 16 lowercase hexadecimal digits). The summary records rows_total, loop_status, invalidation_span, and loop_digest. Mirror pairs are lowerdir with lowerdir_echo, upper with upper_echo, and worker with worker_echo. Coherent runs keep skew_code at 0 on every row, all three closure booleans true, matching cache_key_hex on each pair, and loop_status reading settled. Incoherent runs break at least one of those conditions (closure booleans may read false or loop_status may differ from settled). The module comment above /app/m2/k81/src/main.rs defines invalidation_span and loop_digest reduction; read that header instead of hand-writing JSON. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See visible argv documentation for verifier command details.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category_profile = "security_authority_split"`
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

- path: environment/Dockerfile
  role: build definition; pre-install cargo, pytest, and locked toolchain
- path: environment/m2/k81/src/main.rs
  role: scenario-matrix driver emitting restore_loop_report.json; documents loop_digest and invalidation_span
- path: environment/m2/k81/src/gate_mux.rs
  role: oracle frontier C — combine ordering for replay side vs invalidation gate callbacks
- path: environment/m2/k81/src/stack_mix.rs
  role: ladder application glue coupling numeric packs to lane material
- path: environment/m2/k81/src/step_key.rs
  role: decoy per-step key helper co-resident with driver crate (non-fix)
- path: environment/p7/y4/src/hold.rs
  role: oracle frontier B — durable pack merge refresh under checkpoint invalidation rules
- path: environment/p7/y4/src/lib.rs
  role: y4 crate root exports (co-resident with hold.rs)
- path: environment/p7/y4/src/body.rs
  role: counter helpers co-resident with hold.rs (non-fix)
- path: environment/p7/y4/src/shape.rs
  role: dimension checks co-resident with hold.rs (non-fix)
- path: environment/p7/y5/src/tie.rs
  role: oracle frontier A — generation fold for cache_key_hex material
- path: environment/p7/y5/src/lib.rs
  role: y5 crate root exports (co-resident with tie.rs)
- path: environment/p7/y5/src/body.rs
  role: bitmask helpers co-resident with tie.rs (non-fix)
- path: environment/p7/layer_core/src/inv_stamp.rs
  role: slow cross-format invalidation reducer (required regeneration path)
- path: environment/docs/phase_rules.md
  role: internal contract doc for invalidation closure and authority split rules

### fix_frontier

- count: 3
- distribution: `environment/p7/y5/src/tie.rs`, `environment/p7/y4/src/hold.rs`, `environment/m2/k81/src/gate_mux.rs` (distinct crate roots under p7 and m2)
- naming_policy: Keep opaque Rust identifiers on the fix path (`key_fold`, `pack_sync`, `loop_order`); do not rename to instruction nouns
- forbidden_stems: namespace, restore, replay, loop, cache, invalidation, divergence, numeric, durable, runtime, authority, partial, recovery, checkpoint, probe, regeneration, cross, format, invariant, enforcement, mirror, echo, coherent, settled, span, digest, scenario, obligation, optimization, workspace, driver, report, closure, lane, material, generation, partition, skew, settled, loop_status, invalidation_span, loop_digest, cache_key, merge, sync, fold, slot, reducer, scientific, computing, cluster, cycle, diagnostics, override, marks, re-materialize, pipeline, align, sources, release, build, published, write, output, static, manual, verifier, rebuild, fixed, pytest, cargo, argv, hints, ablation, patch, oracle, apply, locked, toolchain, metadata, internet, false, green, intermediate, corruption, ordering, bypass, silently, visible, checks, locally, hidden, invariants, fail, restart, reconciliation, surfaces, destructive, cause, revealing, canonical, path, phase, reconciliation
- helpers_policy: Co-resident crate roots and rhyming decoys perform credible adjacent work; `step_key.rs`, y4/y5 `lib.rs`/`body.rs`/`shape.rs` are declared co-resident helpers; frontier stays thin at three fix symbols
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: loop_digest recomputation, cache_key_hex mirror pairs, namespace-restore replay traps, ablation incoherence, pipeline overwrite trap, consecutive run identity, cross-format invalidation agreement, checkpoint authority derivation
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction.md; per-scenario answer rows in docs; boolean answer-key JSON fields named `overall_pass` or `scenario_pass`

### task_shape

- type: optimization_under_constraints
- instruction_framing: constraint-complete
- hardness_source: constrained optimization — satisfy multi-surface authority split and invalidation-settled coherence under replay loops without naming which merge rule, combine ordering, or emit path is defective
- collapse_risk: leaking canonical recovery path, replay phase, or reconciliation authority collapses to localized one-file repair

### category_profile

- challenge_family: numeric_cache_invalidation_divergence
- profile_name: security_authority_split
- allowed_instruction_disclosures: assets (numeric generations, invalidation marks), allowed/denied materialization outcomes, audit/driver command, authority boundary between checkpoint bytes and runtime probes, three obligations, optimization target (invalidation_span zero + loop_status settled), report schema, mirror pairs, loop_digest definition header, deterministic rerun requirement
- forbidden_instruction_leaks: vulnerable sink location, trust-boundary implementation file, exploit primitive, patch rule, sanitizer name, exact guard function, which module is canonical by default, replay phase ordering bug description, fast-path bypass file name
- category_specific_hardness_bar: encode/decode/enforce authorities must reconcile across changing generations, freshness, and invalidation under namespace-restore replay loops; at least two partitions and two evidence surfaces with invalidation lineage
- category_specific_verifier_risks: toy checklist, blocklist bypass, one exploit-string test, process-only assertions without durable invalidation checks, golden report leakage
- coverage_role: Adds scientific-computing optimization_under_constraints coverage under security_authority_split distinct from formal_reasoning revocation-cache-authority-split-012 and config_policy_precedence cross-runtime-float-policy-drift-016

### satisfiability_risk

- rc2_planned_name_risk: medium — instruction uses domain nouns; fix path stays opaque neutral crate paths (m2/p7) with `key_fold` / `pack_sync` / `loop_order`
- gx9_contract_risk: low — loop_digest derived from rows; per-row booleans are product-shaped closure fields documented in instruction
- cr1_symbol_frontier_risk: low — three substantive Rust modules plus distributed layer_core support
- hidden_contract_risk: medium — false-green row flags vs summary loop_status during replay ordering require ablation tests; mitigated by loop_contract.md and main.rs header

### actionability_plan

- verifier_command_visible: `cargo build --release --locked` from `/app` and driver at `/app/target/release/mk`; pytest via `/opt/verifier-venv` per build_hints.txt
- source_fix_intent_visible: instruction requires aligning sources to satisfy three obligations and optimization target; does not name `key_fold`, `pack_sync`, or `loop_order`
- generated_output_rule_visible: `/app/output/restore_loop_report.json` path and field names
- exact_formula_home: module comment above `environment/m2/k81/src/main.rs` plus `environment/docs/loop_contract.md` (skew_code bands, loop_digest reduction, subspace norm threshold 1e-2 for skew_code zero when documented)
- schema_home: instruction.md public contract + output_contract.toml paths

### waiver_plan

- waivers_expected: no
- waiver_rationale: Overlay mold demonstrates RC2-safe naming; regeneration, flipping-point, authority-split, and replay-loop tests avoid hidden-instance puzzles

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/_ref/overlay-lowerdir-stale-bind/` (`overlay-lowerdir-stale-bind.zip`) for verifier shape, flipping-point ablations, pipeline traps, and pytest ablation patterns; reframed to scientific-computing + security_authority_split + optimization_under_constraints with namespace-restore replay-loop and numeric cache invalidation vocabulary. No promoted `docs/reference_tasks/index.json` entry matches this exact profile combo.

### realism_source

- source_type: synthetic_exception
- evidence_basis: Minimized from HPC / simulation control planes where numeric cache layers, runtime probes, and checkpoint bytes disagree after namespace restore and replay-loop recovery
- upstream_or_synthetic_rationale: Controlled false-green intermediate verifier state with deterministic replay — avoids hidden-instance “which file is corrupt” puzzles while preserving real authority-split + cache-invalidation coupling
- minimization_preserves: Split authority surfaces (runtime probes vs durable checkpoint), false-green intermediate verifier state after replay ordering, fast-path regeneration bypass of cross-format invalidation reducer
- synthetic_exception_review: Difficulty from coupled authority/invalidation semantics and constraint-complete optimization target, not obscure facts; decoys perform real non-fix work

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, rollback_recovery_requirements, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, partial_observability_experiment_design, buried_local_constraints, stateful_multi_step_dependencies
- adversarial_layers_count: 7
- fairness_guardrails: All tested formulas and scenario ids are public; deterministic rebuild; no timing/latency thresholds
- mechanism: false_green_intermediate_states
  placement: per-row three closure booleans vs summary loop_status during replay-loop ordering
  why_model_misses_it: agents stop after row-level greens without mirror/loop_digest cross-check
  fairness_guardrail: mirror pairs and loop_digest contract are in instruction and loop_contract.md
- mechanism: rollback_recovery_requirements
  placement: ladder.toml scenarios spanning namespace restore, checkpoint replay, then echo lanes
  why_model_misses_it: fixing one lane table without merge ordering leaves stale generations on echo partitions
  fairness_guardrail: deterministic cycle_ids.txt
- mechanism: deceptive_but_valid_local_evidence
  placement: slot_emit fast emit vs inv_stamp slow reducer; runtime probe shows coherent generation locally
  why_model_misses_it: summary looks settled while cache_key_hex diverges on echo lanes
  fairness_guardrail: obligation 3 and cross-lane tests
- mechanism: cross_file_cross_format_invariants
  placement: JSON report vs TOML ladder/checkpoint vs pack bytes must agree on cache_key_hex linkage
  why_model_misses_it: editing one format leaves orphans that still pass shallow row flags
  fairness_guardrail: cross-format rules in loop_contract.md with worked examples
- mechanism: partial_observability_experiment_design
  placement: runtime probe surface vs durable checkpoint visible in different fixtures
  why_model_misses_it: models treat probe stream as authoritative after partial recovery
  fairness_guardrail: obligation 2 states checkpoint precedence explicitly
- mechanism: buried_local_constraints
  placement: key_fold must include prev_family shift, not step_ix alone, for cross-partition cache_key material
  why_model_misses_it: looks like optional lineage field
  fairness_guardrail: ablation test reverts key_fold body
- mechanism: stateful_multi_step_dependencies
  placement: driver argv modes select which surfaces participate before loop_status scoring
  why_model_misses_it: default mode hides checkpoint/probe conflicts until echo-lane mode runs
  fairness_guardrail: loop_contract.md documents modes without naming internal functions

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert can satisfy three obligations and optimization target using loop_contract.md and regenerated report within a few hours
- shortcut_audit: static JSON, test deletion, stale-doc-only edits, reward file writes, digest hardcoding, single-surface invalidation table copy
- ablation_plan: revert key_fold only, pack_sync only, loop_order only — each should drop pass rate on disjoint test subsets
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

Numeric cache invalidation divergence appears when three authorities disagree: runtime-visible cache probes, durable checkpoint bytes replayed after partial namespace restore, and replay-ordered lane emission after a **restore replay loop**. Local row-level closure flags and probe diagnostics can read coherent while echo lanes re-materialize stale invalidation generations and a fast slot regeneration path skips the slow cross-format reducer—producing a green intermediate verifier state that masks corruption until full pipeline replay. Hardness requires reconciling authority split, invalidation materialization, and loop-settled coherence under the three public obligations and invalidation_span optimization target without the instruction naming which merge rule, which combine ordering, or which emit path is defective.

### Environment shape

Rust Cargo workspace under `/app` forked from the overlay reference mold: driver crate `m2/k81`, pack crates `p7/y4`–`y6`, shared `p7/layer_core`. Fixtures under `environment/data/` (`checkpoint.toml`, `seed.json`, `ladder.toml`). Contract in `environment/docs/loop_contract.md`. Output at `/app/output/restore_loop_report.json`. Step 2b may fork `accepted tasks/_ref/overlay-lowerdir-stale-bind/environment/` then reframe docs, field names, and broken semantics for namespace-restore replay loops + numeric cache invalidation; do not shrink below 20 non-Docker environment files.

### Required artifacts

instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh, solution/oracle.patch, and the environment tree listed in Initial Draft Commitments.

### Test plan

- `test_nrl_r1_table`: report shape; scenario ids match cycle_ids.txt
- `test_nrl_r2_pair`: paired echo lanes agree on cache_key_hex and closure fields when coherent
- `test_nrl_r3_m1_flags`: coherent run — skew_code 0 and three row closure fields true on all rows
- `test_nrl_r4_m2_label`: summary loop_status settled when matrix coherent
- `test_nrl_r5_m3_zero`: invalidation_span equals max abs skew_code; optimization target invalidation_span==0 when coherent
- `test_nrl_r6_m4_rule`: summary loop_digest matches driver header reduction from rows
- `test_nrl_r7_m5_anchor`: summary loop_digest matches known-good repaired emission
- `test_nrl_r8_m6_chars`: cache_key_hex sixteen lowercase hex chars
- `test_nrl_r9_m8_count`: rows_total integer equals len(rows)
- `test_nrl_r10_m10_fresh`: tampered hand-written JSON replaced by pipeline rerun
- `test_nrl_r11_m9_twice`: consecutive pipeline runs identical
- `test_nrl_r12_m7_shift`: mutating lowerdir step table changes cache_key_hex and loop_digest
- `test_nrl_r13_p1_fold`: reverting key_fold lineage body breaks cross-partition cache_key coherence
- `test_nrl_r14_p2_dual`: reverting pack sync and key_fold together breaks pipeline
- `test_nrl_r15_p3_combo`: broken gate wiring + stock stride helper breaks loop closure
- `test_nrl_r16_k7_trap`: echo lane cannot keep stale generation after durable-bytes replay fixture
- `test_nrl_r17_k8_trap`: forcing slot_emit-only emit breaks cross-format invalidation agreement
- `test_nrl_r18_k9_side`: namespace-restore scenario requires side-before-gate ordering to reach loop_status settled
- `test_nrl_r19_m1_view`: runtime diagnostics may differ from durable marks without breaking echo agreement when coherent

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests.

### Drafting guardrails

Instruction is constraint-complete: state the three obligations, optimization target, and report contract without naming `key_fold`, `pack_sync`, `loop_order`, replay phase, canonical recovery order, or fast-path module. Do not copy overlay “Repair sources” wording — use optimization language (“align sources so constraints hold”). Tests derive verdicts from regenerated JSON, checkpoint precedence traps, restore-loop traps, and ablations—not static answer keys.

### Triviality Ledger

- Hand-writing restore_loop_report.json fails `test_nrl_r10_m10_fresh` because verifier reruns cargo + driver.
- Fixing only key_fold without pack_sync fails `test_nrl_r14_p2_dual` and mirror coherence subsets.
- Fixing only gate ordering without stride/gate contract fails `test_nrl_r15_p3_combo` and `test_nrl_r18_k9_side`.
- Satisfying runtime probes while ignoring durable-bytes precedence fails `test_nrl_r16_k7_trap`.
- Routing regeneration through slot_emit fast emit fails `test_nrl_r17_k8_trap` even when row flags look green.
- Widening invalidation windows in one TOML file alone fails echo-pair and loop_digest tests until cross-crate coordination.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle patch must change semantics in three roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns listed in code_forbidden_tokens must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays constraint-complete about obligations, not cause-revealing (“pack_sync omits storage”).
- RC5/RC6: schemas and loop_digest home in main.rs header + loop_contract.md; no boolean answer grid in instruction.
- RC7/GX3: oracle.patch coordinated across tie/hold/gate_mux with substantive bodies (lineage fold, pack storage refresh, gate order invert — same structural fixes as overlay reference).
- GX9/GX10: derived loop_digest and pair equality; no per-scenario expected literals in instruction.
- GX4/GX5: ablation tests patch sources in-container; expectations computed from contract functions in test file.
- Static: run `collapse_check.py --check flipping_point_compliance` and `grep_resistance` after Step 2b.

### Initial Draft Commitments

- tasks/namespace-restore-replay-loop-028/task.toml
- tasks/namespace-restore-replay-loop-028/instruction.md
- tasks/namespace-restore-replay-loop-028/output_contract.toml
- tasks/namespace-restore-replay-loop-028/construction_manifest.json
- tasks/namespace-restore-replay-loop-028/tests/test.sh
- tasks/namespace-restore-replay-loop-028/tests/test_outputs.py
- tasks/namespace-restore-replay-loop-028/solution/solve.sh
- tasks/namespace-restore-replay-loop-028/solution/oracle.patch
- tasks/namespace-restore-replay-loop-028/environment/Dockerfile
- tasks/namespace-restore-replay-loop-028/environment/Cargo.toml
- tasks/namespace-restore-replay-loop-028/environment/Cargo.lock
- tasks/namespace-restore-replay-loop-028/environment/m2/k81/Cargo.toml
- tasks/namespace-restore-replay-loop-028/environment/m2/k81/src/main.rs
- tasks/namespace-restore-replay-loop-028/environment/m2/k81/src/gate_mux.rs
- tasks/namespace-restore-replay-loop-028/environment/m2/k81/src/stack_mix.rs
- tasks/namespace-restore-replay-loop-028/environment/m2/k81/src/step_key.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/Cargo.toml
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/lib.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/mesh.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/family.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/row_help.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/inv_stamp.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/apply.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/probe.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/kind.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/stack.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/layer_core/src/alias_stub.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y4/Cargo.toml
- tasks/namespace-restore-replay-loop-028/environment/p7/y4/src/lib.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y4/src/hold.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y4/src/body.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y4/src/shape.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y5/Cargo.toml
- tasks/namespace-restore-replay-loop-028/environment/p7/y5/src/lib.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y5/src/tie.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y5/src/body.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y5/src/stamp_help.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y6/Cargo.toml
- tasks/namespace-restore-replay-loop-028/environment/p7/y6/src/lib.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y6/src/stride.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y6/src/slot_emit.rs
- tasks/namespace-restore-replay-loop-028/environment/p7/y6/src/body.rs
- tasks/namespace-restore-replay-loop-028/environment/data/ladder.toml
- tasks/namespace-restore-replay-loop-028/environment/data/channel.toml
- tasks/namespace-restore-replay-loop-028/environment/data/seed.json
- tasks/namespace-restore-replay-loop-028/environment/data/weights.tsv
- tasks/namespace-restore-replay-loop-028/environment/data/checkpoint.toml
- tasks/namespace-restore-replay-loop-028/environment/data/notes.md
- tasks/namespace-restore-replay-loop-028/environment/docs/cycle_ids.txt
- tasks/namespace-restore-replay-loop-028/environment/docs/loop_contract.md
- tasks/namespace-restore-replay-loop-028/environment/docs/build_hints.txt

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p7/y5/src/tie.rs
  symbol: key_fold
  kind: function
  signature: key_fold(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Derives cache_key_hex material from step and cross-partition generation tuple
- path: environment/p7/y4/src/hold.rs
  symbol: pack_sync
  kind: function
  signature: pack_sync(state: &mut PackState, incoming: &PackState, stamp_b: u64)
  purpose: Merges incoming durable pack into active state under checkpoint authority
- path: environment/m2/k81/src/gate_mux.rs
  symbol: loop_order
  kind: function
  signature: loop_order<F: FnMut(), G: FnMut()>(side: F, gate: G) -> u32
  purpose: Invokes side and gate callbacks in seeded combine order during restore replay loops
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p7/y5/src/tie.rs
    controls_tests: [test_nrl_r1_table, test_nrl_r2_pair, test_nrl_r8_m6_chars, test_nrl_r12_m7_shift, test_nrl_r13_p1_fold, test_nrl_r7_m5_anchor, test_nrl_r16_k7_trap]
  - id: B
    path: environment/p7/y4/src/hold.rs
    controls_tests: [test_nrl_r5_m3_zero, test_nrl_r9_m8_count, test_nrl_r14_p2_dual, test_nrl_r4_m2_label, test_nrl_r10_m10_fresh, test_nrl_r16_k7_trap]
  - id: C
    path: environment/m2/k81/src/gate_mux.rs
    controls_tests: [test_nrl_r11_m9_twice, test_nrl_r19_m1_view, test_nrl_r15_p3_combo, test_nrl_r3_m1_flags, test_nrl_r6_m4_rule, test_nrl_r17_k8_trap, test_nrl_r18_k9_side]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/p7/y6/src/slot_emit.rs
  kind: module
  rhymes_with: inv_stamp
  non_fix_purpose: Fast slot emit used in fastpath trap; must not satisfy obligation 3 alone
- path: environment/p7/y6/src/stride.rs
  kind: helper
  rhymes_with: loop_order
  non_fix_purpose: Alternate step_1 ordering helper used in ablation traps, not the fix path
- path: environment/p7/layer_core/src/probe.rs
  kind: helper
  rhymes_with: pack_sync
  non_fix_purpose: Runtime-visible cache probe for diagnostics; not durable checkpoint authority
- path: environment/p7/y5/src/stamp_help.rs
  kind: helper
  rhymes_with: key_fold
  non_fix_purpose: Widening utilities for non-fix stamp experiments
```

#### code_forbidden_tokens

```
namespace, restore, replay, cache, invalidation, divergence, numeric, durable, runtime, authority, partial, recovery, checkpoint, probe, regeneration, cross, invariant, enforcement, mirror, echo, coherent, settled, span, digest, scenario, obligation, optimization, cluster, partition, generation, skew, loop_status, invalidation_span, loop_digest, cache_key, pipeline, lowerdir, upper, worker, closure, lane, material, diagnostics, override, marks, reconciliation, canonical, bypass, corruption, intermediate, green, visible, locally, hidden, surfaces, align, sources, release, published, static, manual, verifier, rebuild, reducer, fold, sync, merge, re-materialize, incoherent, hexadecimal, rows, summary, rows_total, skew_code, cache_key_hex, restore_loop, tampered, idempotent, consecutive, ladder, channel, weights, seed, notes, ablation, patch, oracle, workspace, driver, report, scientific, computing, cross_format, slot_emit, inv_stamp, pack_sync, key_fold, loop_order, gate_mux, layer_core, restore_loop_report, checkpoint_toml
```
