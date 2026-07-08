### Decision

GO — Attempt 1. Validated bank-ready seed as a **reverse_engineering** debugging task on the approved **overlay-lowerdir-stale-bind** Rust/Cargo mold: behavioral-target public revival report contract, three opaque crate roots (driver, pack/emit, catalog/replay), false-green intermediate closure, and cross-format regeneration traps. Profile **build_dependency_toolchain** matches the workspace build graph; tombstone/generation recovery semantics replace overlay layer metaphor without multi-container scope.

### Metadata

- version: 2
- Task name: distributed-tombstone-revival-015
- Title: Tombstone Revival Skew
- Category: debugging
- Task shape: reverse_engineering
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["rust", "cargo-workspace", "generation-skew", "recovery-replay", "json-report", "false-green"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do not leak oracle patch ordering, flipping-point file names in instruction.md, or per-wave answer tables.

### Public contract

After partial store recovery, checkpoint and mount probes can read settled while retired keys reappear under stale generation tags. Echo waves disagree on closure stamps and revival facets even when the aggregate line looks mostly fine.

Make sources under `/app` emit `/app/output/revival_report.json` via `cargo build --release --locked` and `/app/target/release/tv`. Wave ids are listed in `/app/docs/wave_ids.txt`.

The report has `rows` and `summary`. Each row records `wave_id`, `store_rc`, `gen_rc`, `slot_rc` (each 1 when that closure dimension passes, else 0), `skew_code`, and `facet_hex` (exactly 16 lowercase hexadecimal digits). The summary records `rows_total`, `reconcile_status`, `span_band`, and `trace_digest`. Mirror pairs bind `store` with `store_echo`, `shard` with `shard_echo`, and `sweep` with `sweep_echo`. Coherent runs keep `skew_code` at 0 on every row, all three closure counters at 1, matching `facet_hex` on each pair, and `reconcile_status` reading `quiesced`. Incoherent runs break at least one of those conditions (closure counters may read 0 or `reconcile_status` may differ from `quiesced`). The module comment above `/app/m3/k82/src/main.rs` defines `span_band` and `trace_digest` reduction; read that header instead of hand-writing JSON. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_hints.txt` for cargo and pytest argv details.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt (behavioral-target; mirrors Public contract above)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only
- path: tests/test_outputs.py
  role: domain verifier with ablation helpers
- path: solution/solve.sh
  role: oracle applying oracle.patch and rebuild
- path: environment/Dockerfile
  role: build definition; pre-install cargo, pytest, and locked deps
- path: construction_manifest.json
  role: local authoring artifact mirroring Construction manifest below

### task_files

- path: environment/m3/k82/src/main.rs
  role: release driver wiring recovery waves and summary reduction
- path: environment/m3/k82/src/lane_mux.rs
  role: oracle frontier C — combine/invalidate ordering
- path: environment/m3/k82/src/stack_mix.rs
  role: decoy stack helper (non-fix)
- path: environment/m3/k82/src/step_key.rs
  role: decoy key helper (non-fix)
- path: environment/p8/y5/src/seal.rs
  role: oracle frontier A — stamp fold mixing generation lineage
- path: environment/p8/y5/src/body.rs
  role: facet body materialization
- path: environment/p8/y5/src/lib.rs
  role: y5 crate root exports
- path: environment/p8/y5/src/stamp_help.rs
  role: decoy stamp utilities
- path: environment/p8/y4/src/cell.rs
  role: oracle frontier B — pack merge with durable storage refresh
- path: environment/p8/y4/src/body.rs
  role: pack body materialization for y4 crate
- path: environment/p8/y4/src/lib.rs
  role: y4 crate root exports
- path: environment/p8/y4/src/hold.rs
  role: decoy hold buffer (non-fix)
- path: environment/p8/y4/src/contour.rs
  role: decoy contour table
- path: environment/p8/y6/src/pace.rs
  role: oracle frontier C helper — side/gate ordering primitive
- path: environment/p8/y6/src/catalog.rs
  role: durable tombstone index (authority surface)
- path: environment/p8/y6/src/body.rs
  role: pace body materialization for y6 crate
- path: environment/p8/y6/src/lib.rs
  role: y6 crate root exports
- path: environment/p8/y6/src/stride.rs
  role: decoy stride catalog scanner
- path: environment/p8/core/src/emit_layer.rs
  role: oracle frontier D — cross-format emission path
- path: environment/p8/core/src/lib.rs
  role: layer_core crate root exports
- path: environment/p8/core/src/alias_stub.rs
  role: decoy alias table (non-fix)
- path: environment/p8/core/src/kind.rs
  role: row kind tagging helpers
- path: environment/p8/core/src/row_help.rs
  role: decoy row utilities
- path: environment/p8/core/src/stack.rs
  role: decoy stack reducer
- path: environment/p8/core/src/apply.rs
  role: decoy apply shim
- path: environment/p8/core/src/family.rs
  role: generation family tagging
- path: environment/p8/core/src/slot.rs
  role: runtime-visible slot surface (contrasts catalog authority)
- path: environment/p8/core/src/mesh.rs
  role: decoy mesh helper
- path: environment/data/ladder.toml
  role: seeded bind ladder for store wave
- path: environment/data/channel.toml
  role: channel weights for shard wave
- path: environment/data/seed.json
  role: generation seed manifest
- path: environment/data/weights.tsv
  role: sweep weight table
- path: environment/docs/wave_ids.txt
  role: comma-separated wave id table
- path: environment/docs/build_hints.txt
  role: cargo/pytest argv notes
- path: environment/docs/notes.md
  role: row/summary schema and mirror-pair contract visible to the agent
- path: environment/Cargo.toml
  role: workspace root
- path: environment/Cargo.lock
  role: locked dependency graph

### fix_frontier

- count: 4
- distribution: `environment/m3/k82`, `environment/p8/y5`, `environment/p8/y4`, `environment/p8/core` (pace.rs couples to lane_mux but stays thin; catalog.rs is read-only authority witness, not a flip location)
- naming_policy: opaque function and module names on neutral `m3`/`p8` roots; no instruction nouns on fix-path symbols
- forbidden_stems: revival, tombstone, generation, reconciliation, replay, recovery, authority, skew, quiesced, facet, digest, store, shard, sweep, echo, probe, reconcile
- helpers_policy: co-resident crate roots (`lib.rs`), body modules, and rhyming decoys (`hold.rs`, `stride.rs`, `mesh.rs`, `stamp_help.rs`, `alias_stub.rs`, `row_help.rs`, `stack.rs`) perform real non-fix work; no `validate_*`/`repair_*` stems
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: regenerated JSON rows, integer closure counters, derived trace_digest from visible driver contract, paired echo equality, ablation-induced incoherence, pipeline overwrite traps
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction; static golden report files under tests/

### task_shape

- type: reverse_engineering
- instruction_framing: behavioral-target
- hardness_source: semantic inference across conflicting durable vs runtime authorities, replay-ordered closure gates, and cross-format regeneration paths inside a Cargo workspace
- collapse_risk: leaking canonical recovery phase, replay ordering recipe, or reconciliation authority in instruction collapses to a local one-crate patch

### category_profile

- challenge_family: generation_skew_recovery_toolchain
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: build commands, artifact path `/app/output/revival_report.json`, driver binary `tv`, wave id table, row/summary schema, coherent vs incoherent conditions, mirror pairs, trace_digest formula home in main.rs header, offline locked build expectation
- forbidden_instruction_leaks: which crate owns durable tombstone authority, broken replay ordering site, emit path that skips cross-format checks, exact patch functions, per-wave facet answers
- category_specific_hardness_bar: lockfile workspace, generated facets, incremental rebuild graph, and cache-visible runtime probes must coordinate; one dependency bump or one manifest row cannot pass ablation suites
- category_specific_verifier_risks: clean-build-only pass, pin-one-crate fix, static JSON satisfying format without rebuild, false-green closure on partial replay
- coverage_role: Adds build_dependency_toolchain coverage for recovery-era generation skew using the approved overlay Cargo mold with distinct wave/tombstone semantics

### satisfiability_risk

- rc2_planned_name_risk: low — neutral `m3`/`p8` roots and opaque symbols (`mix_key`, `pack_bind`, `lane_mux`, `phase_a`, `emit_rows`)
- gx9_contract_risk: medium — mitigate by deriving expectations from driver header + independent trace_digest recompute, not per-wave answer tables in instruction
- cr1_symbol_frontier_risk: low — explicit four-location flipping contract and decoy manifest
- hidden_contract_risk: low — every tested field and digest rule is visible in instruction or main.rs header comment

### actionability_plan

- verifier_command_visible: instruction cites `cargo build --release --locked`, `/app/target/release/tv`, and `/app/docs/build_hints.txt`
- source_fix_intent_visible: yes — “make sources under `/app` emit …” without naming fix files
- generated_output_rule_visible: revival_report.json path, mirror pairs, coherent predicates, regeneration requirement
- exact_formula_home: module comment above `environment/m3/k82/src/main.rs` for `span_band` and `trace_digest`; tests recompute trace_digest independently
- schema_home: instruction public contract; optional `environment/schemas/revival_report.schema.json` for author lint only

### waiver_plan

- waivers_expected: no
- waiver_rationale: Fairness comes from local deterministic Cargo rebuilds and derived digests; no timing or network dependencies

### reference_pattern

- reference_task_id: async-pipeline-premature-completion

### realism_source

- source_type: real_system
- evidence_basis: Minimized from overlay lowerdir stale-bind recovery incidents (approved zip) and distributed store tombstone revival bugs where runtime probes green-light before durable index replay converges
- upstream_or_synthetic_rationale: Preserves real Cargo incremental rebuild + generation-indexed recovery semantics without shipping proprietary cluster code; Step 2b construction mold follows accepted tasks/overlay-lowerdir-stale-bind.zip (Rust multi-crate workspace, wave JSON sweep, cargo+driver pipeline, ablation pytest)
- minimization_preserves: authority split between catalog index and driver probes, replay-ordered closure gates, cross-format emit bypass, deterministic wave matrix
- synthetic_exception_review: not required

### difficulty_mechanism_plan

- mechanisms: stateful_multi_step_dependencies, false_green_intermediate_states, buried_local_constraints, rollback_recovery_requirements, cross_file_cross_format_invariants
- adversarial_layers_count: 5
- fairness_guardrails: deterministic offline workspace; no latency thresholds; all formulas visible in instruction or main.rs header
- mechanism: stateful_multi_step_dependencies
  placement: cargo rebuild → driver → JSON report; consecutive-run and manual-json overwrite tests
  why_model_misses_it: agents patch sources without rerunning locked build graph
  fairness_guardrail: build_hints document exact commands
- mechanism: false_green_intermediate_states
  placement: lane_mux marks closure true before replay sorts tombstone revival order
  why_model_misses_it: stops when summary line reads quiesced while echo pairs disagree
  fairness_guardrail: tests assert paired echo agreement and closure integers jointly
- mechanism: buried_local_constraints
  placement: mix_key lineage fold in seal.rs vs shipped broken half-payload fold
  why_model_misses_it: facet_hex looks well-formed while skew_code stays zero incorrectly
  fairness_guardrail: ablation test reverts fold and expects incoherence
- mechanism: rollback_recovery_requirements
  placement: pack_bind must refresh durable storage after merge; catalog vs probe authority
  why_model_misses_it: runtime slot_rc reads 1 while gen_rc/store_rc diverge after partial recovery
  fairness_guardrail: dual-crate ablation and store ladder sensitivity tests
- mechanism: cross_file_cross_format_invariants
  placement: emit_layer fast path skips TOML seed cross-check against JSON body
  why_model_misses_it: format-valid JSON passes layout tests without reading data/*.toml
  fairness_guardrail: pipeline tests rebuild from seeds and reject hand-written JSON

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert can derive trace_digest from main.rs header and reconcile echo pairs without tests
- shortcut_audit: static JSON, pytest edits, skipping cargo rebuild, hardcoding trace_digest, reward file writes
- ablation_plan: revert seal fold only; revert cell storage refresh only; revert lane_mux ordering only; revert emit cross-check only — each should drop distinct test subsets
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=frontier agents; post-upload Part E classification on worst-model accuracy
- verifier_offline: pytest and cargo baked in Dockerfile; test.sh performs no apt/pip/curl under allow_internet=false
- post_upload_difficulty: acknowledge platform auto-eval may reclassify if worst-model accuracy exceeds 20%

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when every semantic pytest passes

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step task; cross-test coupling via rebuild pipeline and ablation traps
- local_only_data: true
- sidecar_or_protocol_notes: all fixtures under environment/data; no network services

### Failure topology

Visible recovery checks (probes, aggregate reconcile line) can read healthy while retired keys resurrect under stale generation tags because three mechanisms interact: the durable tombstone catalog remains authoritative for revival ordering but the driver’s runtime probe surface answers first; lane-level closure flags flip true on an intermediate replay pass before tombstone ordering finishes; and a fast emit path materializes JSON facets without reconciling TOML seed ladders against pack-merged storage. Each defect is locally plausible; together they produce generation skew that only appears after rebuild, driver rerun, or echo-pair comparison — matching the bank-ready discovery plan without naming fix coordinates in the prompt.

### Environment shape

Rust Cargo workspace rooted at `/app` with opaque crates under `environment/m3/k82` (driver), `environment/p8/y5` (stamp/seal), `environment/p8/y4` (pack/cell), `environment/p8/y6` (catalog/pace), and `environment/p8/core` (emit/probe/family). Seed data lives in `environment/data/`; operator docs in `environment/docs/`. Single-container only; mirror overlay zip layout density (≥20 non-Docker environment files).

### Required artifacts

Standard TB3 task tree under `tasks/distributed-tombstone-revival-015/`: instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile with locked cargo/pytest, tests/test.sh, tests/test_outputs.py (≥14 tests), solution/solve.sh + oracle.patch, full environment workspace per Initial Draft Commitments.

### Test plan

- `test_q7_matrix_layout`: JSON layout; wave ids match `wave_ids.txt`
- `test_q8_pair_agreement`: mirror pairs agree on facet and closure fields when coherent
- `test_q9_flags_zero`: coherent run — booleans true, skew_code 0
- `test_q10_status_line`: summary reconcile_status reads quiesced when coherent
- `test_q11_band_match`: span_band equals max abs skew_code
- `test_q12_token_contract`: trace_digest matches independent recompute from rows
- `test_q13_token_anchor`: trace_digest matches known-good repaired emission
- `test_q14_token_format`: facet_hex is 16 lowercase hex chars
- `test_q15_total_int`: rows_total matches len(rows)
- `test_q16_overwrite_trap`: stale hand-written JSON replaced after rebuild+tv
- `test_q17_repeat_stable`: back-to-back emissions identical
- `test_q18_bind_mutate`: mutating store ladder in main.rs changes facet and digest
- `test_q19_fold_ablation`: reverting op_a5 fold breaks coherence
- `test_q20_dual_ablation`: reverting seal fold + cell storage refresh breaks pipeline
- `test_q21_order_ablation`: broken lane_mux ordering + shipped pace helper breaks closure

### Drafting guardrails

Keep instruction behavioral-target: complete report schema and coherence rules, but never name catalog vs probe authority, replay phase ordering, or emit bypass. Ban instruction nouns from fix-path symbols and test function names. Do not ship golden revival_report.json in repo. Comments must not use “bug/fix/tombstone/revival” on fix path. Step 2b clones overlay-lowerdir-stale-bind structure then renames metaphors (waves not lanes, tv not mk, revival_report not layer_report).

### Triviality Ledger

- Hand-writing revival_report.json fails `test_pipeline_overwrites_manual_json` and digest anchor tests.
- Pinning one Cargo dependency fails ablation suites that require semantic fixes in seal/cell/lane_mux/emit_layer.
- Fixing only runtime slots in `slot.rs` leaves catalog authority and echo-pair mismatch failures.
- Reordering only data TOML without op_b2 cross-check leaves gen_rc/store_rc divergence on shard/sweep waves.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle.patch must change substantive logic across four roots, not whitespace.
- RC2: instruction nouns must not appear as fix-path symbol/directory substrings.
- RC5/RC6: instruction stays behavioral-target; do not add cause-revealing “the catalog is wrong” sentences.
- RC7: flipping-point spread prevents single-file oracle rewrite.
- GX9: no per-wave expected facet table in instruction; derive from rebuild.
- GX10: coherent/incoherent rules stated once; tests use derived observations.
- Static/collapse: run `collapse_check.py --check flipping_point_compliance` after oracle green.

### Initial Draft Commitments

- tasks/distributed-tombstone-revival-015/task.toml
- tasks/distributed-tombstone-revival-015/instruction.md
- tasks/distributed-tombstone-revival-015/output_contract.toml
- tasks/distributed-tombstone-revival-015/construction_manifest.json
- tasks/distributed-tombstone-revival-015/tests/test.sh
- tasks/distributed-tombstone-revival-015/tests/test_outputs.py
- tasks/distributed-tombstone-revival-015/solution/solve.sh
- tasks/distributed-tombstone-revival-015/solution/oracle.patch
- tasks/distributed-tombstone-revival-015/environment/Dockerfile
- tasks/distributed-tombstone-revival-015/environment/Cargo.toml
- tasks/distributed-tombstone-revival-015/environment/Cargo.lock
- tasks/distributed-tombstone-revival-015/environment/m3/k82/Cargo.toml
- tasks/distributed-tombstone-revival-015/environment/m3/k82/src/main.rs
- tasks/distributed-tombstone-revival-015/environment/m3/k82/src/lane_mux.rs
- tasks/distributed-tombstone-revival-015/environment/m3/k82/src/stack_mix.rs
- tasks/distributed-tombstone-revival-015/environment/m3/k82/src/step_key.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y5/Cargo.toml
- tasks/distributed-tombstone-revival-015/environment/p8/y5/src/seal.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y5/src/body.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y5/src/lib.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y5/src/stamp_help.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y4/Cargo.toml
- tasks/distributed-tombstone-revival-015/environment/p8/y4/src/cell.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y4/src/hold.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y4/src/contour.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y4/src/lib.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y6/Cargo.toml
- tasks/distributed-tombstone-revival-015/environment/p8/y6/src/pace.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y6/src/catalog.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y6/src/stride.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y6/src/body.rs
- tasks/distributed-tombstone-revival-015/environment/p8/y6/src/lib.rs
- tasks/distributed-tombstone-revival-015/environment/p8/core/Cargo.toml
- tasks/distributed-tombstone-revival-015/environment/p8/core/src/emit_layer.rs
- tasks/distributed-tombstone-revival-015/environment/p8/core/src/slot.rs
- tasks/distributed-tombstone-revival-015/environment/p8/core/src/family.rs
- tasks/distributed-tombstone-revival-015/environment/p8/core/src/apply.rs
- tasks/distributed-tombstone-revival-015/environment/p8/core/src/mesh.rs
- tasks/distributed-tombstone-revival-015/environment/p8/core/src/lib.rs
- tasks/distributed-tombstone-revival-015/environment/data/ladder.toml
- tasks/distributed-tombstone-revival-015/environment/data/channel.toml
- tasks/distributed-tombstone-revival-015/environment/data/seed.json
- tasks/distributed-tombstone-revival-015/environment/data/weights.tsv
- tasks/distributed-tombstone-revival-015/environment/docs/wave_ids.txt
- tasks/distributed-tombstone-revival-015/environment/docs/build_hints.txt
- tasks/distributed-tombstone-revival-015/environment/docs/notes.md

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p8/y5/src/seal.rs
  symbol: op_a5
  kind: function
  signature: pub fn op_a5(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Folds step and generation family tags into a 64-bit stamp for facet materialization.

- path: environment/p8/y4/src/cell.rs
  symbol: pack_bind
  kind: function
  signature: pub fn pack_bind(state: &mut PackState, incoming: &PackState, stamp_b: u32) -> u32
  purpose: Merges incoming pack bytes into durable storage during bind steps.

- path: environment/m3/k82/src/lane_mux.rs
  symbol: lane_mux
  kind: function
  signature: pub fn lane_mux(gate_first: bool, side: impl FnMut(), gate: impl FnMut()) -> u32
  purpose: Orders side-effect callbacks during per-wave combine steps.

- path: environment/p8/y6/src/pace.rs
  symbol: phase_a
  kind: function
  signature: pub fn phase_a(gate_first: bool, mut side: impl FnMut(), mut gate: impl FnMut()) -> u32
  purpose: Low-level side/gate ordering primitive invoked from lane_mux.

- path: environment/p8/core/src/emit_layer.rs
  symbol: op_b2
  kind: function
  signature: pub fn op_b2(waves: &[WaveRow], seeds: &SeedBundle) -> Vec<EmittedRow>
  purpose: Materializes report rows from wave state and on-disk seed bundle.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p8/y5/src/seal.rs
    controls_tests: [test_q7_matrix_layout, test_q14_token_format, test_q13_token_anchor, test_q12_token_contract, test_q19_fold_ablation]
  - id: B
    path: environment/p8/y4/src/cell.rs
    controls_tests: [test_q20_dual_ablation, test_q9_flags_zero]
  - id: C
    path: environment/m3/k82/src/lane_mux.rs
    controls_tests: [test_q8_pair_agreement, test_q10_status_line, test_q11_band_match, test_q21_order_ablation]
  - id: D
    path: environment/p8/core/src/emit_layer.rs
    controls_tests: [test_q16_overwrite_trap, test_q17_repeat_stable, test_q18_bind_mutate, test_q15_total_int]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/p8/y4/src/hold.rs
  kind: module
  rhymes_with: pack_bind
  non_fix_purpose: Buffers transient pack slices for diagnostics without touching durable storage.

- path: environment/p8/y6/src/stride.rs
  kind: module
  rhymes_with: phase_a
  non_fix_purpose: Scans catalog windows for offline benchmarks unrelated to driver waves.

- path: environment/p8/core/src/mesh.rs
  kind: module
  rhymes_with: op_b2
  non_fix_purpose: Builds adjacency meshes for notes.md examples without participating in revival_report emission.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [partial, recovery, checkpoint, mount, settled, retired, generation, echo, closure, stamps, facets, aggregate, revival, quiesced, incoherent, static, manual, verifier, rebuild, mirror, pairs, reconcile, locked, sources]
```
