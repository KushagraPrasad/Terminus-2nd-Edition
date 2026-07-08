### Decision

GO — Attempt 1. Bank-ready seed validated on the approved `overlay-lowerdir-stale-bind` construction mold, reframed to `formal_reasoning` + `scientific-computing` + `security_authority_split` with cross-node tombstone resurrection topology. Three non-trivial discoveries, three coordinated fix topologies, overlay-style flipping-point ablations, and constraint-complete public obligations without leaking canonical recovery path, replay phase, or reconciliation authority.

### Metadata

- version: 2
- Task name: revocation-cache-authority-split-012
- Title: Cache authority split report
- Category: scientific-computing
- Task shape: formal_reasoning
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["scientific-computing", "revocation", "tombstone", "authority", "witness", "replay"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract

A partitioned scientific cache cluster exposes two evidence surfaces after partial recovery: a runtime-visible revocation probe stream and a durable checkpoint journal replayed offline. Local per-node checks can read coherent while cross-node tombstone resurrection reappears in echo lanes after deterministic replay. The agent must align sources under `/app` so a release workspace build and the published driver write `/app/output/authority_lane_report.json`. Scenario ids are listed in `/app/docs/case_ids.txt`.

**Formal obligations** (also summarized in `/app/docs/lane_contract.md`; full derivation rules in the module comment above `/app/m2/k81/src/main.rs`):

1. **Tombstone non-resurrection:** once a principal epoch is tombstoned on any node, no replay or merge step may re-materialize that epoch in any lane or echo lane.
2. **Authority precedence:** after partial recovery, durable journal bytes are the sole authority for merge decisions; runtime probe snapshots may inform diagnostics but must not override journal tombstones.
3. **Witness closure:** every regeneration path must pass the slow cross-format witness reducer; no fast emit path may emit row-level witness flags without the same reducer used for summary `bundle_digest`.

The report has rows and summary with per-row closure fields, lag_code, and sixteen-digit hex lane material documented in `/app/docs/lane_contract.md`. Mirror pairs are lowerdir with lowerdir_echo, upper with upper_echo, and worker with worker_echo. Coherent runs keep lag_code at 0 on every row, all three per-row closure fields true, matching hex lane material on each pair, and consensus_status reading settled. Incoherent runs break at least one of those conditions. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_hints.txt` for cargo and pytest argv details.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category_profile = "security_authority_split"`
- path: instruction.md
  role: natural public task prompt (constraint-complete formal obligations; must not name patch sites or canonical recovery order)
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
  role: scenario-matrix driver emitting authority_lane_report.json
- path: environment/m2/k81/src/gate_mux.rs
  role: oracle frontier C — combine ordering for witness gate vs side callbacks
- path: environment/m2/k81/src/stack_mix.rs
  role: ladder application glue (non-fix but coupled)
- path: environment/m2/k81/src/step_key.rs
  role: per-step key material
- path: environment/p7/layer_core/Cargo.toml
  role: shared core crate
- path: environment/p7/layer_core/src/lib.rs
  role: core exports
- path: environment/p7/layer_core/src/mesh.rs
  role: mesh view helpers
- path: environment/p7/layer_core/src/family.rs
  role: family specs for lanes
- path: environment/p7/layer_core/src/row_help.rs
  role: hex16 formatting helper
- path: environment/p7/layer_core/src/emit_layer.rs
  role: lane line emission (slow witness path)
- path: environment/p7/layer_core/src/apply.rs
  role: numeric mix helpers (decoy-adjacent)
- path: environment/p7/layer_core/src/kind.rs
  role: kind tagging
- path: environment/p7/layer_core/src/stack.rs
  role: frame stack helpers
- path: environment/p7/layer_core/src/alias_stub.rs
  role: linear algebra stub (non-fix)
- path: environment/p7/y4/Cargo.toml
  role: pack merge crate (durable journal authority)
- path: environment/p7/y4/src/hold.rs
  role: oracle frontier B — durable pack merge refresh under tombstone rules
- path: environment/p7/y4/src/lib.rs
  role: y4 exports
- path: environment/p7/y4/src/body.rs
  role: counter helpers
- path: environment/p7/y4/src/shape.rs
  role: dimension checks
- path: environment/p7/y5/Cargo.toml
  role: fold material crate
- path: environment/p7/y5/src/tie.rs
  role: oracle frontier A — lineage fold for witness_hex material
- path: environment/p7/y5/src/lib.rs
  role: y5 exports
- path: environment/p7/y5/src/body.rs
  role: bitmask helpers
- path: environment/p7/y5/src/stamp_help.rs
  role: widen helpers (decoy)
- path: environment/p7/y6/Cargo.toml
  role: stride/catalog crate (fast-path trap surface)
- path: environment/p7/y6/src/stride.rs
  role: decoy rhyming with gate ordering (shipped broken ordering helper for ablation)
- path: environment/p7/y6/src/catalog.rs
  role: decoy fast catalog emit rhyming with emit_layer (non-fix regeneration shortcut)
- path: environment/p7/y6/src/lib.rs
  role: y6 exports
- path: environment/p7/y6/src/body.rs
  role: clip helpers
- path: environment/data/ladder.toml
  role: per-scenario replay tables (partition heal + tombstone echo lanes)
- path: environment/data/channel.toml
  role: channel weights
- path: environment/data/seed.json
  role: seeded principal epoch fixtures
- path: environment/data/weights.tsv
  role: weight table for core mix
- path: environment/data/notes.md
  role: operator notes (no fix recipe)
- path: environment/docs/case_ids.txt
  role: comma-separated scenario ids (mirror triple + base scenarios)
- path: environment/docs/lane_contract.md
  role: formal obligation restatement, cross-format witness rules, CLI semantics
- path: environment/docs/build_hints.txt
  role: cargo/pytest argv and ablation path hints (paths only, not fixes)
- path: solution/oracle.patch
  role: unified diff applied by solve.sh

### fix_frontier

- count: 3
- distribution: `environment/p7/y5/src/tie.rs`, `environment/p7/y4/src/hold.rs`, `environment/m2/k81/src/gate_mux.rs` (distinct crate roots under p7 and m2)
- naming_policy: Keep opaque Rust identifiers on the fix path (`fold_key`, `merge_pack`, `mux_combine`); do not rename to instruction nouns
- forbidden_stems: revocation, cache, authority, tombstone, resurrection, witness, principal, epoch, node, partition, durable, runtime, verifier, replay, regeneration, cluster, manifest, obligation, consensus, settled, bundle, align, probe, journal, checkpoint, offline, merge, echo, coherent, incoherent, formal
- helpers_policy: `catalog.rs`, `stride.rs`, `stamp_help.rs`, `probe.rs`, `alias_stub.rs` are decoys or non-fix helpers declared in decoy_manifest
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: bundle_digest recomputation, witness_hex mirror pairs, tombstone resurrection traps, ablation incoherence, pipeline overwrite trap, consecutive run identity, cross-format witness agreement
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction.md; per-scenario answer rows in docs; boolean answer-key JSON fields named `overall_pass` or `scenario_pass`

### task_shape

- type: formal_reasoning
- instruction_framing: constraint-complete
- hardness_source: formal correctness — reconcile split encode/decode/enforce authorities under tombstone replay without naming which surface is canonical by default
- collapse_risk: leaking canonical recovery path, replay phase, or reconciliation authority collapses to localized one-file repair

### category_profile

- challenge_family: cross_node_tombstone_resurrection
- profile_name: security_authority_split
- allowed_instruction_disclosures: assets (principal epochs, tombstones), allowed/denied materialization outcomes, audit/driver command, authority boundary between journal and probes, formal obligations, report schema, mirror pairs, bundle_digest definition header, deterministic rerun requirement
- forbidden_instruction_leaks: vulnerable sink location, trust-boundary implementation file, exploit primitive, patch rule, sanitizer name, exact guard function, which module is canonical by default, replay phase ordering bug description, fast-path bypass file name
- category_specific_hardness_bar: encode/decode/enforce authorities must reconcile across changing principals, freshness, and revocation under cross-node replay; at least two principals and two evidence surfaces with tombstone lineage
- category_specific_verifier_risks: toy checklist, blocklist bypass, one exploit-string test, process-only assertions without durable tombstone checks, golden report leakage
- coverage_role: Adds scientific-computing formal_reasoning coverage under security_authority_split distinct from repair-shaped revocation-cache-split-brain and reverse_engineering archive-repair

### satisfiability_risk

- rc2_planned_name_risk: medium — instruction uses domain nouns; fix path stays opaque neutral crate paths (m2/p7)
- gx9_contract_risk: low — bundle_digest derived from rows; per-row booleans are product-shaped witness fields documented in instruction
- cr1_symbol_frontier_risk: low — three substantive Rust modules plus distributed layer_core support
- hidden_contract_risk: medium — false-green row witness flags vs summary consensus require ablation tests; mitigated by lane_contract.md and main.rs header

### actionability_plan

- verifier_command_visible: `cargo build --release --locked` from `/app` and driver at `/app/target/release/mk`; pytest via `/opt/verifier-venv` per build_hints.txt
- source_fix_intent_visible: instruction requires aligning sources to satisfy formal obligations; does not name `fold_key`, `merge_pack`, or `mux_combine`
- generated_output_rule_visible: `/app/output/authority_lane_report.json` path and field names
- exact_formula_home: module comment above `environment/m2/k81/src/main.rs` plus `environment/docs/lane_contract.md`
- schema_home: instruction.md public contract + output_contract.toml paths

### waiver_plan

- waivers_expected: no
- waiver_rationale: Overlay mold demonstrates RC2-safe naming; regeneration, flipping-point, and formal-obligation tests avoid hidden-instance puzzles

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/_ref/overlay-lowerdir-stale-bind/` (`overlay-lowerdir-stale-bind.zip`) for verifier shape, flipping-point ablations, pipeline traps, and pytest ablation patterns; reframed to scientific-computing + security_authority_split + formal_reasoning with tombstone/witness vocabulary. No promoted `docs/reference_tasks/index.json` entry matches this exact profile combo.

### realism_source

- source_type: synthetic_exception
- evidence_basis: Minimized from distributed cache revocation postmortems where runtime probes green-light while durable journals resurrect tombstoned epochs after replay reordering
- upstream_or_synthetic_rationale: Controlled cross-node tombstone resurrection with deterministic replay — avoids hidden-instance “which file is corrupt” puzzles
- minimization_preserves: Split authority surfaces, false-green intermediate verifier state, fast-path regeneration bypass of cross-format witnesses
- synthetic_exception_review: Difficulty from coupled authority/witness semantics and formal obligations, not obscure facts; decoys perform real non-fix work

### difficulty_mechanism_plan

- mechanisms: stateful_multi_step_dependencies, false_green_intermediate_states, cross_file_cross_format_invariants, partial_observability_experiment_design, deceptive_but_valid_local_evidence, buried_local_constraints
- adversarial_layers_count: 6
- fairness_guardrails: All tested formulas and scenario ids are public; deterministic rebuild; no timing/latency thresholds
- mechanism: stateful_multi_step_dependencies
  placement: ladder.toml scenarios spanning partition heal, journal replay, then echo lanes
  why_model_misses_it: fixing one lane table without merge ordering leaves echo tombstone resurrection
  fairness_guardrail: deterministic case_ids.txt
- mechanism: false_green_intermediate_states
  placement: per-row closure fields vs summary consensus_status during replay ordering
  why_model_misses_it: agents stop after row-level greens without mirror/bundle_digest cross-check
  fairness_guardrail: mirror pairs and bundle_digest contract are in instruction and lane_contract.md
- mechanism: cross_file_cross_format_invariants
  placement: JSON report vs TOML ladder vs journal pack bytes must agree on witness_hex linkage
  why_model_misses_it: editing one format leaves orphans that still pass shallow row flags
  fairness_guardrail: cross-format rules in lane_contract.md with worked examples
- mechanism: partial_observability_experiment_design
  placement: runtime probe surface vs durable journal visible in different fixtures
  why_model_misses_it: models treat probe stream as authoritative after partial recovery
  fairness_guardrail: formal obligation 2 states journal precedence explicitly
- mechanism: deceptive_but_valid_local_evidence
  placement: catalog fast emit vs emit_layer slow witness reducer
  why_model_misses_it: summary looks settled while witness_hex diverges on echo lanes
  fairness_guardrail: formal obligation 3 and cross-lane tests
- mechanism: buried_local_constraints
  placement: fold_key must include prev_family shift, not step_ix alone, for tombstone lineage material
  why_model_misses_it: looks like optional lineage field
  fairness_guardrail: ablation test reverts fold body

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert can satisfy three formal obligations using lane_contract.md and regenerated report within a few hours
- shortcut_audit: static JSON, test deletion, stale-doc-only edits, reward file writes, digest hardcoding
- ablation_plan: revert fold_key only, merge_pack refresh only, mux_combine ordering only — each should drop pass rate on disjoint test subsets
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

Cross-node tombstone resurrection arises when three authorities disagree: runtime-visible revocation probes, durable checkpoint journal bytes, and replay-ordered witness emission. After partial recovery, probes and row-level witness flags can read coherent while echo lanes re-materialize retired principal epochs and a fast catalog regeneration path skips the slow cross-format reducer—producing a green intermediate verifier state that masks corruption until full pipeline replay. Hardness requires reconciling these surfaces under the three formal obligations without the instruction naming which merge rule, which combine ordering, or which emit path is defective.

### Environment shape

Rust Cargo workspace under `/app` forked from the overlay reference mold: driver crate `m2/k81`, pack crates `p7/y4`–`y6`, shared `p7/layer_core`. Data fixtures under `environment/data/`; formal contract in `environment/docs/lane_contract.md`. Output at `/app/output/authority_lane_report.json`. Step 2b may fork `accepted tasks/_ref/overlay-lowerdir-stale-bind/environment/` then reframe docs, instruction field names, and broken semantics; do not shrink below 20 non-Docker environment files.

### Required artifacts

instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh, solution/oracle.patch, and the environment tree listed in Initial Draft Commitments.

### Test plan

- `test_wit_r1_table`: report shape; scenario ids match case_ids.txt
- `test_wit_r2_mirror`: paired echo lanes agree on witness_hex and witness fields when coherent
- `test_wit_r3_closure_flags`: coherent run — lag_code 0 and three row closure fields true on all rows
- `test_wit_r4_consensus`: summary consensus_status settled when matrix coherent
- `test_wit_r5_tier`: tier_span equals max abs lag_code
- `test_wit_r6_digest_rule`: summary digest matches driver header reduction from rows
- `test_wit_r7_digest_anchor`: summary digest matches known-good repaired emission
- `test_wit_r8_hex_format`: witness_hex sixteen lowercase hex chars
- `test_wit_r9_rows_total`: rows_total integer equals len(rows)
- `test_wit_r10_overwrite`: tampered hand-written JSON replaced by pipeline rerun
- `test_wit_r11_idempotent`: consecutive pipeline runs identical
- `test_wit_r12_lowerdir_sensitivity`: mutating lowerdir step table changes witness_hex and bundle_digest
- `test_wit_r13_fold_ablation`: reverting fold_key lineage body breaks tombstone witness coherence
- `test_wit_r14_dual_ablation`: reverting merge refresh and fold together breaks pipeline
- `test_wit_r15_order_ablation`: broken gate wiring + stock stride helper breaks witness closure
- `test_wit_r16_tombstone_trap`: replay lane cannot resurrect tombstoned epoch from seed fixture
- `test_wit_r17_fastpath_trap`: forcing catalog-only emit breaks cross-format witness agreement

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests.

### Drafting guardrails

Instruction is constraint-complete: state the three formal obligations and report contract without naming `fold_key`, `merge_pack`, `mux_combine`, replay phase, canonical recovery order, or fast-path module. Do not copy overlay “Repair sources” wording. Tests derive verdicts from regenerated JSON, tombstone traps, and ablations—not static answer keys.

### Triviality Ledger

- Hand-writing authority_lane_report.json fails `test_wit_r10_overwrite` because verifier reruns cargo + driver.
- Fixing only fold_key without merge_pack refresh fails `test_wit_r14_dual_ablation` and mirror coherence subsets.
- Fixing only mux ordering without stride/gate contract fails `test_wit_r15_order_ablation`.
- Satisfying runtime probes while ignoring journal precedence fails `test_wit_r16_tombstone_trap`.
- Routing regeneration through catalog fast emit fails `test_wit_r17_fastpath_trap` even when row flags look green.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle patch must change semantics in three roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns listed in code_forbidden_tokens must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays constraint-complete about obligations, not cause-revealing (“merge_pack omits storage”).
- RC5/RC6: schemas and bundle_digest home in main.rs header + lane_contract.md; no boolean answer grid in instruction.
- RC7/GX3: oracle.patch coordinated across tie/hold/gate_mux with substantive bodies.
- GX9/GX10: derived bundle_digest and pair equality; no per-scenario expected literals in instruction.
- GX4/GX5: ablation tests patch sources in-container; expectations computed from contract functions in test file.
- Static: run `collapse_check.py --check flipping_point_compliance` and `grep_resistance` after Step 2b.

### Initial Draft Commitments

- tasks/revocation-cache-authority-split-012/task.toml
- tasks/revocation-cache-authority-split-012/instruction.md
- tasks/revocation-cache-authority-split-012/output_contract.toml
- tasks/revocation-cache-authority-split-012/construction_manifest.json
- tasks/revocation-cache-authority-split-012/tests/test.sh
- tasks/revocation-cache-authority-split-012/tests/test_outputs.py
- tasks/revocation-cache-authority-split-012/solution/solve.sh
- tasks/revocation-cache-authority-split-012/solution/oracle.patch
- tasks/revocation-cache-authority-split-012/environment/Dockerfile
- tasks/revocation-cache-authority-split-012/environment/Cargo.toml
- tasks/revocation-cache-authority-split-012/environment/Cargo.lock
- tasks/revocation-cache-authority-split-012/environment/m2/k81/Cargo.toml
- tasks/revocation-cache-authority-split-012/environment/m2/k81/src/main.rs
- tasks/revocation-cache-authority-split-012/environment/m2/k81/src/gate_mux.rs
- tasks/revocation-cache-authority-split-012/environment/m2/k81/src/stack_mix.rs
- tasks/revocation-cache-authority-split-012/environment/m2/k81/src/step_key.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/Cargo.toml
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/lib.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/mesh.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/family.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/row_help.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/emit_layer.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/apply.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/probe.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/kind.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/stack.rs
- tasks/revocation-cache-authority-split-012/environment/p7/layer_core/src/alias_stub.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y4/Cargo.toml
- tasks/revocation-cache-authority-split-012/environment/p7/y4/src/lib.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y4/src/hold.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y4/src/body.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y4/src/shape.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y5/Cargo.toml
- tasks/revocation-cache-authority-split-012/environment/p7/y5/src/lib.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y5/src/tie.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y5/src/body.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y5/src/stamp_help.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y6/Cargo.toml
- tasks/revocation-cache-authority-split-012/environment/p7/y6/src/lib.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y6/src/stride.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y6/src/catalog.rs
- tasks/revocation-cache-authority-split-012/environment/p7/y6/src/body.rs
- tasks/revocation-cache-authority-split-012/environment/data/ladder.toml
- tasks/revocation-cache-authority-split-012/environment/data/channel.toml
- tasks/revocation-cache-authority-split-012/environment/data/seed.json
- tasks/revocation-cache-authority-split-012/environment/data/weights.tsv
- tasks/revocation-cache-authority-split-012/environment/data/notes.md
- tasks/revocation-cache-authority-split-012/environment/docs/case_ids.txt
- tasks/revocation-cache-authority-split-012/environment/docs/lane_contract.md
- tasks/revocation-cache-authority-split-012/environment/docs/build_hints.txt

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p7/y5/src/tie.rs
  symbol: fold_key
  kind: function
  signature: fold_key(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Derives witness_hex material from step and lineage tuple
- path: environment/p7/y4/src/hold.rs
  symbol: merge_pack
  kind: function
  signature: merge_pack(state: &mut PackState, incoming: &PackState, stamp_b: u64)
  purpose: Merges incoming durable pack into active state under journal authority
- path: environment/m2/k81/src/gate_mux.rs
  symbol: mux_combine
  kind: function
  signature: mux_combine<F: FnMut(), G: FnMut()>(side: F, gate: G) -> u32
  purpose: Invokes side and gate callbacks in seeded combine order during replay
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p7/y5/src/tie.rs
    controls_tests: [test_wit_r2_mirror, test_wit_r13_fold_ablation, test_wit_r7_digest_anchor, test_wit_r16_tombstone_trap]
  - id: B
    path: environment/p7/y4/src/hold.rs
    controls_tests: [test_wit_r14_dual_ablation, test_wit_r4_consensus, test_wit_r10_overwrite, test_wit_r16_tombstone_trap]
  - id: C
    path: environment/m2/k81/src/gate_mux.rs
    controls_tests: [test_wit_r15_order_ablation, test_wit_r3_closure_flags, test_wit_r6_digest_rule, test_wit_r17_fastpath_trap]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/p7/y6/src/catalog.rs
  kind: module
  rhymes_with: emit_layer
  non_fix_purpose: Fast catalog emit used in fastpath trap; must not satisfy formal obligation 3 alone
- path: environment/p7/y6/src/stride.rs
  kind: helper
  rhymes_with: mux_combine
  non_fix_purpose: Alternate step_1 ordering helper used in ablation traps, not the fix path
- path: environment/p7/layer_core/src/probe.rs
  kind: helper
  rhymes_with: merge_pack
  non_fix_purpose: Runtime-visible probe stream for diagnostics; not durable journal authority
- path: environment/p7/y5/src/stamp_help.rs
  kind: helper
  rhymes_with: fold_key
  non_fix_purpose: Widening utilities for non-fix stamp experiments
```

#### code_forbidden_tokens

```
revocation, cache, authority, tombstone, resurrection, witness, principal, epoch, node, partition, durable, runtime, verifier, replay, regeneration, cluster, manifest, obligation, consensus, settled, bundle, align, probe, journal, checkpoint, offline, merge, echo, coherent, incoherent, formal
```
