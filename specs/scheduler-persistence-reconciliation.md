### Decision

GO — Attempt 2. Seed `scheduler-persistence-reconciliation-019` validated on the approved `overlay-lowerdir-stale-bind` construction mold: `repair_existing_system` + `symptoms-only` instruction, `debugging` + `state_recovery_crash_consistency` profile with `offline_resolver_artifact_mismatch` challenge family, three-root Rust flipping-point contract, false-green replay traps, and cross-format regeneration invariants without leaking canonical recovery path or replay phase.

### Metadata

- version: 2
- Task name: scheduler-persistence-reconciliation
- Title: Scheduler persistence reconciliation
- Category: debugging
- Task shape: repair_existing_system
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["scheduler", "persistence", "replay", "rust", "offline-resolver", "crash-recovery"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract

After partial cluster recovery, local scheduler status probes and an offline resolver bundle both look healthy. Cold replay still disagrees on closure stamps and digest totals; row-level readiness flags read settled even when echo scenarios diverge. Repair sources under `/app` so a release workspace build and the published driver write `/app/output/reconciliation_report.json`. Scenario ids are in `/app/docs/case_ids.txt`.

The report has `rows` and `summary` with per-scenario closure fields, a lag integer, sixteen-digit hex stamp material, and a summary block carrying row count, status text, tier span, and an eight-digit `run_digest`. Mirror pairs are `lowerdir` with `lowerdir_echo`, `upper` with `upper_echo`, and `worker` with `worker_echo`. Coherent runs keep lag at zero on every row, all three per-row closure fields true, matching stamp material on each pair, and summary status reading `settled`. The module comment above `/app/m2/k81/src/main.rs` defines `tier_span` and `run_digest` reduction; read that header instead of hand-writing JSON. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_hints.txt` for cargo and pytest argv details.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category_profile = "state_recovery_crash_consistency"`
- path: instruction.md
  role: natural public task prompt (symptoms-only repair; must not name patch sites or recovery phase ordering)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl/uv bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation and pipeline traps
- path: solution/solve.sh
  role: oracle applying patch then release build + driver
- path: environment/Dockerfile
  role: build definition; pre-install cargo, pytest, tmux, asciinema, and locked toolchain
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
  role: scenario-matrix driver emitting reconciliation_report.json
- path: environment/m2/k81/src/gate_mux.rs
  role: oracle frontier C — combine ordering for gate vs side callbacks
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
  role: lane line emission
- path: environment/p7/layer_core/src/apply.rs
  role: numeric mix helpers (decoy-adjacent)
- path: environment/p7/layer_core/src/probe.rs
  role: probe utilities
- path: environment/p7/layer_core/src/kind.rs
  role: kind tagging
- path: environment/p7/layer_core/src/stack.rs
  role: frame stack helpers
- path: environment/p7/layer_core/src/alias_stub.rs
  role: linear algebra stub (non-fix)
- path: environment/p7/y4/Cargo.toml
  role: pack merge crate
- path: environment/p7/y4/src/hold.rs
  role: oracle frontier B — durable pack merge refresh
- path: environment/p7/y4/src/lib.rs
  role: y4 exports
- path: environment/p7/y4/src/body.rs
  role: counter helpers
- path: environment/p7/y4/src/shape.rs
  role: dimension checks
- path: environment/p7/y5/Cargo.toml
  role: fold material crate
- path: environment/p7/y5/src/tie.rs
  role: oracle frontier A — lineage fold for row material
- path: environment/p7/y5/src/lib.rs
  role: y5 exports
- path: environment/p7/y5/src/body.rs
  role: bitmask helpers
- path: environment/p7/y5/src/pad_widen.rs
  role: widen helpers
- path: environment/p7/y6/Cargo.toml
  role: stride/catalog crate
- path: environment/p7/y6/src/stride.rs
  role: decoy rhyming with gate ordering (shipped broken ordering helper)
- path: environment/p7/y6/src/catalog.rs
  role: decoy catalog indexing
- path: environment/p7/y6/src/lib.rs
  role: y6 exports
- path: environment/p7/y6/src/body.rs
  role: clip helpers
- path: environment/data/ladder.toml
  role: per-scenario step tables (restart + replay + persistence scenarios)
- path: environment/data/channel.toml
  role: channel weights
- path: environment/data/seed.json
  role: seeded offline resolver inputs
- path: environment/data/weights.tsv
  role: weight table for core mix
- path: environment/data/notes.md
  role: operator notes (no fix recipe)
- path: environment/docs/case_ids.txt
  role: comma-separated scenario ids (mirror triple + base scenarios)
- path: environment/docs/build_hints.txt
  role: cargo/pytest argv and ablation path hints (paths only, not fixes)
- path: solution/oracle.patch
  role: unified diff applied by solve.sh

### fix_frontier

- count: 3
- distribution: `environment/p7/y5/src/tie.rs`, `environment/p7/y4/src/hold.rs`, `environment/m2/k81/src/gate_mux.rs` (distinct crate roots under p7 and m2)
- naming_policy: Keep opaque Rust identifiers on the fix path (`fold_key`, `merge_pack`, `mux_combine`); do not rename to instruction nouns
- forbidden_stems: scheduler, persistence, reconciliation, recovery, replay, resolver, authority, journal, checkpoint, offline, bundle, invariant, settled, digest, align, cluster, probes, readiness, echo, scenarios, closure, stamp, material, tier, span
- helpers_policy: `catalog.rs`, `stride.rs`, `pad_widen.rs`, `alias_stub.rs` are decoys or non-fix helpers declared in decoy_manifest
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: run_digest recomputation, stamp_hex pairs, mirror lane agreement, ablation incoherence, pipeline overwrite trap, consecutive run identity
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction.md; readiness fields named `*_ok` in instruction prose tied 1:1 to test grep of fix symbols

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis across conflicting durable vs runtime evidence, replay ordering, and cross-format regeneration
- collapse_risk: leaking canonical recovery path, replay phase, or fast-path module collapses to localized repair

### category_profile

- challenge_family: offline_resolver_artifact_mismatch
- bug_family: state_recovery_crash_consistency
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: partial recovery/restart workflow, durability guarantee for the report artifact, recovery/rebuild command surface, post-recovery observable state, mirror pairs, digest definition header, scenario ids, false-green symptom description
- forbidden_instruction_leaks: journal/checkpoint internals, broken recovery phase, corrupt record location, replay function names, cleanup path, exact phase ordering, patch functions, fast-path bypass site, canonical recovery sequence
- category_specific_hardness_bar: Partial writes, replay, cleanup, idempotent rerun safety, and restart-after-partial-recovery must all coordinate; durable checkpoint authority must diverge from runtime-visible probe surface until all three fix roots align
- category_specific_verifier_risks: nondeterministic crash timing, hidden snapshot expectations, verifier reading private internals, single stale-file repair shortcut
- coverage_role: Adds state_recovery_crash_consistency depth under debugging with offline resolver artifact mismatch topology distinct from promoted abi-rebuild-mismatch reference

### satisfiability_risk

- rc2_planned_name_risk: medium — instruction uses domain nouns; fix path stays opaque and neutral crate paths (m2/p7)
- gx9_contract_risk: low — run_digest derived from rows; boolean row fields are product-shaped closure flags documented in instruction
- cr1_symbol_frontier_risk: low — three substantive Rust modules plus distributed layer_core support
- hidden_contract_risk: medium — false-green row flags vs summary align_status require ablation messaging in tests only

### actionability_plan

- verifier_command_visible: `cargo build --release --locked` from `/app` and driver at `/app/target/release/mk`; pytest via `/opt/verifier-venv` per build_hints.txt
- source_fix_intent_visible: yes — repair framing requires source changes; instruction must not name which modules
- generated_output_rule_visible: `/app/output/reconciliation_report.json` path and field names
- exact_formula_home: module comment above `environment/m2/k81/src/main.rs`
- schema_home: instruction.md public contract + output_contract.toml paths

### waiver_plan

- waivers_expected: no
- waiver_rationale: Overlay mold demonstrates RC2-safe naming; regeneration and flipping-point tests avoid hidden-instance puzzles

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/overlay-lowerdir-stale-bind.zip` (overlay-lowerdir-stale-bind) for verifier shape, flipping-point ablations, pipeline traps, and three-root Rust workspace layout; reframed to scheduler persistence reconciliation with state_recovery_crash_consistency profile and symptoms-only repair instruction. No promoted entry in docs/reference_tasks/index.json matches this exact profile combo; abi-rebuild-mismatch covers multi-crate regeneration discipline only.

### realism_source

- source_type: synthetic_exception
- evidence_basis: Minimized from production patterns where post-restart scheduler views disagree with offline resolver bundles and replay ordering masks corruption during partial recovery
- upstream_or_synthetic_rationale: Controlled offline resolver artifact mismatch with deterministic replay/restart — avoids hidden-instance “which file is corrupt” puzzles
- minimization_preserves: Multi-surface evidence conflict, false-green intermediate states, cross-format regeneration bypass, partial-recovery authority split
- synthetic_exception_review: Difficulty from coupled recovery/replay/authority semantics, not obscure facts; decoys perform real non-fix work

### Failure topology

Partial cluster recovery leaves two plausible authorities: the runtime-visible scheduler probe surface and the durable checkpoint journal that offline resolver tooling replays. Local checks can agree while replay reordering reintroduces retired wave states into echo lanes; a regeneration fast path can emit JSON that satisfies superficial row flags yet violates cross-format stamp rules used by the slow validator. Hardness requires reconciling these surfaces under deterministic replay and restart without the instruction naming which queue ordering, which journal merge, or which emitter path is wrong.

### Environment shape

Rust Cargo workspace under `/app` with driver crate `m2/k81`, pack crates `p7/y4`–`y6`, and shared `p7/layer_core`. Data fixtures under `environment/data/`; operator docs under `environment/docs/`. Output lands in `/app/output/`. Step 2b forks the overlay reference tree then reframes docs/instruction field names and scenario tables for persistence/restart semantics; do not shrink below 20 non-Docker environment files.

### Required artifacts

instruction.md, task.toml (`allow_internet = false`, `category = "debugging"`, `category_profile = "state_recovery_crash_consistency"`), output_contract.toml, construction_manifest.json, Dockerfile (tmux + asciinema pinned), tests/test.sh, tests/test_outputs.py, solution/solve.sh, solution/oracle.patch, and the environment tree listed in Initial Draft Commitments.

### Test plan

- `test_aux_r1_table`: report shape; scenario ids match case_ids.txt
- `test_aux_r2_mirror`: paired echo lanes agree on stamp and closure fields when coherent
- `test_aux_r3_closure`: coherent run — lag_code 0 and three booleans true on all rows
- `test_aux_r4_align`: summary align_status settled when matrix coherent
- `test_aux_r5_tier`: tier_span equals max abs lag_code
- `test_aux_r6_digest_contract`: run_digest matches driver header reduction from rows
- `test_aux_r7_digest_anchor`: run_digest matches known-good repaired emission
- `test_aux_r8_hex_format`: stamp_hex sixteen lowercase hex chars
- `test_aux_r9_rows_total`: rows_total integer equals len(rows)
- `test_aux_r10_overwrite`: tampered hand-written JSON replaced by pipeline rerun
- `test_aux_r11_idempotent`: consecutive pipeline runs identical
- `test_aux_r12_lowerdir_sensitivity`: mutating lowerdir step table changes stamp and digest
- `test_aux_r13_fold_ablation`: reverting fold_key lineage body breaks coherence
- `test_aux_r14_dual_ablation`: reverting merge refresh and fold together breaks pipeline
- `test_aux_r15_order_ablation`: broken gate wiring + stock stride helper breaks closure

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests (5/15 each).

### Drafting guardrails

Instruction is symptoms-only repair: describe conflicting evidence after partial recovery and the report contract without naming `fold_key`, `merge_pack`, `mux_combine`, replay phase, journal merge site, or canonical recovery order. Do not copy overlay “lowerdir replay” wording verbatim — reframe to scheduler/persistence symptoms. Keep module comments free of GX1 correctional vocabulary. Tests derive verdicts from regenerated JSON and ablations, not static answer keys.

### Triviality Ledger

- Hand-writing reconciliation_report.json fails `test_aux_r10_overwrite` because verifier reruns cargo + driver.
- Fixing only fold_key without merge_pack refresh fails `test_aux_r14_dual_ablation` and mirror coherence subsets.
- Fixing only mux ordering without stride/gate contract fails `test_aux_r15_order_ablation`.
- Copying one row from a golden fixture fails digest anchor and ladder sensitivity tests.
- Deleting one stale checkpoint file without coordinating merge ordering passes local probe checks but fails echo mirror and digest contract tests.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle patch must change semantics in three roots; forbid single-file wholesale replace of entire workspace.
- RC2: instruction nouns (scheduler, persistence, reconciliation, etc.) must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays symptoms-only; no cause-revealing “the journal merge omits storage” sentences.
- RC5/RC6: schemas and digest home documented in main.rs header; no boolean answer grid in instruction.
- RC7/GX3: oracle.patch coordinated across tie/hold/gate_mux with substantive bodies, not comment-only drift.
- GX9/GX10: prefer derived digests and pair equality over scenario boolean tables; avoid contradictory polarity per scenario in instruction.
- GX4/GX5: ablation tests patch sources in-container; expectations computed from contract functions in test file.
- Static: run `collapse_check.py --check flipping_point_compliance` and `grep_resistance` after Step 2b; refresh `.step2b-checksum` only after gates.

### Initial Draft Commitments

- tasks/scheduler-persistence-reconciliation/task.toml
- tasks/scheduler-persistence-reconciliation/instruction.md
- tasks/scheduler-persistence-reconciliation/output_contract.toml
- tasks/scheduler-persistence-reconciliation/construction_manifest.json
- tasks/scheduler-persistence-reconciliation/tests/test.sh
- tasks/scheduler-persistence-reconciliation/tests/test_outputs.py
- tasks/scheduler-persistence-reconciliation/solution/solve.sh
- tasks/scheduler-persistence-reconciliation/solution/oracle.patch
- tasks/scheduler-persistence-reconciliation/environment/Dockerfile
- tasks/scheduler-persistence-reconciliation/environment/Cargo.toml
- tasks/scheduler-persistence-reconciliation/environment/Cargo.lock
- tasks/scheduler-persistence-reconciliation/environment/m2/k81/Cargo.toml
- tasks/scheduler-persistence-reconciliation/environment/m2/k81/src/main.rs
- tasks/scheduler-persistence-reconciliation/environment/m2/k81/src/gate_mux.rs
- tasks/scheduler-persistence-reconciliation/environment/m2/k81/src/stack_mix.rs
- tasks/scheduler-persistence-reconciliation/environment/m2/k81/src/step_key.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/Cargo.toml
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/lib.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/mesh.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/family.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/row_help.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/emit_layer.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/apply.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/probe.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/kind.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/stack.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/layer_core/src/alias_stub.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y4/Cargo.toml
- tasks/scheduler-persistence-reconciliation/environment/p7/y4/src/lib.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y4/src/hold.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y4/src/body.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y4/src/shape.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y5/Cargo.toml
- tasks/scheduler-persistence-reconciliation/environment/p7/y5/src/lib.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y5/src/tie.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y5/src/body.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y5/src/pad_widen.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y6/Cargo.toml
- tasks/scheduler-persistence-reconciliation/environment/p7/y6/src/lib.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y6/src/stride.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y6/src/catalog.rs
- tasks/scheduler-persistence-reconciliation/environment/p7/y6/src/body.rs
- tasks/scheduler-persistence-reconciliation/environment/data/ladder.toml
- tasks/scheduler-persistence-reconciliation/environment/data/channel.toml
- tasks/scheduler-persistence-reconciliation/environment/data/seed.json
- tasks/scheduler-persistence-reconciliation/environment/data/weights.tsv
- tasks/scheduler-persistence-reconciliation/environment/data/notes.md
- tasks/scheduler-persistence-reconciliation/environment/docs/case_ids.txt
- tasks/scheduler-persistence-reconciliation/environment/docs/build_hints.txt

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p7/y5/src/tie.rs
  symbol: fold_key
  kind: function
  signature: fold_key(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Derives stamp material from step and lineage tuple
- path: environment/p7/y4/src/hold.rs
  symbol: merge_pack
  kind: function
  signature: merge_pack(state: &mut PackState, incoming: &PackState, stamp_b: u64)
  purpose: Merges incoming durable pack into active state
- path: environment/m2/k81/src/gate_mux.rs
  symbol: mux_combine
  kind: function
  signature: mux_combine<F: FnMut(), G: FnMut()>(side: F, gate: G) -> u32
  purpose: Invokes side and gate callbacks in seeded combine order
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p7/y5/src/tie.rs
    controls_tests: [test_aux_r2_mirror, test_aux_r7_digest_anchor, test_aux_r8_hex_format, test_aux_r12_lowerdir_sensitivity, test_aux_r13_fold_ablation]
  - id: B
    path: environment/p7/y4/src/hold.rs
    controls_tests: [test_aux_r4_align, test_aux_r9_rows_total, test_aux_r10_overwrite, test_aux_r11_idempotent, test_aux_r14_dual_ablation]
  - id: C
    path: environment/m2/k81/src/gate_mux.rs
    controls_tests: [test_aux_r1_table, test_aux_r3_closure, test_aux_r5_tier, test_aux_r6_digest_contract, test_aux_r15_order_ablation]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/p7/y6/src/catalog.rs
  kind: module
  rhymes_with: fold_key
  non_fix_purpose: Indexes lane metadata for diagnostics exports
- path: environment/p7/y6/src/stride.rs
  kind: helper
  rhymes_with: mux_combine
  non_fix_purpose: Alternate step_1 ordering helper used in ablation traps, not the fix path
- path: environment/p7/y5/src/pad_widen.rs
  kind: helper
  rhymes_with: fold_key
  non_fix_purpose: Widening utilities for non-fix stamp experiments
```

#### code_forbidden_tokens

```
scheduler, persistence, reconciliation, recovery, replay, resolver, authority, journal, checkpoint, offline, bundle, invariant, settled, digest, align, cluster, probes, readiness, echo, scenarios, closure, stamp, material, tier, span
```

### difficulty_mechanism_plan

- mechanisms: environment_specific_cli_semantics, buried_local_constraints, rollback_recovery_requirements, false_green_intermediate_states, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants
- adversarial_layers_count: 6
- fairness_guardrails: All tested formulas and scenario ids are public; deterministic rebuild; no timing/latency thresholds
- mechanism: environment_specific_cli_semantics
  placement: build_hints.txt cargo argv and `/bin/true /app/environment/p7` prefix
  why_model_misses_it: hand-written JSON survives until full pipeline rerun
  fairness_guardrail: documented in build_hints
- mechanism: buried_local_constraints
  placement: fold_key must include prev_family shift, not step_ix alone
  why_model_misses_it: looks like optional lineage field
  fairness_guardrail: ablation test reverts fold body
- mechanism: rollback_recovery_requirements
  placement: ladder.toml scenarios spanning restart then replay lanes
  why_model_misses_it: fixing one lane table row without merge ordering leaves echo incoherence after partial recovery
  fairness_guardrail: deterministic case_ids.txt
- mechanism: false_green_intermediate_states
  placement: mux_combine gate-first wiring during combine; row closure fields vs summary status line
  why_model_misses_it: intermediate pass reports settled align_status while echo lanes diverge
  fairness_guardrail: mirror pairs and run_digest contract are in instruction
- mechanism: deceptive_but_valid_local_evidence
  placement: runtime probe surface vs durable pack authority in hold/tie
  why_model_misses_it: agents trust local greens without cross-authority reconciliation
  fairness_guardrail: ablation and mirror tests
- mechanism: cross_file_cross_format_invariants
  placement: fast regeneration path vs slow validator in hold/tie vs catalog stride
  why_model_misses_it: summary looks fine while stamp_hex diverges on echo lanes
  fairness_guardrail: cross-lane tests and dual-crate ablation

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: author runs `harbor_gate.py --oracle` and `--nop` after Step 2b
- shortcut_audit: static JSON, test deletion, stale-doc-only edits, reward file writes, single stale-file deletion
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
