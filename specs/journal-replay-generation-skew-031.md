### Decision

GO — Attempt 1. Bank-ready seed `journal-replay-generation-skew-031` passes idea validation on the approved **overlay-lowerdir-stale-bind** Rust/Cargo construction mold (`accepted tasks/_ref/overlay-lowerdir-stale-bind/` / `overlay-lowerdir-stale-bind.zip`), reframed to **debugging** + **repair_existing_system** + **build_dependency_toolchain** with **stale checkpoint replay after partial rollback** topology. Three mandated discoveries, four-location flipping-point contract, symptoms-only public contract without leaking canonical recovery path, replay phase ordering, or durable-index vs runtime-probe authority.

### Metadata

- version: 2
- Task name: journal-replay-generation-skew-031
- Title: Journal replay generation skew
- Category: debugging
- Task shape: repair_existing_system
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["rust", "cargo-workspace", "journal-replay", "checkpoint-rollback", "generation-skew", "false-green", "offline-build"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, per-lane facet answer tables, or narrative causal chains that name fix coordinates.

### Public contract

After partial rollback, locked workspace checks can read settled while journal replay still revives retired generation identities from stale checkpoint ancestry. Echo lanes disagree on closure counters and facet material even when the aggregate summary line looks mostly fine.

Repair sources under `/app` so the workspace release build and `/app/target/release/jr` write `/app/output/replay_report.json`. Lane ids are in `/app/docs/lane_ids.txt`.

The report has `rows` and `summary`. Each row records `lane_id`, `chk_rc`, `seg_rc`, `roll_rc` (each `1` when that closure dimension passes, else `0`), `skew_code`, and `facet_hex` (exactly 16 lowercase hexadecimal digits). The summary records `rows_total`, `sync_label`, `gen_span`, and `trace_digest`. Mirror pairs are `alpha` with `alpha_echo`, `beta` with `beta_echo`, and `gamma` with `gamma_echo`. Coherent runs keep `skew_code` at `0` on every row, all three closure counters at `1`, matching `facet_hex` on each pair, and `sync_label` reading `settled`. Incoherent runs break at least one of those conditions (closure counters may read `0` or `sync_label` may differ from `settled`). The module comment above `/app/m3/k82/src/main.rs` defines `gen_span` and `trace_digest` reduction; read that header instead of hand-writing JSON. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_cmds.txt` for cargo and pytest argv details including rollback replay hook sequence.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "debugging"`
- path: instruction.md
  role: natural public task prompt (symptoms-only repair; mirrors Public contract above)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation, authority-split, and pipeline traps
- path: solution/solve.sh
  role: oracle applying oracle.patch and locked rebuild
- path: environment/Dockerfile
  role: build definition; pre-install rustc workspace tooling, pytest, tmux, asciinema, and locked deps
- path: construction_manifest.json
  role: local authoring artifact mirroring Construction manifest below

### task_files

- path: environment/m3/k82/src/main.rs
  role: release driver wiring lane matrix and summary reduction header
- path: environment/m3/k82/src/seq_n4.rs
  role: oracle frontier C — combine/invalidate ordering under journal replay after rollback
- path: environment/m3/k82/src/stack_mix.rs
  role: ladder application glue coupling checkpoint packs to lane material
- path: environment/m3/k82/src/step_key.rs
  role: decoy per-step key helper co-resident with driver crate (non-fix)
- path: environment/p8/y5/src/fold_k3.rs
  role: oracle frontier A — generation fold for facet_hex material across checkpoint lineage
- path: environment/p8/y5/src/body.rs
  role: facet body materialization for y5 crate
- path: environment/p8/y5/src/lib.rs
  role: y5 crate root exports
- path: environment/p8/y5/src/sp_help.rs
  role: decoy stamp utilities (non-fix)
- path: environment/p8/y4/src/pack_w2.rs
  role: oracle frontier B — pack merge with durable checkpoint refresh after partial rollback
- path: environment/p8/y4/src/body.rs
  role: pack body materialization for y4 crate
- path: environment/p8/y4/src/lib.rs
  role: y4 crate root exports
- path: environment/p8/y4/src/hold_buf.rs
  role: decoy hold buffer (non-fix)
- path: environment/p8/y4/src/contour.rs
  role: decoy contour table (non-fix)
- path: environment/p8/y6/src/twist_p8.rs
  role: low-level side/gate ordering primitive used by seq_n4 (decoy rhymes with seq_n4)
- path: environment/p8/y6/src/index_h.rs
  role: durable checkpoint index authority (witness surface; not a flip location)
- path: environment/p8/y6/src/body.rs
  role: pace body materialization for y6 crate
- path: environment/p8/y6/src/lib.rs
  role: y6 crate root exports
- path: environment/p8/y6/src/stride_scan.rs
  role: decoy stride catalog scanner (non-fix)
- path: environment/p8/core/src/emit_q1.rs
  role: oracle frontier D — cross-format row materialization path with checkpoint witness cross-check
- path: environment/p8/core/src/blob_chk.rs
  role: checkpoint blob witness parsing module co-resident with emit_q1 slow path
- path: environment/p8/core/src/gauge_m.rs
  role: false-green intermediate closure counters before replay completes
- path: environment/p8/core/src/fprint.rs
  role: runtime-visible generation probe surface (contrasts index_h authority)
- path: environment/p8/core/src/lib.rs
  role: core crate root exports
- path: environment/p8/core/src/alias_stub.rs
  role: decoy alias table (non-fix)
- path: environment/p8/core/src/kind.rs
  role: row kind tagging helpers
- path: environment/p8/core/src/row_help.rs
  role: decoy row utilities (non-fix)
- path: environment/p8/core/src/stack.rs
  role: decoy stack reducer (non-fix)
- path: environment/p8/core/src/apply.rs
  role: decoy apply shim (non-fix)
- path: environment/p8/core/src/family.rs
  role: generation family tagging
- path: environment/p8/core/src/mesh.rs
  role: decoy mesh helper (non-fix)
- path: environment/data/seg_tbl.toml
  role: seeded bind ladder for alpha lane
- path: environment/data/channel.toml
  role: channel weights for beta lane
- path: environment/data/seed.json
  role: generation seed manifest
- path: environment/data/weights.tsv
  role: gamma lane weight table
- path: environment/data/chk_blob.json
  role: durable checkpoint witness bytes cross-checked by slow path
- path: environment/data/rollback_ladder.toml
  role: partial rollback scenario ladder consumed by driver
- path: environment/docs/lane_ids.txt
  role: comma-separated primary lane id table
- path: environment/docs/build_cmds.txt
  role: cargo/pytest argv and rollback replay hook notes
- path: environment/docs/notes.md
  role: row/summary schema and mirror-pair contract visible to the agent
- path: environment/Cargo.toml
  role: workspace root
- path: environment/Cargo.lock
  role: locked dependency graph

### fix_frontier

- count: 4
- distribution: `environment/p8/y5/src/fold_k3.rs`, `environment/p8/y4/src/pack_w2.rs`, `environment/m3/k82/src/seq_n4.rs`, `environment/p8/core/src/emit_q1.rs` (distinct roots m3, p8/y5, p8/y4, p8/core)
- naming_policy: Opaque identifiers (`fold_k3`, `pack_w2`, `seq_n4`, `emit_q1`) on neutral parameter names; no instruction nouns on fix path
- forbidden_stems: journal, replay, generation, skew, rollback, partial, settled, checkpoint, echo, disagree, closure, facet, aggregate, summary, repair, release, replay_report, lane_ids, chk_rc, seg_rc, roll_rc, skew_code, facet_hex, sync_label, gen_span, trace_digest, mirror, alpha, beta, gamma, coherent, incoherent, static, manual, verifier, recovery, durable, runtime, corruption, regeneration, drift, provenance, shadow, incremental, stale_bind, mix_r7, merge_u3, ord_g2, rk1_snap, mk, k81, m2, m4, p7, p9
- helpers_policy: Co-resident crate roots and rhyming decoys perform credible adjacent work; frontier stays thin at four fix symbols with blob_chk parsing helpers declared in decoy_manifest and driver/index orchestration separate
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: regenerated JSON rows, integer closure counters, derived trace_digest, echo pair equality, checkpoint authority traps, ablation incoherence, pipeline overwrite, checkpoint witness cross-check, rollback replay hook sequence
- forbidden_assertion_styles: scenario-key expected tables in instruction.md; static golden report under tests/; readiness fields named `*_ok` in instruction prose tied 1:1 to fix-path grep

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis across conflicting journal-replay evidence surfaces under destructive rollback recovery without cause-revealing hints
- collapse_risk: Leaking canonical recovery path, replay phase ordering, or durable-index vs runtime-probe authority collapses to a local one-crate patch

### category_profile

- challenge_family: stale_checkpoint_replay_after_partial_rollback
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: locked Cargo build commands, artifact path `/app/output/replay_report.json`, driver binary `jr`, lane_ids.txt, row/summary schema, coherent vs incoherent conditions, mirror pairs, trace_digest formula home in main.rs header, build_cmds rollback replay argv
- forbidden_instruction_leaks: Durable-index vs runtime-probe authority split, broken replay ordering site, emit_q1 bypass site, canonical recovery sequence, replay phase that masks corruption, which module is authoritative by default
- category_specific_hardness_bar: Lockfile workspace, generated facets, build graph, cache-visible runtime probes, checkpoint witness bytes, and cross-format emit path must coordinate; one dependency bump or one manifest row cannot pass ablation and authority-split suites
- category_specific_verifier_risks: clean-build-only pass, pin-one-crate fix, static JSON satisfying format without rebuild, false-green closure on partial journal replay after rollback
- coverage_role: Adds build_dependency_toolchain repair coverage for journal replay generation skew using the approved overlay Cargo mold with distinct checkpoint/rollback semantics and symptoms-only framing distinct from incremental-build-shadow-artifacts-023 adversarial_generalization variant

### satisfiability_risk

- rc2_planned_name_risk: low — neutral `m3`/`p8` roots and opaque symbols (`fold_k3`, `pack_w2`, `seq_n4`, `emit_q1`)
- gx9_contract_risk: low — tests derive verdicts from trace_digest recompute and pair equality, not per-lane answer tables in instruction
- cr1_symbol_frontier_risk: low — four substantive Rust modules plus explicit flipping-point contract
- hidden_contract_risk: medium — rollback replay hook argv and checkpoint precedence traps; instruction states hook existence in build_cmds.txt without naming internal wiring

### actionability_plan

- verifier_command_visible: `cargo build --release --locked` from `/app`, `/app/target/release/jr`, `/app/docs/build_cmds.txt` rollback replay argv
- source_fix_intent_visible: yes — repair under `/app` without naming modules
- generated_output_rule_visible: replay_report.json path, mirror pairs, coherent predicates, regeneration requirement
- exact_formula_home: module comment above `environment/m3/k82/src/main.rs`
- schema_home: instruction public contract; optional `environment/schemas/replay_row.schema.json` for author lint only

### waiver_plan

- waivers_expected: false
- waiver_rationale: Overlay mold keeps contracts observation-shaped with solver-visible formula homes; deterministic offline Cargo rebuilds

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/_ref/overlay-lowerdir-stale-bind/` (`overlay-lowerdir-stale-bind.zip`) for verifier shape, flipping-point ablations, workspace+driver pipeline traps, and three-plus crate flipping-point discipline; reframed from overlay lowerdir repair to journal replay generation skew + build_dependency_toolchain with checkpoint rollback vocabulary and symptoms-only repair framing. No promoted entry in `docs/reference_tasks/index.json` matches this exact profile combo; incremental-build-shadow-artifacts-023 shares the mold but uses adversarial_generalization + held-out permutations.

### realism_source

- source_type: real_system
- evidence_basis: Minimized from build-farm journal/checkpoint replay postmortems where partial rollback leaves durable checkpoint bytes authoritative while runtime generation probes answer first, plus overlay lowerdir stale-bind recovery incidents (approved zip)
- upstream_or_synthetic_rationale: Preserves authority split, false-green intermediate closure, cross-format emit bypass, and rollback replay ordering without proprietary build farm code
- minimization_preserves: Durable checkpoint index vs runtime fprint divergence, intermediate gauge_m closure before replay completes, JSON fast path without chk_blob cross-check, rollback ladder scenarios in rollback_ladder.toml
- synthetic_exception_review: not required

### Failure topology

Visible rollback checks (locked workspace check surfaces, aggregate sync_label) can read settled while journal replay revives stale generation identities because three mechanisms interact: the durable checkpoint index (`index_h`) remains authoritative for replay ordering but the driver’s runtime generation probe (`fprint`) answers first after partial recovery; `seq_n4` marks `chk_rc`/`seg_rc` true on an intermediate replay pass before `twist_p8`/phase ordering finishes, producing false-green closure while echo pairs disagree; and `emit_q1` fast path materializes JSON facets without reconciling `chk_blob.json` against bundled TOML/TSV seeds. Each defect is locally plausible; together they produce generation skew that only appears after locked rebuild, driver rerun, echo-pair comparison, rollback replay hook sequence, or checkpoint authority drills—matching the bank-ready discovery plan without naming fix coordinates in the prompt.

### Environment shape

Rust Cargo workspace rooted at `/app` with opaque crates under `environment/m3/k82` (driver), `environment/p8/y5` (generation fold), `environment/p8/y4` (pack merge), `environment/p8/y6` (index/twist), and `environment/p8/core` (emit/gauge/fprint). Seed data lives in `environment/data/`; operator docs in `environment/docs/`. Single-container only; fork overlay reference layout density (≥20 non-Docker environment files). Step 2b may fork `accepted tasks/_ref/overlay-lowerdir-stale-bind/environment/` then reframe docs, field names, and broken semantics; do not shrink below 20 non-Docker environment files.

### Required artifacts

Standard TB3 task tree under `tasks/journal-replay-generation-skew-031/`: instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile with locked cargo/pytest/tmux/asciinema, tests/test.sh, tests/test_outputs.py (≥18 tests), solution/solve.sh + oracle.patch, full environment workspace per Initial Draft Commitments.

### Test plan

- test_jr_r1_matrix_layout: JSON layout; primary lane ids match lane_ids.txt
- test_jr_r2_pair_hex: mirror pairs agree on facet material and rc fields when coherent
- test_jr_r3_rc_fields: coherent run — skew_code 0 and three rc fields 1 on all rows
- test_jr_r4_label_text: summary sync_label reads settled when matrix coherent
- test_jr_r5_width_max: gen_span equals max abs skew_code
- test_jr_r6_reduce_hex: summary trace_digest matches main.rs header reduction from rows
- test_jr_r7_known_good: trace_digest matches known-good repaired emission
- test_jr_r8_hex_lower: facet_hex sixteen lowercase hex chars
- test_jr_r9_total_count: rows_total integer equals row vector length
- test_jr_r10_fresh_pipeline: tampered hand-written JSON replaced by pipeline rebuild
- test_jr_r11_twice_same: consecutive pipeline runs identical
- test_jr_r12_sens_steps: mutating alpha ladder data changes facet material and digest
- test_jr_r13_ablate_k3: reverting fold_k3 fold breaks coherence
- test_jr_r14_flip_both: reverting pack_w2 and fold_k3 together breaks pipeline
- test_jr_r15_ablate_order: broken seq_n4 combine wiring + stock twist_p8 helper breaks closure
- test_jr_r16_k7_trap: echo lane cannot keep stale generation after durable-bytes replay fixture
- test_jr_r17_ablate_wit: reverting emit_q1 checkpoint witness cross-check breaks seg_rc vs blob bytes
- test_jr_r18_durable_first: durable index_h precedes runtime fprint reads after alpha drill
- test_jr_r19_premature: gauge_m settled label with disagreeing mirror pairs fails until replay completes
- test_jr_r20_replay_hook: build_cmds command sequence required for jr rollback replay success

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests (cap 0.5).

### Drafting guardrails

Instruction is symptoms-only about disagreeing echo lanes and stale generation revival after partial rollback—without naming `fold_k3`, `pack_w2`, `seq_n4`, `emit_q1`, replay phase ordering, index_h vs fprint wiring, or emit bypass. Do not copy overlay “lowerdir/mount” wording verbatim. Ban instruction nouns from fix-path code symbols and test identifiers. No boolean readiness verdict fields in planned outputs. Do not ship golden replay_report.json in repo.

### Triviality Ledger

- Hand-writing replay_report.json fails test_jr_r10_fresh_pipeline because verifier reruns cargo + jr.
- Fixing only fold_k3 without pack_w2 durable refresh fails test_jr_r14_flip_both and pair coherence subsets.
- Fixing only seq_n4 without twist_p8 primitive contract fails test_jr_r15_ablate_order and test_jr_r16_k7_trap.
- Copying one row from a golden fixture fails test_jr_r7_known_good and test_jr_r12_sens_steps.
- Trusting gauge_m settled label while mirror pairs disagree fails test_jr_r19_premature until seq_n4 ordering and checkpoint authority align.
- Bumping one Cargo.toml dependency version fails ablation suites requiring semantic fixes across four roots.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle must change semantics in four roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays symptoms-only without cause-revealing “emit_q1 skips checkpoint witness” sentences.
- RC5/RC6: schemas and digest home in main.rs header; no boolean answer grid in instruction.
- RC7/GX3: solve.sh coordinated across four modules with substantive bodies.
- GX9/GX10: derived digests and pair equality over scenario boolean tables.
- GX4/GX5: ablation tests patch sources in-container; expectations computed in test file.
- CR1/CR2: honor symbol table and flipping-point concentration cap 0.5.

### Initial Draft Commitments

- tasks/journal-replay-generation-skew-031/task.toml
- tasks/journal-replay-generation-skew-031/instruction.md
- tasks/journal-replay-generation-skew-031/output_contract.toml
- tasks/journal-replay-generation-skew-031/construction_manifest.json
- tasks/journal-replay-generation-skew-031/tests/test.sh
- tasks/journal-replay-generation-skew-031/tests/test_outputs.py
- tasks/journal-replay-generation-skew-031/solution/solve.sh
- tasks/journal-replay-generation-skew-031/solution/oracle.patch
- tasks/journal-replay-generation-skew-031/environment/Dockerfile
- tasks/journal-replay-generation-skew-031/environment/Cargo.toml
- tasks/journal-replay-generation-skew-031/environment/Cargo.lock
- tasks/journal-replay-generation-skew-031/environment/m3/k82/Cargo.toml
- tasks/journal-replay-generation-skew-031/environment/m3/k82/src/main.rs
- tasks/journal-replay-generation-skew-031/environment/m3/k82/src/seq_n4.rs
- tasks/journal-replay-generation-skew-031/environment/m3/k82/src/stack_mix.rs
- tasks/journal-replay-generation-skew-031/environment/m3/k82/src/step_key.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y5/Cargo.toml
- tasks/journal-replay-generation-skew-031/environment/p8/y5/src/fold_k3.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y5/src/body.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y5/src/lib.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y5/src/sp_help.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y4/Cargo.toml
- tasks/journal-replay-generation-skew-031/environment/p8/y4/src/pack_w2.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y4/src/body.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y4/src/hold_buf.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y4/src/contour.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y4/src/lib.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y6/Cargo.toml
- tasks/journal-replay-generation-skew-031/environment/p8/y6/src/twist_p8.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y6/src/index_h.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y6/src/body.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y6/src/stride_scan.rs
- tasks/journal-replay-generation-skew-031/environment/p8/y6/src/lib.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/Cargo.toml
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/emit_q1.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/blob_chk.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/gauge_m.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/fprint.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/kind.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/family.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/alias_stub.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/row_help.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/stack.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/apply.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/mesh.rs
- tasks/journal-replay-generation-skew-031/environment/p8/core/src/lib.rs
- tasks/journal-replay-generation-skew-031/environment/data/seg_tbl.toml
- tasks/journal-replay-generation-skew-031/environment/data/channel.toml
- tasks/journal-replay-generation-skew-031/environment/data/seed.json
- tasks/journal-replay-generation-skew-031/environment/data/weights.tsv
- tasks/journal-replay-generation-skew-031/environment/data/chk_blob.json
- tasks/journal-replay-generation-skew-031/environment/data/rollback_ladder.toml
- tasks/journal-replay-generation-skew-031/environment/docs/lane_ids.txt
- tasks/journal-replay-generation-skew-031/environment/docs/build_cmds.txt
- tasks/journal-replay-generation-skew-031/environment/docs/notes.md

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p8/y5/src/fold_k3.rs
  symbol: fold_k3
  kind: function
  signature: pub fn fold_k3(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Folds step and family tags into generation bits for report facets.
- path: environment/p8/y4/src/pack_w2.rs
  symbol: pack_w2
  kind: function
  signature: pub fn pack_w2(state: &mut PackState, incoming: &PackState, stamp_b: u32) -> u32
  purpose: Merges incoming pack bytes into durable storage during bind steps.
- path: environment/m3/k82/src/seq_n4.rs
  symbol: seq_n4
  kind: function
  signature: pub fn seq_n4(gate_first: bool, side: impl FnMut(), gate: impl FnMut()) -> u32
  purpose: Orders side-effect callbacks during per-lane combine steps under replay.
- path: environment/p8/y6/src/twist_p8.rs
  symbol: twist_p8
  kind: function
  signature: pub fn twist_p8(gate_first: bool, mut side: impl FnMut(), mut gate: impl FnMut()) -> u32
  purpose: Low-level side/gate ordering primitive used by seq_n4.
- path: environment/p8/core/src/emit_q1.rs
  symbol: emit_q1
  kind: function
  signature: pub fn emit_q1(facet_hex: &str, witness_path: &Path) -> bool
  purpose: Cross-checks facet material against durable checkpoint blob bytes.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p8/y5/src/fold_k3.rs
    controls_tests: [test_jr_r1_matrix_layout, test_jr_r8_hex_lower, test_jr_r7_known_good, test_jr_r6_reduce_hex, test_jr_r13_ablate_k3]
  - id: B
    path: environment/p8/y4/src/pack_w2.rs
    controls_tests: [test_jr_r18_durable_first, test_jr_r3_rc_fields]
  - id: C
    path: environment/m3/k82/src/seq_n4.rs
    controls_tests: [test_jr_r2_pair_hex, test_jr_r4_label_text, test_jr_r5_width_max, test_jr_r15_ablate_order, test_jr_r16_k7_trap, test_jr_r20_replay_hook]
  - id: D
    path: environment/p8/core/src/emit_q1.rs
    controls_tests: [test_jr_r10_fresh_pipeline, test_jr_r11_twice_same, test_jr_r12_sens_steps, test_jr_r9_total_count, test_jr_r17_ablate_wit]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/m3/k82/src/stack_mix.rs
  kind: module
  rhymes_with: seq_n4
  non_fix_purpose: Buffers ephemeral combine events for offline benchmarks unrelated to replay combine ordering.
- path: environment/p8/y5/src/sp_help.rs
  kind: module
  rhymes_with: fold_k3
  non_fix_purpose: Applies offline fold transforms for diagnostics without participating in generation authority.
- path: environment/p8/core/src/gauge_m.rs
  kind: helper
  rhymes_with: emit_q1
  non_fix_purpose: Formats human-readable summaries for support tooling without checkpoint witness cross-check.
- path: environment/p8/core/src/blob_chk.rs
  kind: module
  rhymes_with: emit_q1
  non_fix_purpose: Checkpoint blob parsing helpers co-resident with witness slow path; not a standalone flip location.
- path: environment/p8/core/src/probe.rs
  kind: helper
  rhymes_with: emit_q1
  non_fix_purpose: Scratch buffers for offline probe runs without checkpoint witness authority.
```

#### code_forbidden_tokens

```
journal, replay, generation, skew, partial, verifier, target, closure, echo, mirror, pairs, settled, coherent, locked, sources, rebuild, manual, static, aggregate, disagree, facet, material, sync, cache, stamp, debug, release, host, sufficient, survives, deterministic, replay_report, lane_ids, facet_hex, trace_digest, gen_span, sync_label, skew_code, chk_rc, seg_rc, roll_rc, rows_total, rows, summary, workspace, check, overwrite, repeat, tampered, fresh, twice, ablate, flip, trap, alpha, beta, gamma, alpha_echo, beta_echo, gamma_echo, identities, stale, ancestry, counters, incoherent, regeneration, reconcil, drift, provenance, shadow, incremental, artifacts, reducer, scenario, canonical, destructive, invariants, restart, generalization, perm, extra, tier_span, sync_status, drift_code, mk, k81, k84, m2, m4, p7, p9, mix_r7, merge_u3, ord_g2, rk1_snap, stale_bind, case_lane
```

### difficulty_mechanism_plan

- mechanisms: partial_observability_experiment_design, deceptive_but_valid_local_evidence, stateful_multi_step_dependencies, false_green_intermediate_states, cross_file_cross_format_invariants, rollback_recovery_requirements, buried_local_constraints
- adversarial_layers_count: 7
- fairness_guardrails: All tested formulas and primary lane ids are public; deterministic drills; no timing/latency thresholds
- mechanism: partial_observability_experiment_design
  placement: runtime fprint probe surface vs durable index_h checkpoint bytes visible in different fixtures
  why_model_misses_it: models treat runtime probe stream as authoritative after partial recovery
  fairness_guardrail: test_jr_r18_durable_first and notes.md schema without naming wiring
- mechanism: deceptive_but_valid_local_evidence
  placement: environment/p8/core/src/fprint.rs runtime-visible generation probes after partial rollback
  why_model_misses_it: Stops at settled sync_label with disagreeing echo pairs
  fairness_guardrail: Tests require pair agreement (test_jr_r2_pair_hex)
- mechanism: stateful_multi_step_dependencies
  placement: cargo rebuild then jr then JSON report under /app/output/
  why_model_misses_it: Patches without locked rebuild graph
  fairness_guardrail: build_cmds documents commands
- mechanism: false_green_intermediate_states
  placement: environment/p8/core/src/gauge_m.rs intermediate closure counters before replay completes
  why_model_misses_it: Aggregate line masks per-row skew on echoes
  fairness_guardrail: test_jr_r19_premature and test_jr_r15_ablate_order
- mechanism: cross_file_cross_format_invariants
  placement: environment/p8/core/src/emit_q1.rs vs chk_blob.json and data seeds
  why_model_misses_it: JSON shape passes without checkpoint witness cross-check
  fairness_guardrail: Pipeline rebuild tests (test_jr_r10_fresh_pipeline, test_jr_r17_ablate_wit)
- mechanism: rollback_recovery_requirements
  placement: pack_w2 after partial rollback; index_h vs fprint
  why_model_misses_it: chk_rc reads 1 while seg_rc/roll_rc diverge
  fairness_guardrail: test_jr_r14_flip_both and test_jr_r18_durable_first
- mechanism: buried_local_constraints
  placement: fold_k3 must include prev_family shift, not step_ix alone, for cross-partition facet material
  why_model_misses_it: looks like optional lineage field
  fairness_guardrail: ablation test reverts fold_k3 body

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: derive trace_digest from m3/k82 main.rs header; run build_cmds hook sequence; one careful human can satisfy using notes.md and bundled fixtures only
- shortcut_audit: static JSON, pytest edits, digest hardcode, hand-edited checkpoint blob, skip cargo; verifier-offline pytest/cargo baked in Dockerfile; test.sh performs no runtime network installs under allow_internet=false
- ablation_plan: revert fold_k3 only, pack_w2 only, seq_n4 only, emit_q1 only — each drops pass rate on disjoint test subsets
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=frontier agents; Part E post-upload classification if worst-model accuracy exceeds 20%
- verifier_offline: pytest and cargo locked in Dockerfile; test.sh performs no runtime network installs under allow_internet=false
- post_upload_difficulty: final Hard/Medium/Easy label follows platform agent runs (Part E)

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when all semantic pytest passes including authority-split and rollback replay traps

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step cross-test coupling via ablations and authority traps
- local_only_data: true
- sidecar_or_protocol_notes: single-container Rust workspace; fixtures under environment/data only
- long_context_token_floor: n/a
