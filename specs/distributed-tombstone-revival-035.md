### Decision

GO — Attempt 2. Bank-ready seed `distributed-tombstone-revival-035` passes idea validation on the approved **overlay-lowerdir-stale-bind** Rust/Cargo construction mold (`accepted tasks/overlay-lowerdir-stale-bind.zip`), reframed to **adversarial_generalization** + **debugging** + **state_recovery_crash_consistency** with **generation skew during filesystem recovery** topology. Three mandated discoveries, held-out `perm_extra.toml` permutations, four-location flipping-point contract, and constraint-complete public obligations without leaking canonical recovery path, replay phase ordering, or tombstone-index vs mount-probe authority. Attempt 2 renamed `test_s8_hex_lower` → `test_s8_narrow_chars` to clear forbidden-noun collision on `lower`.

### Metadata

- version: 2
- Task name: distributed-tombstone-revival-035
- Title: Tombstone revival skew
- Category: debugging
- Task shape: adversarial_generalization
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["rust", "cargo-workspace", "tombstone-revival", "generation-skew", "filesystem-recovery", "false-green", "offline-build"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, per-slot facet answer tables, or narrative causal chains that name fix coordinates.

### Public contract

After partial filesystem recovery, visible checkpoint and mount probes can read settled while tombstone replay still revives retired keys from stale generation ancestry. Echo lanes disagree on closure counters and facet material even when the aggregate summary line looks mostly fine.

Repair sources under `/app` so the workspace release build and `/app/target/release/tr` write `/app/output/skew_report.json`. Lane ids are in `/app/docs/lane_ids.txt`.

The report has `rows` and `summary`. Each row records `lane_id`, `dsk_rc`, `gen_rc`, `mnt_rc` (each `1` when that closure dimension passes, else `0`), `skew_code`, and `facet_hex` (exactly 16 lowercase hexadecimal digits). The summary records `rows_total`, `sync_label`, `skew_span`, and `trace_digest`. Mirror pairs bind `lower` with `lower_echo`, `mid` with `mid_echo`, and `leaf` with `leaf_echo`. Coherent runs keep `skew_code` at `0` on every row, all three closure counters at `1`, matching `facet_hex` on each pair, and `sync_label` reading `settled`. Incoherent runs break at least one of those conditions (closure counters may read `0` or `sync_label` may differ from `settled`). The module comment above `/app/m5/k85/src/main.rs` defines `skew_span` and `trace_digest` reduction; read that header instead of hand-writing JSON. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

**Adversarial generalization:** A correct fix must survive every permutation scenario encoded in `/app/data/perm_extra.toml`. Instruction names the file and the generalization rule only—not individual held-out entries or per-lane facet answers.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/build_cmds.txt` for locked workspace compile and pytest argv details (environment-specific CLI semantics for filesystem recovery hooks).

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category_profile = "state_recovery_crash_consistency"`
- path: instruction.md
  role: natural public task prompt (constraint-complete adversarial generalization; mirrors Public contract above)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation, permutation, and pipeline traps
- path: solution/solve.sh
  role: oracle applying oracle.patch and locked rebuild
- path: environment/Dockerfile
  role: build definition; pre-install rustc workspace tooling, pytest, tmux, asciinema, and locked deps
- path: construction_manifest.json
  role: local authoring artifact mirroring Construction manifest below

### task_files

- path: environment/m5/k85/src/main.rs
  role: release driver wiring recovery slots and summary reduction header
- path: environment/m5/k85/src/ord_h5.rs
  role: oracle frontier C — combine/invalidate ordering under filesystem replay
- path: environment/m5/k85/src/stack_mix.rs
  role: decoy stack helper (non-fix)
- path: environment/m5/k85/src/step_key.rs
  role: decoy key helper (non-fix)
- path: environment/p10/y5/src/mix_q3.rs
  role: oracle frontier A — generation fold mixing tombstone lineage
- path: environment/p10/y5/src/body.rs
  role: facet body materialization for y5 crate
- path: environment/p10/y5/src/lib.rs
  role: y5 crate root exports
- path: environment/p10/y5/src/sp_help.rs
  role: decoy stamp utilities (non-fix)
- path: environment/p10/y4/src/pack_v4.rs
  role: oracle frontier B — pack merge with durable storage refresh
- path: environment/p10/y4/src/body.rs
  role: pack body materialization for y4 crate
- path: environment/p10/y4/src/lib.rs
  role: y4 crate root exports
- path: environment/p10/y4/src/hold_buf.rs
  role: decoy hold buffer (non-fix)
- path: environment/p10/y4/src/contour.rs
  role: decoy contour table (non-fix)
- path: environment/p10/y6/src/twist_m6.rs
  role: low-level side/gate ordering primitive used by ord_h5 (decoy rhymes with ord_h5)
- path: environment/p10/y6/src/idx_m6.rs
  role: durable tombstone index authority (witness surface; not a flip location)
- path: environment/p10/y6/src/body.rs
  role: pace body materialization for y6 crate
- path: environment/p10/y6/src/lib.rs
  role: y6 crate root exports
- path: environment/p10/y6/src/stride_scan.rs
  role: decoy stride catalog scanner (non-fix)
- path: environment/p10/core/src/form_k2.rs
  role: oracle frontier D — cross-format facet materialization path with snap witness cross-check
- path: environment/p10/core/src/blob_chk.rs
  role: snap blob witness parsing module co-resident with form_k2 slow path
- path: environment/p10/core/src/gauge_m6.rs
  role: false-green intermediate closure counters before replay completes
- path: environment/p10/core/src/mnt_probe.rs
  role: runtime-visible mount probe surface (contrasts idx_m6 authority)
- path: environment/p10/core/src/lib.rs
  role: core crate root exports
- path: environment/p10/core/src/alias_stub.rs
  role: decoy alias table (non-fix)
- path: environment/p10/core/src/kind.rs
  role: row kind tagging helpers
- path: environment/p10/core/src/pad_util.rs
  role: decoy padding utilities (non-fix)
- path: environment/p10/core/src/stack.rs
  role: decoy stack reducer (non-fix)
- path: environment/p10/core/src/apply.rs
  role: decoy apply shim (non-fix)
- path: environment/p10/core/src/family.rs
  role: generation family tagging
- path: environment/p10/core/src/mesh.rs
  role: decoy mesh helper (non-fix)
- path: environment/data/ladder_tbl.toml
  role: seeded bind ladder for lower primary lane
- path: environment/data/channel.toml
  role: channel weights for mid primary lane
- path: environment/data/seed.json
  role: generation seed manifest
- path: environment/data/weights.tsv
  role: leaf primary lane weight table
- path: environment/data/snap_blob.json
  role: durable snap witness bytes cross-checked by slow path
- path: environment/data/perm_extra.toml
  role: held-out permutation scenario table (adversarial generalization)
- path: environment/docs/lane_ids.txt
  role: comma-separated primary lane id table (held-out permutations excluded)
- path: environment/docs/build_cmds.txt
  role: cargo/pytest argv and filesystem recovery hook notes
- path: environment/docs/notes.md
  role: row/summary schema and mirror-pair contract visible to the agent
- path: environment/Cargo.toml
  role: workspace root
- path: environment/Cargo.lock
  role: locked dependency graph

### fix_frontier

- count: 4
- distribution: `environment/p10/y5/src/mix_q3.rs`, `environment/p10/y4/src/pack_v4.rs`, `environment/m5/k85/src/ord_h5.rs`, `environment/p10/core/src/form_k2.rs` (distinct roots m5, p10/y5, p10/y4, p10/core)
- naming_policy: Opaque identifiers (`mix_q3`, `pack_v4`, `ord_h5`, `form_k2`) on neutral parameter names; no instruction nouns on fix path
- forbidden_stems: partial, filesystem, recovery, tombstone, generation, skew, revival, authority, settled, facet, digest, echo, mirror, reconcile, report, driver, mount, probe, regeneration, corruption, ancestry, retired, permutations, coherent, incoherent, static, manual, verifier, rebuild, locked, workspace, generalization, survives, aggregate, disagree, closure, stamps, facets, material, summary, probes, checkpoint, reconciliation, restart, drift, sources, primary, held-out, hints, skew_report, lane_ids, build_cmds, facet_hex, trace_digest, skew_span, sync_label, skew_code, dsk_rc, gen_rc, mnt_rc, rows_total, lower_echo, mid_echo, leaf_echo, snap_blob, perm_extra, overwrite, consecutive, lower, mid, leaf
- helpers_policy: Co-resident crate roots and rhyming decoys perform credible adjacent work; frontier stays thin at four fix symbols with blob_chk parsing helpers declared in decoy_manifest and driver/index orchestration separate
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: regenerated JSON rows, integer closure counters, derived trace_digest, echo bind equality, held-out permutation traps, ablation incoherence, pipeline overwrite, tomb witness cross-check
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction.md; static golden report under tests/; readiness fields named `*_ok` in instruction prose tied 1:1 to fix-path grep

### task_shape

- type: adversarial_generalization
- instruction_framing: constraint-complete
- hardness_source: adversarial generalization across conflicting recovery evidence surfaces under destructive replay and partial filesystem recovery
- collapse_risk: Leaking canonical recovery path, replay phase ordering, or tombstone-index vs mount-probe authority collapses to a local one-crate patch

### category_profile

- challenge_family: generation_skew_filesystem_recovery
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: partial recovery/restart workflow, durability guarantee for skew_report artifact, recovery/rebuild command surface, post-recovery observable state, mirror pairs, trace_digest formula home in main.rs header, lane_ids.txt primary table, existence of perm_extra generalization rule, build_cmds recovery argv
- forbidden_instruction_leaks: journal/checkpoint internals, broken recovery phase, corrupt record location, replay function names, cleanup path, exact phase ordering, patch functions, cross-format bypass site, canonical recovery sequence, per-record facet answers
- category_specific_hardness_bar: Partial writes, replay, cleanup, idempotent rerun safety, and restart-after-partial-recovery must coordinate; durable tombstone index must diverge from runtime-visible mount probes until all four fix roots align; held-out permutations must survive
- category_specific_verifier_risks: nondeterministic crash timing, hidden snapshot expectations, verifier reading private internals, single stale-file repair shortcut, clean-build-only pass
- coverage_role: Adds state_recovery_crash_consistency adversarial_generalization coverage for generation skew during filesystem recovery using the approved overlay Cargo mold with distinct tombstone/slot semantics

### satisfiability_risk

- rc2_planned_name_risk: low — neutral `m5`/`p10` roots and opaque symbols (`mix_q3`, `pack_v4`, `ord_h5`, `form_k2`)
- gx9_contract_risk: low — tests derive verdicts from trace_digest recompute and bind equality, not per-slot answer tables in instruction
- cr1_symbol_frontier_risk: low — four substantive Rust modules plus explicit flipping-point contract
- hidden_contract_risk: medium — held-out permutations in perm_extra.toml; instruction states existence and generalization rule only

### actionability_plan

- verifier_command_visible: `cargo build --release --locked`, `/app/target/release/tr`, `/app/docs/build_cmds.txt` recovery argv
- source_fix_intent_visible: yes — repair under `/app` without naming modules
- generated_output_rule_visible: skew_report.json path, mirror pairs, coherent predicates, regeneration requirement
- exact_formula_home: module comment above `environment/m5/k85/src/main.rs`
- schema_home: instruction public contract; optional `environment/schemas/skew_row.schema.json` for author lint only

### waiver_plan

- waivers_expected: false
- waiver_rationale: Overlay mold keeps contracts observation-shaped with solver-visible formula homes; deterministic offline Cargo rebuilds

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/overlay-lowerdir-stale-bind.zip` (overlay-lowerdir-stale-bind) for verifier shape, flipping-point ablations, workspace+driver pipeline traps, and three-plus crate flipping-point discipline; reframed from overlay lowerdir repair to adversarial_generalization generation skew during filesystem recovery + state_recovery_crash_consistency with held-out perm_extra permutations. No promoted entry in `docs/reference_tasks/index.json` matches this exact profile combo; abi-rebuild-mismatch covers multi-crate regeneration discipline only.

### realism_source

- source_type: real_system
- evidence_basis: Minimized from distributed filesystem tombstone revival postmortems and overlay lowerdir stale-bind recovery incidents (approved zip)
- upstream_or_synthetic_rationale: Preserves authority split, false-green intermediate closure, cross-format emit bypass, and permutation generalization without proprietary cluster code
- minimization_preserves: Durable tombstone index vs runtime mount probe divergence, intermediate gauge closure before replay completes, JSON fast path without snap_blob cross-check, held-out ordering rows in perm_extra.toml
- synthetic_exception_review: not required

### Failure topology

Visible recovery checks (checkpoint/mount probes, aggregate sync_label) can read settled while retired keys resurrect under stale generation tags because three mechanisms interact: the durable tombstone catalog in idx_m6 remains authoritative for revival ordering but the driver’s runtime mount-probe surface answers first after partial filesystem recovery; ord_h5 marks closure counters true on an intermediate replay pass before twist_m6/phase ordering finishes; and form_k2 fast path materializes JSON facets without reconciling snap_blob.json against bundled TOML/TSV seeds and pack-merged storage. Each defect is locally plausible; together they produce generation skew that only appears after rebuild, driver rerun, echo-bind comparison, or held-out permutation sweeps — matching the bank-ready discovery plan without naming fix coordinates in the prompt.

### Environment shape

Rust Cargo workspace rooted at `/app` with opaque crates under `environment/m5/k85` (driver), `environment/p10/y5` (stamp fold), `environment/p10/y4` (pack merge), `environment/p10/y6` (index/twist), and `environment/p10/core` (emit/gauge/mnt_probe). Seed data lives in `environment/data/`; operator docs in `environment/docs/`. Single-container only; fork overlay reference layout density (≥20 non-Docker environment files). Step 2b may fork `accepted tasks/overlay-lowerdir-stale-bind.zip` environment/ then reframe docs, field names, and broken semantics; do not shrink below 20 non-Docker environment files.

### Required artifacts

Standard TB3 task tree under `tasks/distributed-tombstone-revival-035/`: instruction.md, task.toml (`allow_internet = false`, `category_profile = state_recovery_crash_consistency`), output_contract.toml, construction_manifest.json, Dockerfile with locked cargo/pytest/tmux/asciinema, tests/test.sh, tests/test_outputs.py (≥20 tests), solution/solve.sh + oracle.patch, full environment workspace per Initial Draft Commitments.

### Test plan

- test_s1_shape_only: JSON layout; primary lane ids match lane_ids.txt
- test_s2_agree_hex: mirror binds agree on facet material and rc fields when coherent
- test_s3_rc_fields: coherent run — skew_code 0 and three rc fields 1 on all rows
- test_s4_label_text: summary sync_label reads settled when emission coherent
- test_s5_width_max: skew_span equals max abs skew_code
- test_s6_reduce_hex: summary trace_digest matches main.rs header reduction from rows
- test_s7_known_good: trace_digest matches known-good repaired emission
- test_s8_narrow_chars: facet_hex sixteen lowercase hex chars
- test_s9_total_count: rows_total integer equals row vector length
- test_s10_fresh_pipe: tampered hand-written JSON replaced by pipeline rebuild
- test_s11_twice_same: consecutive pipeline runs identical
- test_s12_sens_steps: mutating lower ladder data changes facet material and digest
- test_s13_ablate_fold: reverting mix_q3 fold breaks coherence
- test_s14_flip_both: reverting pack_v4 and mix_q3 together breaks pipeline
- test_s15_ablate_order: broken ord_h5 combine wiring + stock twist_m6 helper breaks closure
- test_s16_all_extras: every held-out permutation scenario in perm_extra.toml survives after fix
- test_s17_ablate_drop: reverting form_k2 snap witness cross-check breaks mnt_rc vs snap_blob bytes
- test_s18_witness_first: durable idx_m6 precedes runtime mnt_probe reads after profile drill
- test_s19_premature: gauge_m6 settled label with disagreeing mirror binds fails until replay completes
- test_s20_cmd_hook: build_cmds command sequence required for tr filesystem recovery success

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests (cap 0.5).

### Drafting guardrails

Instruction is constraint-complete about report schema, mirror binds, coherence predicates, and permutation generalization—without naming `mix_q3`, `pack_v4`, `ord_h5`, `form_k2`, replay phase ordering, idx_m6 vs mnt_probe wiring, or cross-format bypass. Do not copy overlay “lowerdir/mount” wording verbatim. Ban instruction nouns from fix-path code symbols and test identifiers. No boolean readiness verdict fields in planned outputs. Do not ship golden skew_report.json in repo.

### Triviality Ledger

- Hand-writing skew_report.json fails test_s10_fresh_pipe because verifier reruns cargo + tr.
- Fixing only mix_q3 without pack_v4 durable refresh fails test_s14_flip_both and bind coherence subsets.
- Fixing only ord_h5 without twist_m6 primitive contract fails test_s15_ablate_order and test_s16_all_extras.
- Copying one row from a golden fixture fails test_s7_known_good and test_s12_sens_steps.
- Trusting gauge_m6 settled label while mirror binds disagree fails test_s19_premature until ord_h5 ordering and tombstone authority align.
- Bumping one Cargo.toml dependency version fails ablation suites requiring semantic fixes across four roots.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle must change semantics in four roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays constraint-complete without cause-revealing “form_k2 skips snap witness” sentences.
- RC5/RC6: schemas and digest home in main.rs header; no boolean answer grid in instruction.
- RC7/GX3: solve.sh coordinated across four modules with substantive bodies.
- GX9/GX10: derived digests and bind equality over scenario boolean tables.
- GX4/GX5: ablation tests patch sources in-container; expectations computed in test file.
- CR1/CR2: honor symbol table and flipping-point concentration cap 0.5.

### Initial Draft Commitments

- tasks/distributed-tombstone-revival-035/task.toml
- tasks/distributed-tombstone-revival-035/instruction.md
- tasks/distributed-tombstone-revival-035/output_contract.toml
- tasks/distributed-tombstone-revival-035/construction_manifest.json
- tasks/distributed-tombstone-revival-035/tests/test.sh
- tasks/distributed-tombstone-revival-035/tests/test_outputs.py
- tasks/distributed-tombstone-revival-035/solution/solve.sh
- tasks/distributed-tombstone-revival-035/solution/oracle.patch
- tasks/distributed-tombstone-revival-035/environment/Dockerfile
- tasks/distributed-tombstone-revival-035/environment/Cargo.toml
- tasks/distributed-tombstone-revival-035/environment/Cargo.lock
- tasks/distributed-tombstone-revival-035/environment/m5/k85/Cargo.toml
- tasks/distributed-tombstone-revival-035/environment/m5/k85/src/main.rs
- tasks/distributed-tombstone-revival-035/environment/m5/k85/src/ord_h5.rs
- tasks/distributed-tombstone-revival-035/environment/m5/k85/src/stack_mix.rs
- tasks/distributed-tombstone-revival-035/environment/m5/k85/src/step_key.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y5/Cargo.toml
- tasks/distributed-tombstone-revival-035/environment/p10/y5/src/mix_q3.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y5/src/body.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y5/src/lib.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y5/src/sp_help.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y4/Cargo.toml
- tasks/distributed-tombstone-revival-035/environment/p10/y4/src/pack_v4.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y4/src/body.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y4/src/hold_buf.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y4/src/contour.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y4/src/lib.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y6/Cargo.toml
- tasks/distributed-tombstone-revival-035/environment/p10/y6/src/twist_m6.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y6/src/idx_m6.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y6/src/body.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y6/src/stride_scan.rs
- tasks/distributed-tombstone-revival-035/environment/p10/y6/src/lib.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/Cargo.toml
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/form_k2.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/blob_chk.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/gauge_m6.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/mnt_probe.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/kind.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/family.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/alias_stub.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/pad_util.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/stack.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/apply.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/mesh.rs
- tasks/distributed-tombstone-revival-035/environment/p10/core/src/lib.rs
- tasks/distributed-tombstone-revival-035/environment/data/ladder_tbl.toml
- tasks/distributed-tombstone-revival-035/environment/data/channel.toml
- tasks/distributed-tombstone-revival-035/environment/data/seed.json
- tasks/distributed-tombstone-revival-035/environment/data/weights.tsv
- tasks/distributed-tombstone-revival-035/environment/data/snap_blob.json
- tasks/distributed-tombstone-revival-035/environment/data/perm_extra.toml
- tasks/distributed-tombstone-revival-035/environment/docs/lane_ids.txt
- tasks/distributed-tombstone-revival-035/environment/docs/build_cmds.txt
- tasks/distributed-tombstone-revival-035/environment/docs/notes.md

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p10/y5/src/mix_q3.rs
  symbol: mix_q3
  kind: function
  signature: pub fn mix_q3(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Folds step and family tags into stamp bits for report facets.
- path: environment/p10/y4/src/pack_v4.rs
  symbol: pack_v4
  kind: function
  signature: pub fn pack_v4(state: &mut PackState, incoming: &PackState, stamp_b: u32) -> u32
  purpose: Merges incoming pack bytes into durable storage during bind steps.
- path: environment/m5/k85/src/ord_h5.rs
  symbol: ord_h5
  kind: function
  signature: pub fn ord_h5(gate_first: bool, side: impl FnMut(), gate: impl FnMut()) -> u32
  purpose: Orders side-effect callbacks during per-lane combine steps under recovery ordering.
- path: environment/p10/y6/src/twist_m6.rs
  symbol: twist_m6
  kind: function
  signature: pub fn twist_m6(gate_first: bool, mut side: impl FnMut(), mut gate: impl FnMut()) -> u32
  purpose: Low-level side/gate ordering primitive used by ord_h5.
- path: environment/p10/core/src/form_k2.rs
  symbol: form_k2
  kind: function
  signature: pub fn form_k2(facet_hex: &str, witness_path: &Path) -> bool
  purpose: Cross-checks facet material against durable snap witness bytes.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p10/y5/src/mix_q3.rs
    controls_tests: [test_s1_shape_only, test_s6_reduce_hex, test_s7_known_good, test_s8_narrow_chars, test_s13_ablate_fold]
  - id: B
    path: environment/p10/y4/src/pack_v4.rs
    controls_tests: [test_s14_flip_both, test_s3_rc_fields]
  - id: C
    path: environment/m5/k85/src/ord_h5.rs
    controls_tests: [test_s2_agree_hex, test_s4_label_text, test_s5_width_max, test_s15_ablate_order, test_s16_all_extras, test_s20_cmd_hook]
  - id: D
    path: environment/p10/core/src/form_k2.rs
    controls_tests: [test_s10_fresh_pipe, test_s11_twice_same, test_s12_sens_steps, test_s9_total_count, test_s17_ablate_drop, test_s18_witness_first, test_s19_premature]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/m5/k85/src/stack_mix.rs
  kind: module
  rhymes_with: ord_h5
  non_fix_purpose: Buffers ephemeral combine events for offline benchmarks unrelated to replay combine ordering.
- path: environment/p10/y5/src/sp_help.rs
  kind: module
  rhymes_with: mix_q3
  non_fix_purpose: Applies offline fold transforms for diagnostics without participating in stamp authority.
- path: environment/p10/core/src/gauge_m6.rs
  kind: helper
  rhymes_with: form_k2
  non_fix_purpose: Formats human-readable summaries for support tooling without snap witness cross-check.
- path: environment/p10/core/src/blob_chk.rs
  kind: module
  rhymes_with: form_k2
  non_fix_purpose: Snap blob parsing helpers co-resident with witness slow path; not a standalone flip location.
```

#### code_forbidden_tokens

```
partial, filesystem, recovery, tombstone, generation, skew, restart, reconciliation, echo, closure, stamps, facets, aggregate, revival, settled, incoherent, static, manual, verifier, rebuild, mirror, pairs, durable, runtime, authority, corruption, regeneration, drift, locked, workspace, permutations, survives, coherent, report, driver, sources, primary, generalization, scenario, counters, material, summary, probes, checkpoint, mount, retired, ancestry, disagree, hand-writing, validate, encoded, individual, held-out, answers, hints, skew_report, lane_ids, build_cmds, facet_hex, trace_digest, skew_span, sync_label, skew_code, dsk_rc, gen_rc, mnt_rc, rows_total, lower_echo, mid_echo, leaf_echo, snap_blob, perm_extra, overwrite, consecutive, lower, mid, leaf
```

### difficulty_mechanism_plan

- mechanisms: partial_observability_experiment_design, buried_local_constraints, false_green_intermediate_states, rollback_recovery_requirements, cross_file_cross_format_invariants, environment_specific_cli_semantics
- adversarial_layers_count: 6
- fairness_guardrails: All tested formulas and primary slot ids are public; deterministic drills; no timing/latency thresholds
- mechanism: partial_observability_experiment_design
  placement: environment/p10/core/src/mnt_probe.rs vs environment/p10/y6/src/idx_m6.rs; solver must compare rebuild outputs across echo binds
  why_model_misses_it: Agents trust runtime-visible mount probes after partial recovery without reconciling durable tombstone index reads
  fairness_guardrail: Instruction names observable skew_report contract and mirror binds; tests require bind agreement
- mechanism: buried_local_constraints
  placement: environment/p10/y5/src/mix_q3.rs lineage fold vs shipped half-payload fold
  why_model_misses_it: facet_hex looks well-formed while skew_code stays zero incorrectly on revival slots
  fairness_guardrail: Ablation test reverts fold and expects incoherence
- mechanism: false_green_intermediate_states
  placement: environment/p10/core/src/gauge_m6.rs intermediate closure counters before replay completes
  why_model_misses_it: Aggregate sync_label masks per-row skew on echo slots
  fairness_guardrail: test_s19_premature and test_s15_ablate_order
- mechanism: rollback_recovery_requirements
  placement: environment/p10/y4/src/pack_v4.rs after partial recovery; idx_m6 vs mnt_probe
  why_model_misses_it: mnt_rc reads 1 while gen_rc/dsk_rc diverge after partial filesystem recovery
  fairness_guardrail: test_s14_flip_both and test_s18_witness_first
- mechanism: cross_file_cross_format_invariants
  placement: environment/p10/core/src/form_k2.rs vs snap_blob.json and data seeds
  why_model_misses_it: JSON shape passes without snap witness cross-check against TOML/TSV seeds
  fairness_guardrail: Pipeline rebuild tests test_s10_fresh_pipe and test_s17_ablate_drop
- mechanism: environment_specific_cli_semantics
  placement: environment/docs/build_cmds.txt argv consumed by tr filesystem recovery hook
  why_model_misses_it: Agents run generic cargo loops without documented recovery argv sequence
  fairness_guardrail: build_cmds ships in docs; test_s20_cmd_hook

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: derive trace_digest from m5/k85 main.rs header; run build_cmds hook sequence; one careful human can satisfy using notes.md and bundled fixtures only
- shortcut_audit: static JSON, pytest edits, digest hardcode, hand-edited snap blob, skip cargo; verifier-offline pytest/cargo baked in Dockerfile; test.sh performs no runtime network installs under allow_internet=false
- ablation_plan: revert mix_q3 only, pack_v4 only, ord_h5 only, form_k2 only — each drops pass rate on disjoint test subsets; remove test_s16_all_extras and expect easier pass rate
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=frontier agents; Part E post-upload Hard/Medium/Easy classification on worst/best model accuracy

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when all semantic pytest passes including test_s16_all_extras

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step cross-test coupling via permutations and ablations
- local_only_data: true
- sidecar_or_protocol_notes: single-container Rust workspace; fixtures under environment/data only; no network services
- long_context_token_floor: n/a
