### Decision

GO — Attempt 1 (validated). Bank-ready seed `incremental-build-shadow-artifacts-023` passes idea validation on the approved **overlay-lowerdir-stale-bind** Rust/Cargo construction mold (`accepted tasks/_ref/overlay-lowerdir-stale-bind/`), reframed to **adversarial_generalization** + **debugging** + **build_dependency_toolchain** with incremental rebuild provenance drift topology. Three mandated discoveries, held-out `extra_targets.toml` permutations, four-location flipping-point contract, and constraint-complete public obligations without leaking canonical recovery path, replay phase ordering, or stamp-cache vs fingerprint authority.

### Metadata

- version: 2
- Task name: incremental-build-shadow-artifacts-023
- Title: Incremental shadow provenance
- Category: debugging
- Task shape: adversarial_generalization
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["rust", "cargo-incremental", "provenance-drift", "shadow-stamps", "json-report", "false-green", "offline-build"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, per-target facet answer tables, or narrative causal chains that name fix coordinates.

### Public contract

After partial workspace recovery, `locked workspace check`-visible surfaces can read settled while shadow-stamp replay still revives stale artifact identities from mismatched provenance. Echo build targets disagree on closure counters and facet material even when the aggregate summary line looks mostly fine.

Repair sources under `/app` so the workspace release build and `/app/target/release/ib` write `/app/output/provenance_report.json`. Primary target ids are in `/app/docs/tgt_ids.txt`.

The report has `rows` and `summary`. Each row records `target_id`, `cache_rc`, `gen_rc`, `stamp_rc` (each `1` when that closure dimension passes, else `0`), `drift_code`, and `facet_hex` (exactly 16 lowercase hexadecimal digits). The summary records `rows_total`, `sync_label`, `span_band`, and `trace_digest`. Mirror pairs bind `debug` with `debug_echo`, `release` with `release_echo`, and `host` with `host_echo`. Coherent runs keep `drift_code` at `0` on every row, all three closure counters at `1`, matching `facet_hex` on each pair, and `sync_label` reading `settled`. Incoherent runs break at least one of those conditions (closure counters may read `0` or `sync_label` may differ from `settled`). The module comment above `/app/m4/k84/src/main.rs` defines `span_band` and `trace_digest` reduction; read that header instead of hand-writing JSON. Static or manual JSON writes are not sufficient; the verifier rebuilds from fixed sources and reruns the driver.

**Adversarial generalization:** A correct fix must survive every permutation scenario encoded in `/app/data/perm_extra.toml`. Instruction names the file and the generalization rule only—not individual held-out rows or per-target facet answers.

Verifier tests rebuild from sources, run the driver, and validate the report. See `/app/docs/operator_cmds.txt` for locked workspace compile and pytest argv details (environment-specific CLI semantics for incremental replay hooks).

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "debugging"`
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

- path: environment/m4/k84/src/main.rs
  role: release driver wiring build targets and summary reduction header
- path: environment/m4/k84/src/ord_g2.rs
  role: oracle frontier C — combine/invalidate ordering under incremental replay
- path: environment/m4/k84/src/stack_mix.rs
  role: decoy stack helper (non-fix)
- path: environment/m4/k84/src/step_key.rs
  role: decoy key helper (non-fix)
- path: environment/p9/y5/src/mix_r7.rs
  role: oracle frontier A — stamp fold mixing provenance lineage
- path: environment/p9/y5/src/body.rs
  role: facet body materialization for y5 crate
- path: environment/p9/y5/src/lib.rs
  role: y5 crate root exports
- path: environment/p9/y5/src/sp_help.rs
  role: decoy stamp utilities (non-fix)
- path: environment/p9/y4/src/merge_u3.rs
  role: oracle frontier B — pack merge with durable shadow-stamp refresh
- path: environment/p9/y4/src/body.rs
  role: pack body materialization for y4 crate
- path: environment/p9/y4/src/lib.rs
  role: y4 crate root exports
- path: environment/p9/y4/src/hold_buf.rs
  role: decoy hold buffer (non-fix)
- path: environment/p9/y4/src/contour.rs
  role: decoy contour table (non-fix)
- path: environment/p9/y6/src/twist_p9.rs
  role: low-level side/gate ordering primitive used by ord_g2 (decoy rhymes with ord_g2)
- path: environment/p9/y6/src/index_r.rs
  role: durable stamp-cache index authority (witness surface; not a flip location)
- path: environment/p9/y6/src/body.rs
  role: pace body materialization for y6 crate
- path: environment/p9/y6/src/lib.rs
  role: y6 crate root exports
- path: environment/p9/y6/src/stride_scan.rs
  role: decoy stride catalog scanner (non-fix)
- path: environment/p9/core/src/rk1_snap.rs
  role: oracle frontier D — cross-format row materialization path
- path: environment/p9/core/src/blob_chk.rs
  role: snap blob witness parsing module co-resident with rk1_cross slow path
- path: environment/p9/core/src/gauge_r.rs
  role: false-green intermediate closure counters before replay completes
- path: environment/p9/core/src/fprint.rs
  role: runtime-visible fingerprint surface (contrasts index_r authority)
- path: environment/p9/core/src/lib.rs
  role: core crate root exports
- path: environment/p9/core/src/alias_stub.rs
  role: decoy alias table (non-fix)
- path: environment/p9/core/src/kind.rs
  role: row kind tagging helpers
- path: environment/p9/core/src/row_help.rs
  role: decoy row utilities (non-fix)
- path: environment/p9/core/src/stack.rs
  role: decoy stack reducer (non-fix)
- path: environment/p9/core/src/apply.rs
  role: decoy apply shim (non-fix)
- path: environment/p9/core/src/family.rs
  role: provenance family tagging
- path: environment/p9/core/src/mesh.rs
  role: decoy mesh helper (non-fix)
- path: environment/data/seg_tbl.toml
  role: seeded bind ladder for debug target
- path: environment/data/channel.toml
  role: channel weights for release target
- path: environment/data/seed.json
  role: generation seed manifest
- path: environment/data/weights.tsv
  role: host target weight table
- path: environment/data/snap_blob.json
  role: durable stamp witness bytes cross-checked by slow path
- path: environment/data/perm_extra.toml
  role: held-out permutation scenario table (adversarial generalization)
- path: environment/docs/tgt_ids.txt
  role: comma-separated primary target id table (held-out permutations excluded)
- path: environment/docs/operator_cmds.txt
  role: cargo/pytest argv and incremental replay hook notes
- path: environment/docs/notes.md
  role: row/summary schema and mirror-pair contract visible to the agent
- path: environment/Cargo.toml
  role: workspace root
- path: environment/Cargo.lock
  role: locked dependency graph

### fix_frontier

- count: 4
- distribution: `environment/p9/y5/src/mix_r7.rs`, `environment/p9/y4/src/merge_u3.rs`, `environment/m4/k84/src/ord_g2.rs`, `environment/p9/core/src/rk1_snap.rs` (distinct roots m4, p9/y5, p9/y4, p9/core)
- naming_policy: Opaque identifiers (`mix_r7`, `merge_u3`, `ord_g2`, `rk1_snap`) on neutral parameter names; no instruction nouns on fix path
- forbidden_stems: incremental, build, shadow, artifacts, provenance, drift, recovery, replay, partial, verifier, generalization, permutations, target, closure, echo, mirror, pairs, settled, coherent, locked, sources, rebuild, manual, static, aggregate, disagree, stamps, facet, material, sync, cache, gen, stamp, debug, release, host, primary, held-out, sufficient, coherence, survives, deterministic, provenance_report, tgt_ids, operator_cmds, facet_hex, trace_digest, span_band, sync_label, drift_code, cache_rc, gen_rc, stamp_rc, rows_total, debug_echo, release_echo, host_echo, stamp_snapshot, extra_targets, rows, summary,  workspace, check, ladder, repeat
- helpers_policy: Co-resident crate roots and rhyming decoys perform credible adjacent work; frontier stays thin at four fix symbols with blob_chk snap parsing helpers declared in decoy_manifest and driver/index orchestration separate
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: regenerated JSON rows, integer closure counters, derived trace_digest, echo pair equality, held-out permutation traps, ablation incoherence, pipeline overwrite, stamp witness cross-check
- forbidden_assertion_styles: scenario-key expected tables in instruction.md; static golden report under tests/; readiness fields named `*_ok` in instruction prose tied 1:1 to fix-path grep

### task_shape

- type: adversarial_generalization
- instruction_framing: constraint-complete
- hardness_source: adversarial generalization across conflicting incremental-build evidence surfaces under destructive replay and partial recovery
- collapse_risk: Leaking canonical recovery path, replay phase ordering, or stamp-cache vs fingerprint authority collapses to a local one-crate patch

### category_profile

- challenge_family: incremental_rebuild_provenance_drift
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: locked Cargo build commands, artifact path `/app/output/provenance_report.json`, driver binary `ib`, tgt_ids.txt, row/summary schema, coherent vs incoherent conditions, mirror pairs, trace_digest formula home in main.rs header, existence of extra_targets generalization rule, operator_cmds incremental replay argv
- forbidden_instruction_leaks: Stamp-cache vs fingerprint authority split, broken replay ordering site, rk1_cross bypass site, full extra_targets row enumeration, per-target facet answers, canonical recovery sequence
- category_specific_hardness_bar: Lockfile workspace, generated facets, incremental rebuild graph, cache-visible runtime probes, and cross-format stamp witness must coordinate; one dependency bump or one manifest row cannot pass ablation and permutation suites
- category_specific_verifier_risks: clean-build-only pass, pin-one-crate fix, static JSON satisfying format without rebuild, false-green closure on partial incremental replay
- coverage_role: Adds build_dependency_toolchain adversarial_generalization coverage for incremental provenance drift using the approved overlay Cargo mold with distinct target/stamp semantics

### satisfiability_risk

- rc2_planned_name_risk: low — neutral `m4`/`p9` roots and opaque symbols (`mix_r7`, `merge_u3`, `ord_g2`, `rk1_cross`)
- gx9_contract_risk: low — tests derive verdicts from trace_digest recompute and pair equality, not per-target answer tables in instruction
- cr1_symbol_frontier_risk: low — four substantive Rust modules plus explicit flipping-point contract
- hidden_contract_risk: medium — held-out permutations in extra_targets.toml; instruction states existence and generalization rule only

### actionability_plan

- verifier_command_visible: `locked workspace build --release --locked`, `/app/target/release/ib`, `/app/docs/operator_cmds.txt` incremental replay argv
- source_fix_intent_visible: yes — repair under `/app` without naming modules
- generated_output_rule_visible: provenance_report.json path, mirror pairs, coherent predicates, regeneration requirement
- exact_formula_home: module comment above `environment/m4/k84/src/main.rs`
- schema_home: instruction public contract; optional `environment/schemas/provenance_row.schema.json` for author lint only

### waiver_plan

- waivers_expected: false
- waiver_rationale: Overlay mold keeps contracts observation-shaped with solver-visible formula homes; deterministic offline Cargo rebuilds

### reference_pattern

- justification_if_none: Construction follows approved `accepted tasks/_ref/overlay-lowerdir-stale-bind/` (`overlay-lowerdir-stale-bind.zip`) for verifier shape, flipping-point ablations, workspace+driver pipeline traps, and three-plus crate flipping-point discipline; reframed from overlay lowerdir repair to adversarial_generalization incremental provenance drift + build_dependency_toolchain with held-out extra_targets permutations. No promoted entry in `docs/reference_tasks/index.json` matches this exact profile combo; abi-rebuild-mismatch covers multi-crate regeneration discipline only.

### realism_source

- source_type: real_system
- evidence_basis: Minimized from Cargo/rustc incremental compilation stamp-cache vs dep-info fingerprint drift postmortems and overlay lowerdir stale-bind recovery incidents (approved zip)
- upstream_or_synthetic_rationale: Preserves authority split, false-green intermediate closure, cross-format emit bypass, and permutation generalization without proprietary build farm code
- minimization_preserves: Durable stamp index vs runtime fingerprint divergence, intermediate gauge closure before replay completes, JSON fast path without stamp_snapshot cross-check, held-out ordering rows in extra_targets.toml
- synthetic_exception_review: not required

### Failure topology

Visible incremental checks (locked workspace check surfaces, aggregate sync_label) can read settled while shadow-stamp replay revives stale artifact identities because three mechanisms interact: the durable stamp-cache index remains authoritative for replay ordering but the driver’s runtime fingerprint surface answers first after partial recovery; ord_g2 marks cache_rc/gen_rc true on an intermediate replay pass before twist_p9/phase ordering finishes, producing false-green closure while echo pairs disagree; and rk1_cross fast path materializes JSON facets without reconciling stamp_snapshot.json against bundled TOML/TSV seeds. Each defect is locally plausible; together they produce provenance drift that only appears after locked rebuild, driver rerun, echo-pair comparison, or held-out permutation sweeps—matching the bank-ready discovery plan without naming fix coordinates in the prompt.

### Environment shape

Rust Cargo workspace rooted at `/app` with opaque crates under `environment/m4/k84` (driver), `environment/p9/y5` (stamp fold), `environment/p9/y4` (pack merge), `environment/p9/y6` (index/twist), and `environment/p9/core` (emit/gauge/fprint). Seed data lives in `environment/data/`; operator docs in `environment/docs/`. Single-container only; fork overlay reference layout density (≥20 non-Docker environment files). Step 2b may fork `accepted tasks/_ref/overlay-lowerdir-stale-bind/environment/` then reframe docs, field names, and broken semantics; do not shrink below 20 non-Docker environment files.

### Required artifacts

Standard TB3 task tree under `tasks/incremental-build-shadow-artifacts-023/`: instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile with locked cargo/pytest/tmux/asciinema, tests/test.sh, tests/test_outputs.py (≥18 tests), solution/solve.sh + oracle.patch, full environment workspace per Initial Draft Commitments.

### Test plan

- test_r1_matrix_layout: JSON layout; primary target ids match tgt_ids.txt
- test_r2_pair_hex: mirror pairs agree on facet material and rc fields when coherent
- test_r3_rc_fields: coherent run — drift_code 0 and three rc fields 1 on all rows
- test_r4_label_text: summary sync_label reads settled when matrix coherent
- test_r5_width_max: span_band equals max abs drift_code
- test_r6_reduce_hex: summary trace_digest matches main.rs header reduction from rows
- test_r7_known_good: trace_digest matches known-good repaired emission
- test_r8_hex_lower: facet_hex sixteen lowercase hex chars
- test_r9_total_count: rows_total integer equals row vector length
- test_r10_fresh_emit: tampered hand-written JSON replaced by pipeline rebuild
- test_r11_twice_same: consecutive pipeline runs identical
- test_r12_sens_steps: mutating debug ladder data changes facet material and digest
- test_r13_ablate_fold: reverting mix_r7 fold breaks coherence
- test_r14_flip_both: reverting merge_u3 and mix_r7 together breaks pipeline
- test_r15_ablate_order: broken ord_g2 combine wiring + stock twist_p9 helper breaks closure
- test_r16_all_extras: every held-out permutation scenario in extra_targets.toml survives after fix
- test_r17_ablate_wit: reverting rk1_cross stamp witness cross-check breaks stamp_rc vs snapshot bytes
- test_r18_durable_first: durable index_r precedes runtime fprint reads after profile_a drill
- test_r19_premature: gauge_r settled label with disagreeing mirror pairs fails until replay completes
- test_r20_replay_hook: operator_cmds command sequence required for ib incremental replay success

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests (cap 0.5).

### Drafting guardrails

Instruction is constraint-complete about report schema, mirror pairs, coherence predicates, and permutation generalization—without naming `mix_r7`, `merge_u3`, `ord_g2`, `rk1_cross`, replay phase ordering, index_r vs fprint wiring, or emit bypass. Do not copy overlay “lowerdir/mount” wording verbatim. Ban instruction nouns from fix-path code symbols and test identifiers. No boolean readiness verdict fields in planned outputs. Do not ship golden provenance_report.json in repo.

### Triviality Ledger

- Hand-writing provenance_report.json fails test_r10_fresh_emit because verifier reruns cargo + ib.
- Fixing only mix_r7 without merge_u3 durable refresh fails test_r14_flip_both and pair coherence subsets.
- Fixing only ord_g2 without twist_p9 primitive contract fails test_r15_ablate_order and test_r16_all_extras.
- Copying one row from a golden fixture fails test_r7_known_good and test_r12_sens_steps.
- Trusting gauge_r settled label while mirror pairs disagree fails test_r19_premature until ord_g2 ordering and stamp authority align.
- Bumping one Cargo.toml dependency version fails ablation suites requiring semantic fixes across four roots.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle must change semantics in four roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays constraint-complete without cause-revealing “rk1_cross skips stamp witness” sentences.
- RC5/RC6: schemas and digest home in main.rs header; no boolean answer grid in instruction.
- RC7/GX3: solve.sh coordinated across four modules with substantive bodies.
- GX9/GX10: derived digests and pair equality over scenario boolean tables.
- GX4/GX5: ablation tests patch sources in-container; expectations computed in test file.
- CR1/CR2: honor symbol table and flipping-point concentration cap 0.5.

### Initial Draft Commitments

- tasks/incremental-build-shadow-artifacts-023/task.toml
- tasks/incremental-build-shadow-artifacts-023/instruction.md
- tasks/incremental-build-shadow-artifacts-023/output_contract.toml
- tasks/incremental-build-shadow-artifacts-023/construction_manifest.json
- tasks/incremental-build-shadow-artifacts-023/tests/test.sh
- tasks/incremental-build-shadow-artifacts-023/tests/test_outputs.py
- tasks/incremental-build-shadow-artifacts-023/solution/solve.sh
- tasks/incremental-build-shadow-artifacts-023/solution/oracle.patch
- tasks/incremental-build-shadow-artifacts-023/environment/Dockerfile
- tasks/incremental-build-shadow-artifacts-023/environment/Cargo.toml
- tasks/incremental-build-shadow-artifacts-023/environment/Cargo.lock
- tasks/incremental-build-shadow-artifacts-023/environment/m4/k84/Cargo.toml
- tasks/incremental-build-shadow-artifacts-023/environment/m4/k84/src/main.rs
- tasks/incremental-build-shadow-artifacts-023/environment/m4/k84/src/ord_g2.rs
- tasks/incremental-build-shadow-artifacts-023/environment/m4/k84/src/stack_mix.rs
- tasks/incremental-build-shadow-artifacts-023/environment/m4/k84/src/step_key.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y5/Cargo.toml
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y5/src/mix_r7.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y5/src/body.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y5/src/lib.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y5/src/sp_help.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y4/Cargo.toml
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y4/src/merge_u3.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y4/src/body.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y4/src/hold_buf.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y4/src/contour.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y4/src/lib.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y6/Cargo.toml
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y6/src/twist_p9.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y6/src/index_r.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y6/src/body.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y6/src/stride_scan.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/y6/src/lib.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/Cargo.toml
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/rk1_snap.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/blob_chk.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/gauge_r.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/fprint.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/kind.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/family.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/alias_stub.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/row_help.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/stack.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/apply.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/mesh.rs
- tasks/incremental-build-shadow-artifacts-023/environment/p9/core/src/lib.rs
- tasks/incremental-build-shadow-artifacts-023/environment/data/seg_tbl.toml
- tasks/incremental-build-shadow-artifacts-023/environment/data/channel.toml
- tasks/incremental-build-shadow-artifacts-023/environment/data/seed.json
- tasks/incremental-build-shadow-artifacts-023/environment/data/weights.tsv
- tasks/incremental-build-shadow-artifacts-023/environment/data/snap_blob.json
- tasks/incremental-build-shadow-artifacts-023/environment/data/perm_extra.toml
- tasks/incremental-build-shadow-artifacts-023/environment/docs/tgt_ids.txt
- tasks/incremental-build-shadow-artifacts-023/environment/docs/operator_cmds.txt
- tasks/incremental-build-shadow-artifacts-023/environment/docs/notes.md

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/p9/y5/src/mix_r7.rs
  symbol: mix_r7
  kind: function
  signature: pub fn mix_r7(step_ix: usize, family_ix: u32, prev_family: u32) -> u64
  purpose: Folds step and family tags into stamp bits for report facets.
- path: environment/p9/y4/src/merge_u3.rs
  symbol: merge_u3
  kind: function
  signature: pub fn merge_u3(state: &mut PackState, incoming: &PackState, stamp_b: u32) -> u32
  purpose: Merges incoming pack bytes into durable storage during bind steps.
- path: environment/m4/k84/src/ord_g2.rs
  symbol: ord_g2
  kind: function
  signature: pub fn ord_g2(gate_first: bool, side: impl FnMut(), gate: impl FnMut()) -> u32
  purpose: Orders side-effect callbacks during per-target combine steps under replay.
- path: environment/p9/y6/src/twist_p9.rs
  symbol: twist_p9
  kind: function
  signature: pub fn twist_p9(gate_first: bool, mut side: impl FnMut(), mut gate: impl FnMut()) -> u32
  purpose: Low-level side/gate ordering primitive used by ord_g2.
- path: environment/p9/core/src/rk1_snap.rs
  symbol: rk1_snap
  kind: function
  signature: pub fn rk1_snap(facet_hex: &str, snapshot_path: &Path) -> bool
  purpose: Cross-checks facet material against durable snap blob bytes.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/p9/y5/src/mix_r7.rs
    controls_tests: [test_r1_matrix_layout, test_r8_hex_lower, test_r7_known_good, test_r6_reduce_hex, test_r13_ablate_fold]
  - id: B
    path: environment/p9/y4/src/merge_u3.rs
    controls_tests: [test_r18_durable_first, test_r3_rc_fields]
  - id: C
    path: environment/m4/k84/src/ord_g2.rs
    controls_tests: [test_r2_pair_hex, test_r4_label_text, test_r5_width_max, test_r15_ablate_order, test_r16_all_extras, test_r20_replay_hook]
  - id: D
    path: environment/p9/core/src/rk1_snap.rs
    controls_tests: [test_r10_fresh_emit, test_r11_twice_same, test_r12_sens_steps, test_r9_total_count, test_r17_ablate_wit]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/m4/k84/src/stack_mix.rs
  kind: module
  rhymes_with: ord_g2
  non_fix_purpose: Buffers ephemeral combine events for offline benchmarks unrelated to replay combine ordering.
- path: environment/p9/y5/src/sp_help.rs
  kind: module
  rhymes_with: mix_r7
  non_fix_purpose: Applies offline fold transforms for diagnostics without participating in stamp authority.
- path: environment/p9/core/src/gauge_r.rs
  kind: helper
  rhymes_with: rk1_snap
  non_fix_purpose: Formats human-readable summaries for support tooling without stamp witness cross-check.
- path: environment/p9/core/src/probe.rs
  kind: helper
  rhymes_with: rk1_snap
  purpose: Scratch buffers for offline probe runs; called from mesh paths without authority.
- path: environment/p9/core/src/blob_chk.rs
  kind: module
  rhymes_with: rk1_snap
  non_fix_purpose: Snap blob parsing helpers co-resident with witness slow path; not a standalone flip location.
```

#### code_forbidden_tokens

```
incremental, build, shadow, artifacts, provenance, drift, recovery, replay, partial, verifier, generalization, permutations, target, closure, echo, mirror, pairs, settled, coherent, locked, sources, rebuild, manual, static, aggregate, disagree, stamps, facet, material, sync, cache, gen, stamp, debug, release, host, primary, held-out, sufficient, coherence, survives, deterministic, provenance_report, tgt_ids, operator_cmds, facet_hex, trace_digest, span_band, sync_label, drift_code, cache_rc, gen_rc, stamp_rc, rows_total, debug_echo, release_echo, host_echo, stamp_snapshot, extra_targets, rows, summary,  workspace, check, ladder, overwrite, repeat
```

### difficulty_mechanism_plan

- mechanisms: cross_file_cross_format_invariants, deceptive_but_valid_local_evidence, false_green_intermediate_states, environment_specific_cli_semantics, stateful_multi_step_dependencies, rollback_recovery_requirements
- adversarial_layers_count: 6
- fairness_guardrails: All tested formulas and primary target ids are public; deterministic drills; no timing/latency thresholds
- mechanism: cross_file_cross_format_invariants
  placement: environment/p9/core/src/rk1_snap.rs vs stamp_snapshot.json and data seeds
  why_model_misses_it: JSON shape passes without stamp witness cross-check
  fairness_guardrail: Pipeline rebuild tests (test_r10_fresh_emit, test_r17_ablate_wit)
- mechanism: deceptive_but_valid_local_evidence
  placement: environment/p9/core/src/fprint.rs runtime-visible fingerprints after partial recovery
  why_model_misses_it: Stops at settled sync_label with disagreeing echo pairs
  fairness_guardrail: Tests require pair agreement (test_r2_pair_hex)
- mechanism: false_green_intermediate_states
  placement: environment/p9/core/src/gauge_r.rs intermediate closure counters before replay completes
  why_model_misses_it: Aggregate line masks per-row drift on echoes
  fairness_guardrail: test_r19_premature and test_r15_ablate_order
- mechanism: environment_specific_cli_semantics
  placement: environment/docs/operator_cmds.txt argv consumed by ib incremental replay hook
  why_model_misses_it: Agents run generic cargo loops without documented replay argv
  fairness_guardrail: operator_cmds ships in docs
- mechanism: stateful_multi_step_dependencies
  placement: cargo rebuild then ib then JSON report under /app/output/
  why_model_misses_it: Patches without locked rebuild graph
  fairness_guardrail: operator_cmds documents commands
- mechanism: rollback_recovery_requirements
  placement: merge_u3 after partial recovery; index_r vs fprint
  why_model_misses_it: cache_rc reads 1 while gen_rc/stamp_rc diverge
  fairness_guardrail: test_r14_flip_both and test_r18_durable_first

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: derive trace_digest from m4/k84 main.rs header; run operator_cmds hook sequence; one careful human can satisfy using notes.md and bundled fixtures only
- shortcut_audit: static JSON, pytest edits, digest hardcode, hand-edited stamp snapshot, skip cargo; verifier-offline pytest/cargo baked in Dockerfile; test.sh performs no runtime network installs under allow_internet=false
- ablation_plan: revert mix_r7 only, merge_u3 only, ord_g2 only, rk1_cross only — each drops pass rate on disjoint test subsets; remove test_r16_all_extras and expect easier pass rate
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=frontier agents; Part E post-upload classification if worst-model accuracy exceeds 20%

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when all semantic pytest passes including test_r16_all_extras

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step cross-test coupling via permutations and ablations
- local_only_data: true
- sidecar_or_protocol_notes: single-container Rust workspace; fixtures under environment/data only
- long_context_token_floor: n/a
