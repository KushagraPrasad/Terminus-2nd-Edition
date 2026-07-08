### Decision
GO — Attempt 1 (validated). Seed `offline-lockfile-rehydration-017` passes idea validation on the approved **cascade-compaction** construction mold (C++ opaque multi-root workspace, `formal_rules.md` contract, trace/report driver, false-green gauge vs durable witness split) reframed to **adversarial_generalization** + **concurrency_ordering** with scheduler replay ordering mismatch, three mandated discoveries, held-out `extra_ord` permutations, and four-location flipping-point contract.

### Metadata
- version: 2
- Task name: offline-lockfile-rehydration-017
- Title: Offline lockfile rehydration
- Category: system-administration
- Task shape: adversarial_generalization
- Languages: ["cpp", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["lockfile", "scheduler", "replay", "offline", "concurrency", "rehydration"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract
The bundled offline lockfile rehydration stack under `/app/environment` must satisfy the obligations in `/app/environment/docs/formal_rules.md` after partial recovery drills and scheduler replay sequences used by the verifier.

Run `/app/bin/rh_run` as documented there to emit `/app/output/rehydration_report.json`, traces under `/app/output/run_traces/`, and updated durable indices under `/app/environment/state/`. Report row and summary shapes are defined in `formal_rules.md`. Primary unit ids are in `/app/environment/docs/unit_ids.txt`; operator replay argv patterns are in `/app/environment/docs/hook_cmds.txt` (environment-specific CLI semantics).

Mirror pairs are `bind` with `bind_echo`, `upper` with `upper_echo`, and `worker` with `worker_echo`. Coherent runs keep per-row lag at zero on every row, `sched_rc`, `lock_rc`, and `unit_rc` true on all rows, matching sixteen-digit `facet_hex` on each mirror pair, `sync_label` reading `steady`, and summary `run_digest` matching the reduction documented in the module comment above `/app/environment/pilot/entry.cpp`. The module comment defines `band_span` and `run_digest`; read it instead of hand-writing JSON.

**Adversarial generalization:** A correct fix must survive every permutation scenario encoded in `/app/environment/data/extra_ord.toml`. Instruction names the file and the generalization rule only—not individual held-out rows or per-unit facet answers.

Repair C++ and helper code under `/app/environment` so driver output and module behavior satisfy all formal properties. Rebuild `/app/bin/rh_run` from modified sources per `formal_rules.md` before validating. Static or manual JSON writes are insufficient; copying outputs without the normal driver pipeline will not pass.

### platform_files
- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "system-administration"`
- path: instruction.md
  role: natural public task prompt (constraint-complete adversarial generalization; must not name fix sites, replay phase ordering, or authority wiring)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation, permutation, and pipeline traps
- path: solution/solve.sh
  role: oracle
- path: environment/Dockerfile
  role: build definition; pre-install cmake, pytest, tmux, asciinema, and all verifier deps
- path: construction_manifest.json
  role: local authoring artifact mirroring construction manifest below

### task_files
- path: environment/q2w/queue_mux.cpp
  role: oracle frontier C — scheduler replay callback ordering under partial recovery
- path: environment/p8r/slot_mux.cpp
  role: durable slot registry vs runtime-visible slot surface after partial rehydration
- path: environment/p8r/slot_registry.cpp
  role: co-resident registry helper for slot_mux durable bytes
- path: environment/v5k/witness_mux.cpp
  role: oracle frontier A — lockfile witness fold vs runtime probe authority
- path: environment/v5k/phase_prim.cpp
  role: co-resident combine wrapper wiring queue replay callbacks
- path: environment/tools/gauge_mux.cpp
  role: false-green intermediate verifier rows before replay completes
- path: environment/tools/row_mat.cpp
  role: oracle frontier D — cross-format materialization (JSON report vs lock snapshot / TOML seeds)
- path: environment/pilot/entry.cpp
  role: published driver entry and summary reduction header
- path: environment/engine/pipeline.cpp
  role: multi-phase orchestration across replay and rehydration phases
- path: environment/engine/witness_bridge.cpp
  role: witness cross-check and summary materialization after row build
- path: environment/engine/index_registry.cpp
  role: durable lockfile index authority persistence
- path: environment/docs/formal_rules.md
  role: formal properties, schema references, build/replay commands
- path: environment/docs/unit_ids.txt
  role: primary unit id table (held-out permutations excluded from this list)
- path: environment/docs/hook_cmds.txt
  role: operator replay argv patterns for rh_run hooks
- path: environment/data/extra_ord.toml
  role: held-out permutation scenario table (adversarial generalization)
- path: environment/data/lock_snapshot.json
  role: lock witness bytes cross-checked by slow path
- path: environment/schemas/report_row.schema.json
  role: row shape for emitted report
- path: environment/schemas/trace_run.schema.json
  role: trace ledger shape

### fix_frontier
- count: 4
- distribution: `environment/v5k/witness_mux.cpp`, `environment/p8r/slot_mux.cpp`, `environment/q2w/queue_mux.cpp`, `environment/tools/row_mat.cpp` (distinct roots q2w, p8r, v5k, tools)
- naming_policy: Opaque identifiers (`fn_q2`, `fn_p8`, `fn_v5`, `fn_e4`) on neutral parameter names; no instruction nouns on fix path
- forbidden_stems: offline, lockfile, rehydration, scheduler, replay, ordering, mismatch, authority, recovery, partial, green, intermediate, verifier, invariant, regeneration, generalization, permutations, matrix, units, closure, echoes, mirror, pairs, steady, coherent, locked, sources, rebuild, manual, static, argv, probes, aggregate, disagree, stamps, facet, material, sync, drift, bind, upper, worker, primary, held-out, sufficient, coherence, survives, deterministic, rehydration_report, unit_ids, hook_cmds, build_hints, facet_hex, run_digest, band_span, sync_label, drift_code, sched_rc, lock_rc, unit_rc, rows_total, bind_echo, upper_echo, worker_echo, lock_snapshot, extra_ord, cross-format, table, layout, agreement, span, count, stable, mutate, ablation, perms, surface, contract, anchor, trap, flags, zero, line, band, held, overwrite, repeat, ladder, fold, dual, order, emit
- helpers_policy: Decoys in q2w, v5k, tools perform credible adjacent work; frontier stays thin at four symbols with driver/registry orchestration separate
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 0
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: regenerated JSON rows, derived run_digest, echo pair equality, held-out permutation traps, ablation incoherence, pipeline overwrite, trace-derived counters
- forbidden_assertion_styles: scenario-key expected tables in instruction.md; static golden report; readiness fields named `*_ok` in instruction prose tied 1:1 to fix-path grep

### task_shape
- type: adversarial_generalization
- instruction_framing: constraint-complete
- hardness_source: adversarial generalization across conflicting evidence surfaces under scheduler replay reordering
- collapse_risk: Leaking canonical recovery path, replay phase ordering, or index-vs-slot authority collapses to one-module patch

### category_profile
- challenge_family: scheduler_replay_lockfile_mismatch
- profile_name: concurrency_ordering
- allowed_instruction_disclosures: Concurrent scheduler replay operations, public ordering invariant via report predicates and formal_rules.md, hook_cmds.txt, locked CMake build, durable rehydration_report outcomes, mirror pairs, run_digest formula home, existence of extra_ord generalization rule
- forbidden_instruction_leaks: Queue/lock locations, exact interleaving, patch functions, index vs slot authority split, row_mat bypass site, full extra_ord row enumeration, per-unit facet answers, canonical recovery sequence
- category_specific_hardness_bar: Two or more schedulers/queues plus persistence (lockfile index, replay cursor, slot registry) must coordinate; one lock, one sort, or one sleep must not suffice
- category_specific_verifier_risks: Flaky sleeps, single trace, tests that pass by serializing everything, false-green partial replay
- coverage_role: Adds concurrency_ordering under system-administration for offline lockfile rehydration with scheduler replay mismatch; distinct from cascade-compaction state_recovery formal_reasoning while reusing its C++ mold

### satisfiability_risk
- rc2_planned_name_risk: low — opaque package roots (q2w, p8r, v5k) and neutral test prefixes
- gx9_contract_risk: low — tests derive verdicts from run_digest recompute and pair equality
- cr1_symbol_frontier_risk: low — four substantive C++ modules plus explicit flipping-point contract
- hidden_contract_risk: medium — held-out permutations in extra_ord.toml; instruction states existence and generalization rule only

### actionability_plan
- verifier_command_visible: CMake build from `/app/environment` and `/app/bin/rh_run`; hook_cmds.txt; formal_rules.md
- source_fix_intent_visible: yes — repair under /app/environment without naming modules
- generated_output_rule_visible: `/app/output/rehydration_report.json` path and field names; mirror pair rules
- exact_formula_home: module comment above `environment/pilot/entry.cpp`
- schema_home: `environment/schemas/report_row.schema.json` plus formal_rules.md

### waiver_plan
- waivers_expected: false
- waiver_rationale: Cascade mold keeps contracts observation-shaped with solver-visible formal homes; deterministic local drills

### reference_pattern
- justification_if_none: Construction follows approved `accepted tasks/cascade-compaction.zip`: C++ opaque multi-root layout (k7w/m9p/n4q → q2w/p8r/v5k), `formal_rules.md` durability contract, driver binary (`cc_run` → `rh_run`), false-green `gauge_mux` vs authoritative `witness_mux`, trace/report append semantics, and three-plus module flipping-point discipline. Reframed from formal_reasoning namespace compaction to adversarial_generalization offline lockfile rehydration + concurrency_ordering with held-out `extra_ord` permutations. No promoted `docs/reference_tasks/index.json` entry matches this combo.

### realism_source
- source_type: real_system
- evidence_basis: Minimized from offline package-manager lockfile rehydration and scheduler replay postmortems (BuildKit/Cargo-offline resolver patterns) plus cascade-compaction conflicting-observability mold
- upstream_or_synthetic_rationale: Preserves authority split, false-green closure, cross-format emit bypass, and permutation generalization without proprietary cluster code
- minimization_preserves: Durable index vs runtime slot divergence, intermediate verifier green before replay completes, JSON fast path without lock witness cross-check, held-out ordering rows in extra_ord.toml
- synthetic_exception_review: Not required

### Failure topology
After partial recovery, runtime unit probes and intermediate verifier rows can read steady while durable lockfile index material and replay ordering disagree. Scheduler replay can mark closure counters true on an intermediate pass before phase ordering finishes, masking corruption that echo mirror pairs still expose. A JSON materialization path can satisfy superficial row shape while skipping cross-checks against `lock_snapshot.json` and bundled TOML/TSV seeds. Hardness requires reconciling queue ordering, index registry, witness folding, and emit cross-format rules under deterministic replay—without the instruction naming which subsystem mis-orders replay or which authority wins.

### Environment shape
Split C++ modules across q2w (queue mux), p8r (slot mux), v5k (witness fold), tools (gauge and row materialization), pilot entrypoint, engine pipeline and index registry, docs (formal contract), schemas, fixtures (drill profiles), and data (extra_ord, lock snapshot, ladder/channel seeds). Single-container only. Fork file count and verifier trap patterns from cascade-compaction.zip; reframe docs and scenario tables for lockfile rehydration semantics.

### Required artifacts
instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile (tmux + asciinema pinned), tests/test.sh, tests/test_outputs.py, solution/solve.sh, and ≥20 C++/text/schema assets under environment/ per Initial Draft Commitments.

### Test plan
- test_p1_shape_rows: report shape; primary unit ids match unit_ids.txt
- test_p2_pair_hex: mirror pairs agree on facet material and rc fields when coherent
- test_p3_rc_fields: coherent run — lag zero and three rc fields true on all rows
- test_p4_label_text: summary label text steady when matrix coherent
- test_p5_width_max: width field equals max abs drift code magnitude
- test_p6_reduce_hex: summary fingerprint matches pilot header reduction from rows
- test_p7_known_good: fingerprint matches known-good repaired emission
- test_p8_hex_lower: facet material sixteen lowercase hex chars
- test_p9_len_rows: total row count integer equals row vector length
- test_p10_rerun_pipe: tampered hand-written JSON replaced by pipeline rerun
- test_p11_twice_same: consecutive pipeline runs identical
- test_p12_sens_steps: mutating step ladder data changes facet material and fingerprint
- test_p13_flip_v5: reverting fn_v5 witness body breaks coherence
- test_p14_flip_both: reverting fn_p8 and fn_v5 together breaks pipeline
- test_p15_flip_q2: broken fn_q2 combine wiring + stock decoy helper breaks closure
- test_p16_all_extras: every held-out permutation scenario in data file survives after fix
- test_p17_flip_e4: reverting fn_e4 witness cross-check breaks lock rc vs witness bytes
- test_p18_reg_first: durable index_registry precedes runtime slot reads after profile_a drill
- test_p19_premature: gauge_mux steady label with disagreeing mirror pairs fails until replay completes
- test_p20_cli_hooks: hook_cmds argv sequence required for rh_run hook success

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests (cap 0.5).

### Drafting guardrails
Instruction is constraint-complete about report schema, mirror pairs, coherence predicates, and permutation generalization—without naming `fn_q2`, `fn_p8`, `fn_v5`, `fn_e4`, replay phase ordering, index-vs-slot wiring, or emit bypass. Do not copy cascade-compaction “namespace compaction” wording verbatim. Ban instruction nouns from fix-path code symbols and test identifiers. No boolean readiness verdict fields in planned outputs.

### Triviality Ledger
- Hand-writing rehydration_report.json fails test_p10_rerun_pipe because verifier reruns cmake + rh_run.
- Fixing only fn_v5 without fn_p8 durable refresh fails test_p14_flip_both and pair coherence subsets.
- Fixing only fn_q2 without phase primitive contract fails test_p15_flip_q2 and test_p16_all_extras.
- Copying one row from a golden fixture fails test_p7_known_good and test_p12_sens_steps.
- Trusting gauge_mux steady label while mirror pairs disagree fails test_p19_premature until queue ordering and witness authority align.

### Per-gate Pitfall Inventory
- RC1/GX2: oracle must change semantics in four roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays constraint-complete without cause-revealing “the emit path skips witness” sentences.
- RC5/RC6: schemas and digest home in pilot header; no boolean answer grid in instruction.
- RC7/GX3: solve.sh coordinated across four modules with substantive bodies.
- GX9/GX10: derived digests and pair equality over scenario boolean tables.
- GX4/GX5: ablation tests patch sources in-container; expectations computed in test file.
- CR1/CR2: honor symbol table and flipping-point concentration cap 0.5.

### Initial Draft Commitments
- tasks/offline-lockfile-rehydration-017/task.toml
- tasks/offline-lockfile-rehydration-017/instruction.md
- tasks/offline-lockfile-rehydration-017/output_contract.toml
- tasks/offline-lockfile-rehydration-017/construction_manifest.json
- tasks/offline-lockfile-rehydration-017/tests/test.sh
- tasks/offline-lockfile-rehydration-017/tests/test_outputs.py
- tasks/offline-lockfile-rehydration-017/solution/solve.sh
- tasks/offline-lockfile-rehydration-017/environment/Dockerfile
- tasks/offline-lockfile-rehydration-017/environment/CMakeLists.txt
- tasks/offline-lockfile-rehydration-017/environment/q2w/queue_mux.cpp
- tasks/offline-lockfile-rehydration-017/environment/q2w/queue_buffer.cpp
- tasks/offline-lockfile-rehydration-017/environment/p8r/slot_mux.cpp
- tasks/offline-lockfile-rehydration-017/environment/p8r/slot_registry.cpp
- tasks/offline-lockfile-rehydration-017/environment/v5k/witness_mux.cpp
- tasks/offline-lockfile-rehydration-017/environment/v5k/fold_apply.cpp
- tasks/offline-lockfile-rehydration-017/environment/v5k/phase_prim.cpp
- tasks/offline-lockfile-rehydration-017/environment/tools/gauge_mux.cpp
- tasks/offline-lockfile-rehydration-017/environment/tools/row_mat.cpp
- tasks/offline-lockfile-rehydration-017/environment/tools/summary_mux.hpp
- tasks/offline-lockfile-rehydration-017/environment/pilot/entry.cpp
- tasks/offline-lockfile-rehydration-017/environment/engine/pipeline.cpp
- tasks/offline-lockfile-rehydration-017/environment/engine/index_registry.cpp
- tasks/offline-lockfile-rehydration-017/environment/engine/types.hpp
- tasks/offline-lockfile-rehydration-017/environment/util/digest.cpp
- tasks/offline-lockfile-rehydration-017/environment/util/json_codec.cpp
- tasks/offline-lockfile-rehydration-017/environment/docs/formal_rules.md
- tasks/offline-lockfile-rehydration-017/environment/docs/unit_ids.txt
- tasks/offline-lockfile-rehydration-017/environment/docs/hook_cmds.txt
- tasks/offline-lockfile-rehydration-017/environment/data/extra_ord.toml
- tasks/offline-lockfile-rehydration-017/environment/data/lock_snapshot.json
- tasks/offline-lockfile-rehydration-017/environment/data/ladder.toml
- tasks/offline-lockfile-rehydration-017/environment/data/channel.toml
- tasks/offline-lockfile-rehydration-017/environment/fixtures/drill_profiles/profile_a.json
- tasks/offline-lockfile-rehydration-017/environment/fixtures/drill_profiles/profile_b.json
- tasks/offline-lockfile-rehydration-017/environment/schemas/report_row.schema.json
- tasks/offline-lockfile-rehydration-017/environment/schemas/trace_run.schema.json
- tasks/offline-lockfile-rehydration-017/environment/state/README
- tasks/offline-lockfile-rehydration-017/environment/config/defaults.env

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```
- path: environment/v5k/witness_mux.cpp
  symbol: fn_v5
  kind: function
  signature: fn_v5(step_ix, family_ix, prev_family)
  purpose: Folds step and family tags into facet material for report rows.
- path: environment/p8r/slot_mux.cpp
  symbol: fn_p8
  kind: function
  signature: fn_p8(ctx, stamp_a, stamp_b)
  purpose: Merges durable slot bytes into active registry during bind steps.
- path: environment/q2w/queue_mux.cpp
  symbol: fn_q2
  kind: function
  signature: fn_q2(gate_first, side_cb, gate_cb)
  purpose: Orders side-effect callbacks during per-unit combine steps under replay.
- path: environment/tools/row_mat.cpp
  symbol: fn_e4
  kind: function
  signature: fn_e4(rows, seeds, witness)
  purpose: Materializes report rows from unit state, seeds, and lock witness bundle.
```

#### flipping_point_contract
```
locations:
  - id: A
    path: environment/v5k/witness_mux.cpp
    controls_tests: [test_p1_shape_rows, test_p8_hex_lower, test_p7_known_good, test_p6_reduce_hex, test_p13_flip_v5]
  - id: B
    path: environment/p8r/slot_mux.cpp
    controls_tests: [test_p18_reg_first, test_p3_rc_fields]
  - id: C
    path: environment/q2w/queue_mux.cpp
    controls_tests: [test_p2_pair_hex, test_p4_label_text, test_p5_width_max, test_p15_flip_q2, test_p16_all_extras, test_p20_cli_hooks]
  - id: D
    path: environment/tools/row_mat.cpp
    controls_tests: [test_p10_rerun_pipe, test_p11_twice_same, test_p12_sens_steps, test_p9_len_rows, test_p17_flip_e4]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest
```
- path: environment/q2w/queue_buffer.cpp
  kind: module
  rhymes_with: fn_q2
  non_fix_purpose: Buffers ephemeral queue events for offline benchmarks unrelated to replay combine ordering.
- path: environment/v5k/fold_apply.cpp
  kind: module
  rhymes_with: fn_v5
  non_fix_purpose: Applies offline fold transforms for diagnostics without participating in witness authority.
- path: environment/tools/summary_mux.hpp
  kind: helper
  rhymes_with: fn_e4
  non_fix_purpose: Formats human-readable summaries for support tooling without lock witness cross-check.
```

#### code_forbidden_tokens
```
offline, lockfile, rehydration, scheduler, replay, ordering, mismatch, authority, recovery, partial, green, intermediate, verifier, invariant, regeneration, generalization, permutations, matrix, units, closure, echoes, mirror, pairs, steady, coherent, locked, sources, rebuild, manual, static, argv, probes, aggregate, disagree, stamps, facet, material, sync, drift, bind, upper, worker, primary, held-out, sufficient, coherence, survives, deterministic, rehydration_report, unit_ids, hook_cmds, build_hints, facet_hex, run_digest, band_span, sync_label, drift_code, sched_rc, lock_rc, unit_rc, rows_total, bind_echo, upper_echo, worker_echo, lock_snapshot, extra_ord, cross-format, table, layout, agreement, span, count, stable, mutate, ablation, perms, surface, contract, anchor, trap, flags, zero, line, band, held, overwrite, repeat, ladder, fold, dual, order, emit
```

### difficulty_mechanism_plan
- mechanisms: environment_specific_cli_semantics, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, stateful_multi_step_dependencies, false_green_intermediate_states, rollback_recovery_requirements
- adversarial_layers_count: 6
- fairness_guardrails: All tested formulas and primary unit ids are public; deterministic drills; no timing/latency thresholds
- mechanism: environment_specific_cli_semantics
  placement: environment/docs/hook_cmds.txt argv consumed by rh_run replay hook
  why_model_misses_it: Agents run generic cmake loops without documented replay argv
  fairness_guardrail: hook_cmds ships in docs
- mechanism: deceptive_but_valid_local_evidence
  placement: environment/tools/gauge_mux.cpp intermediate closure counters
  why_model_misses_it: Stops at steady sync_label with disagreeing echo pairs
  fairness_guardrail: Tests require pair agreement (test_p2_pair_hex)
- mechanism: cross_file_cross_format_invariants
  placement: environment/tools/row_mat.cpp vs lock_snapshot.json and data seeds
  why_model_misses_it: JSON shape passes without witness cross-check
  fairness_guardrail: Pipeline rebuild tests (test_p10_rerun_pipe, test_p17_flip_e4)
- mechanism: stateful_multi_step_dependencies
  placement: cmake rebuild then rh_run then JSON report under /app/output/
  why_model_misses_it: Patches without locked rebuild graph
  fairness_guardrail: formal_rules.md documents commands
- mechanism: false_green_intermediate_states
  placement: closure counters before replay completes (fn_q2 / phase_prim)
  why_model_misses_it: Aggregate line masks per-row drift on echoes
  fairness_guardrail: test_p19_premature and test_p15_flip_q2
- mechanism: rollback_recovery_requirements
  placement: fn_p8 after partial rehydration; index_registry vs slot_mux
  why_model_misses_it: unit_rc reads true while lock_rc/sched_rc diverge
  fairness_guardrail: test_p14_flip_both and test_p18_reg_first

### calibration_plan
- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: derive run_digest from pilot/entry.cpp header; run hook_cmds sequence; one careful human can satisfy using formal_rules.md and bundled fixtures only
- shortcut_audit: static JSON, pytest edits, digest hardcode, hand-edited lock snapshot, skip cmake; verifier-offline pytest/cmake baked in Dockerfile; test.sh performs no runtime network installs under allow_internet=false
- ablation_plan: revert fn_v5 only, fn_p8 only, fn_q2 only, fn_e4 only — each drops pass rate on disjoint test subsets; remove test_p16_all_extras and expect easier pass rate
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=frontier agents; Part E post-upload classification if worst-model accuracy exceeds 20%

### verifier_scoring_plan
- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when all semantic pytest passes including test_p16_all_extras

### subtype_milestone_plan
- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step cross-test coupling via permutations and ablations
- local_only_data: true
- sidecar_or_protocol_notes: single-container C++ workspace; fixtures under environment/data only
- long_context_token_floor: n/a
