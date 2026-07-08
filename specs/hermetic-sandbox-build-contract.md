### Decision

GO — Attempt 2. Renamed test identifiers that collided with instruction nouns (ladder, extras, argv); retained four-root hermetic sandbox constrained-build topology with inode-witness allowlist, sysroot bind ordering, journal-keyed registry stub, and post-commit capture attest bridge.

### Metadata

- version: 2
- Task name: hermetic-sandbox-build-contract
- Title: Hermetic sandbox contract
- Category: software-engineering
- Task shape: constrained_build
- Languages: ["python", "bash", "cpp"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["hermetic-build", "sandbox-wrapper", "audit-replay", "offline-registry", "sysroot-isolation", "rollback-recovery", "cross-format-attest"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, per-drill answer tables, or narrative causal chains that name fix coordinates.

### Public contract

Complete the offline `/app/bin/hs_run` phased driver for the workspace under `/app/environment` so production audit replay succeeds. Public obligations live in `/app/environment/docs/formal_rules.md`.

The hermetic sandbox build contract requires five coupled outcomes:

1. **Input gate** — only paths admitted by the allowlist manifest plus the declared sysroot enter the compile namespace.
2. **Header isolation** — compiler include search must not observe host headers outside the declared sysroot.
3. **Offline fetch** — dependency metadata comes from pinned registry fixture responses only; live network access is unsupported.
4. **Capture gate** — the output bundle contains only artifact ids declared in the output manifest, with deterministic digests suitable for audit replay.
5. **Attest bridge** — each audit row ties JSON facet material to ELF section hashes from captured binaries under the demo_r9 build target.

Run the locked build workflow and driver as documented to emit `/app/output/audit_report.json`, trace files under `/app/output/run_traces/`, and refreshed durable bytes under `/app/environment/k9d/`. Row and summary shapes are defined in `formal_rules.md`. Primary unit ids are in `/app/environment/docs/tgt_ids.txt`; operator argv patterns are in `/app/environment/docs/operator_cmds.txt` (environment-specific CLI semantics for phased replay hooks).

Mirror pairs bind `bind` with `bind_echo`, `upper` with `upper_echo`, and `worker` with `worker_echo`. Coherent runs keep per-row lag at zero on every row, `sched_rc`, `lock_rc`, and `unit_rc` at `1` on all rows, matching sixteen-digit `facet_hex` on each mirror pair, `sync_label` reading `steady`, and summary `run_digest` matching the reduction documented in the module comment above `/app/environment/pilot/entry.py`. The module comment defines `band_span` and `run_digest`; read it instead of hand-writing JSON.

**Rollback recovery:** After partial phase failure drills encoded in `/app/environment/data/perm_extra.toml`, a correct implementation must converge to the same terminal audit outcome when the driver is rerun from durable state. Instruction names the drill file and convergence rule only—not individual held-out drill rows or per-unit facet answers.

Complete Python and helper code under `/app/environment` so driver output and module behavior satisfy all contract properties. Rebuild `/app/bin/hs_run` from modified sources per `formal_rules.md` before validating. Static or manual JSON writes are insufficient; copying outputs without the normal driver pipeline will not pass.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "software-engineering"`
- path: instruction.md
  role: natural public design-brief prompt (mirrors Public contract above)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation, drill permutation, and pipeline traps
- path: solution/solve.sh
  role: oracle applying coordinated multi-module fix
- path: environment/Dockerfile
  role: build definition; pre-install cmake, python3, pytest, tmux, asciinema, and locked deps
- path: construction_manifest.json
  role: local authoring artifact mirroring Construction manifest below

### task_files

- path: environment/r7k/filter_mux.py
  role: oracle frontier A — inode witness allowlist fold
- path: environment/r7k/scan_mux.py
  role: witness tuple scanner feeding fn_r7
- path: environment/r7k/path_help.py
  role: decoy path normalizer (non-fix)
- path: environment/n3p/root_mux.py
  role: oracle frontier B — sysroot overlay bind ordering
- path: environment/n3p/tbl_l4.py
  role: sysroot bind ladder data loader
- path: environment/n3p/mount_help.py
  role: decoy mount listing helper (non-fix)
- path: environment/w8q/stub_mux.py
  role: oracle frontier C — offline registry shard selection
- path: environment/w8q/idx_mux.py
  role: fixture shard index table
- path: environment/w8q/cache_help.py
  role: decoy fixture mtime cache helper (non-fix)
- path: environment/t2m/cap_mux.py
  role: oracle frontier D — post-commit capture and ELF attest bridge
- path: environment/t2m/ring_mux.py
  role: undeclared artifact purge ring buffer
- path: environment/t2m/hash_help.py
  role: decoy stdout hash helper (non-fix)
- path: environment/pilot/entry.py
  role: hs_run driver entry and summary reduction header
- path: environment/engine/orch_v3.py
  role: multi-phase orchestration across input/isolate/fetch/capture/attest
- path: environment/engine/seg_mux.py
  role: durable phase cursor and rollback segments
- path: environment/engine/ready_g8.py
  role: false-green status subcommand surface
- path: environment/demo_r9/CMakeLists.txt
  role: small offline C++ sample under hermetic wrap
- path: environment/demo_r9/src/main.cpp
  role: sample compile target producing attestable ELF
- path: environment/docs/formal_rules.md
  role: formal properties, schema references, build/replay commands
- path: environment/docs/tgt_ids.txt
  role: primary unit id table (held-out drill permutations excluded)
- path: environment/docs/operator_cmds.txt
  role: operator argv patterns for hs_run hooks
- path: environment/data/gate_tbl.json
  role: inode witness allowlist manifest
- path: environment/data/cap_tbl.json
  role: declared capture artifact ids
- path: environment/data/perm_extra.toml
  role: rollback drill permutation table
- path: environment/data/variant_tbl.toml
  role: offline platform variant matrix
- path: environment/data/fix_stash/index_a.json
  role: pinned registry fixture shard A
- path: environment/data/fix_stash/index_b.json
  role: pinned registry fixture shard B
- path: environment/schemas/row_v3.schema.json
  role: row shape for audit_report.json
- path: environment/k9d/seg_v/.gitkeep
  role: durable segment placeholder

### fix_frontier

- count: 4
- distribution: `environment/r7k/filter_mux.py`, `environment/n3p/root_mux.py`, `environment/w8q/stub_mux.py`, `environment/t2m/cap_mux.py` (distinct roots r7k, n3p, w8q, t2m)
- naming_policy: Opaque identifiers (`fn_r7`, `fn_n3`, `fn_w8`, `fn_t2`) on neutral parameter names; no instruction nouns on fix path
- forbidden_stems: hermetic, sandbox, allowlist, sysroot, registry, capture, audit, manifest, rollback, journal, fixture, overlay, witness, shard, purge, attest, elf, hs_run, contract_rules, audit_report, run_traces, facet_hex, run_digest, sync_label, hook_cmds, unit_ids, bind, bind_echo, upper, upper_echo, worker, worker_echo, sched_rc, lock_rc, unit_rc, drill, profiles, platform, health, gauge, convergence, deterministic, digests, mirror, pairs, steady, coherent, pipeline, regeneration, manual, static, sources, rebuild, locked, workflow, trace, durable, state, operator, hook, reduction, module, comment, rows, summary, primary, documented, emit, refreshed, shapes, defined, properties, validating, insufficient, writes, complete, wrapper, production, reproducible, supply, chain, sample, proj, cmake, compiler, include, paths, tarball, declared, terminal, status, subcommand, fetch, isolation, namespace, provenance, matrix, targets, argv, lag, facet, sync, sched, lock, unit, sixteen, hexadecimal, incoherent, cross, format, runtime, reads, disagreeing, until, sequence, required, success, extras, ladder, known, good, tampered, hand, written, consecutive, mutating, step, reverting, stock, decoy, helper, breaks, closure, held, precedes, matching, digit, lowercase, integer, vector, length, fingerprint, anchor, mut, perms, seq, vecs, dur, seg, rerun, pipe, twice, same, sens, flip, both, cap, reg, first, premature, cli, reduce, hex, lower, len, shape, pair, label, text, width, max, rc, fields, anchor, all, flip, dur, seg, reg, first, premature, cli, seq
- helpers_policy: Decoys in r7k, n3p, w8q, t2m perform credible adjacent diagnostics; frontier stays thin at four symbols with pipeline/journal orchestration separate
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 12
- preferred_assertion_styles: regenerated JSON rows, integer rc counters, derived run_digest, echo pair equality, drill permutation traps, ablation incoherence, pipeline overwrite, ELF section cross-check
- forbidden_assertion_styles: scenario-key expected tables in instruction.md; static golden audit_report under tests/; readiness fields named `*_ok` in instruction prose tied 1:1 to fix-path grep

### task_shape

- type: constrained_build
- instruction_framing: design-brief
- hardness_source: design search across coupled hermetic sandbox phases with rollback recovery
- collapse_risk: blank-canvas build with no binding cross-component constraints

### category_profile

- challenge_family: hermetic build sandbox
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: build/test commands, artifact identities, platform matrix, reproducibility outputs, phased driver obligations, audit_report schema, mirror pairs, operator_cmds argv, formal_rules formal properties, perm_extra existence and convergence rule
- forbidden_instruction_leaks: inode-vs-path rule, bind order recipe, stub shard key, journal replay sequence, purge timing, patch functions, per-drill facet answers, canonical recovery sequence
- category_specific_hardness_bar: Lockfiles/fixtures, generated capture manifest, build graph phases, platform matrix, and journal/cache invalidation must coordinate; one version bump or one manifest row cannot pass ablation and drill suites
- category_specific_verifier_risks: pin-one-dep fix, network reliance, clean-build-only tests, false-green health/status without durable journal convergence
- coverage_role: Strengthens build_dependency_toolchain coverage via hermetic sandbox build contract constrained-build topology

### difficulty_mechanism_plan

- mechanisms: stateful_multi_step_dependencies, deceptive_but_valid_local_evidence, false_green_intermediate_states, cross_file_cross_format_invariants, rollback_recovery_requirements
- adversarial_layers_count: 5
- fairness_guardrails: Public contract states every externally tested phase outcome, schema, and command without naming fix-path symbols or construction recipes; deceptive layers remain discoverable from traces, journal bytes, and ablation flips
- mechanism: stateful_multi_step_dependencies
  placement: environment/engine/orch_v3.py multi-phase CLI workflow across input/isolate/fetch/capture/attest
  why_model_misses_it: models stop after first green status subcommand without finishing attest and convergence phases
  fairness_guardrail: formal_rules.md lists phase outcomes; operator_cmds documents required argv sequence; each phase appends trace rows
- mechanism: deceptive_but_valid_local_evidence
  placement: environment/engine/ready_g8.py ready subcommand surface
  why_model_misses_it: models trust misleading local ready/steady labels while durable journal and mirror pairs still disagree
  fairness_guardrail: verifier cross-checks health output against journal segments and echo pair facet_hex equality
- mechanism: false_green_intermediate_states
  placement: environment/t2m/ring_mux.py intermediate manifest rows before journal commit
  why_model_misses_it: models declare capture done when manifest shape looks complete but ELF attest cross-check still fails
  fairness_guardrail: test_p19_premature requires terminal convergence with matching run_digest after full pipeline
- mechanism: cross_file_cross_format_invariants
  placement: environment/t2m/cap_mux.py JSON rows tied to demo_r9 ELF section hashes and registry fixture bytes
  why_model_misses_it: models fix JSON emitters without reconciling binary section digests and fixture shard metadata
  fairness_guardrail: instruction names cross-format attest obligation; tests recompute digests from visible formula home
- mechanism: rollback_recovery_requirements
  placement: environment/engine/seg_mux.py rollback drills in perm_extra.toml
  why_model_misses_it: models skip journal cursor reconstruction after partial phase failure, passing happy path only
  fairness_guardrail: drill file named in instruction; verifier reruns rollback sequences deterministically offline

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert build engineer reproduces incoherent audit_report under stock scaffold, applies coordinated four-module fix, reruns hs_run offline to steady convergence
- shortcut_audit: block hardcoded audit_report.json, test edits, stale-doc-only changes, wrapper-only health subcommand patches, and single-manifest-row tweaks
- ablation_plan: remove deceptive health layer, then journal replay, then stub shard selection, then bind ordering—each ablation should drop pass rate materially
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=aligns with Part E Hard/Medium/Easy thresholds on worst-model accuracy; verifier-offline: pytest and cmake baked in Dockerfile with tests/test.sh using no runtime apt/pip/curl; post-upload difficulty classification runs only after successful agent+verifier cycles per PLATFORM_AUTO_EVAL.md

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward 1 only when all weighted metrics pass; any ablation flip or pipeline trap failure yields 0

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: single-container local verifier only; offline registry fixtures and drill profiles pre-bundled under environment/data/

### satisfiability_risk

- rc2_planned_name_risk: low — opaque r7k/n3p/w8q/t2m roots and fn_* symbols committed in construction manifest
- gx9_contract_risk: low — tests derive verdicts from run_digest recompute, pair equality, and ELF cross-checks, not per-row answer tables in instruction
- cr1_symbol_frontier_risk: low — four substantive Python modules plus explicit flipping-point contract
- hidden_contract_risk: medium — cross-artifact invariants (journal vs capture vs ELF) live in behavior; formal_rules.md names outcomes not wiring

### actionability_plan

- verifier_command_visible: CMake build from /app/environment, /app/bin/hs_run driver, operator_cmds.txt argv sequences
- source_fix_intent_visible: yes — complete wrapper under /app/environment without naming modules
- generated_output_rule_visible: /app/output/audit_report.json path, mirror pair rules, regeneration requirement, run_traces directory
- exact_formula_home: module comment above environment/pilot/entry.py for run_digest and band_span reduction
- schema_home: environment/schemas/row_v3.schema.json plus formal_rules.md

### waiver_plan

- waivers_expected: false
- waiver_rationale: hardness from coupled phased behavior and cross-format invariants, not harness brittleness; offline fixtures and deterministic replays avoid waiver pressure

### reference_pattern

- reference_task_id:
- justification_if_none: No promoted reference in docs/reference_tasks/index.json matches hermetic sandbox phased-wrapper constrained_build with Python multi-root flipping-point discipline; closest abi-rebuild-mismatch covers multi-crate regeneration not offline registry stub plus capture attest bridge

### realism_source

- source_type: real_system
- evidence_basis: open-source issue
- upstream_or_synthetic_rationale: Minimized from Bazel/BuildKit hermetic action sandbox and reproducible-build audit replay postmortems where allowlisted inputs, sysroot isolation, offline registry mirrors, and capture manifests must align for deterministic digests
- minimization_preserves: Causal coupling across input allowlist, header isolation, offline fetch stub, capture manifest, journal rollback, and JSON-to-ELF attest cross-check
- synthetic_exception_review: not required

### Failure topology

The stock phased driver can emit well-shaped audit rows while durable journal segments, registry fixture bytes, and ELF section material disagree. Health/status subcommands may read steady before rollback drills finish replaying phase cursors. A JSON materialization path can satisfy superficial row shape while skipping cross-checks against captured binaries and pinned fixture shards. Hardness requires reconciling input witness matching, sysroot bind order, offline stub shard selection, post-commit capture purge, and journal replay under platform matrix variants—without the instruction naming which subsystem mis-orders phases or which authority wins.

### Environment shape

Split Python modules across r7k (input filter), n3p (sysroot isolation), w8q (offline registry stub), t2m (capture/attest), pilot entrypoint, engine orch_v3/seg_mux/ready_g8, demo_r9 C++ target, docs (formal_rules, operator_cmds), schemas, fixtures (gate_tbl, cap_tbl, fix_stash shards, perm_extra, variant_tbl), and durable k9d segments. Single-container only. Fork verifier trap patterns from approved multi-root molds; reframe semantics for hermetic sandbox audit replay.

### Required artifacts

instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile (tmux + asciinema pinned), tests/test.sh, tests/test_outputs.py, solution/solve.sh, and ≥20 environment assets per Initial Draft Commitments.

### Test plan

- test_p1_shape_vecs: audit_report row vector shape; primary unit ids match tgt_ids.txt
- test_p2_pair_hex: mirror pairs agree on facet material and rc fields when coherent
- test_p3_rc_fields: coherent run — lag zero and three rc fields at 1 on all rows
- test_p4_label_text: summary label text steady when matrix coherent
- test_p5_width_max: width field equals max abs drift code magnitude
- test_p6_reduce_hex: summary fingerprint matches pilot header reduction from rows
- test_p7_anchor_hex: fingerprint matches known-good repaired emission
- test_p8_hex_lower: facet material sixteen lowercase hex chars
- test_p9_len_vecs: total row count integer equals row vector length
- test_p10_rerun_flow: tampered hand-written JSON replaced by pipeline rerun
- test_p11_twice_same: consecutive pipeline runs identical
- test_p12_sens_mut: mutating allowlist witness data changes facet material and fingerprint
- test_p13_flip_w8: reverting fn_w8 stub body breaks coherence
- test_p14_flip_both: reverting fn_n3 and fn_w8 together breaks pipeline
- test_p15_flip_t2: reverting fn_t2 capture body breaks ELF cross-check
- test_p16_all_perms: every drill permutation scenario in perm_extra.toml survives after fix
- test_p17_flip_k9_t2: reverting fn_t2 without seg_mux commit gate breaks durable k9d segment cross-check
- test_p18_reg_first: durable seg_mux segments precede runtime capture reads after profile_a drill
- test_p19_premature: ready_g8 steady label with disagreeing mirror pairs fails until replay completes
- test_p20_cli_seq: operator_cmds argv sequence required for hs_run hook success

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests (cap 0.5).

### Drafting guardrails

Instruction is design-brief complete about phase obligations, report schema, mirror pairs, coherence predicates, and drill convergence—without naming fn_r7, fn_n3, fn_w8, fn_t2, bind order, stub shard key, or journal replay sequence. Ban instruction nouns from fix-path code symbols and test identifiers. No boolean readiness verdict fields in planned outputs. Do not reduce task to blank-canvas spec transcription.

### Triviality Ledger

- Hand-writing audit_report.json fails test_p10_rerun_flow because verifier reruns cmake + hs_run.
- Fixing only fn_w8 without fn_n3 bind ordering fails test_p14_flip_both and pair coherence subsets.
- Fixing only fn_r7 path-prefix filter without inode witnesses fails test_p12_sens_mut and cross-mount drills.
- Trusting ready_g8 steady label while mirror pairs disagree fails test_p19_premature until seg_mux replay and witness authority align.
- Copying one row from a golden fixture fails test_p7_anchor_hex and test_p12_sens_mut.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle must change semantics in four roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays design-brief without cause-revealing wiring sentences.
- RC5/RC6: schemas and digest home in pilot header; no boolean answer grid in instruction.
- RC7/GX3: solve.sh coordinated across four modules with substantive bodies (target ≥80 LOC semantic delta).
- GX9/GX10: derived digests and pair equality over scenario boolean tables.
- GX4/GX5: ablation tests patch sources in-container; expectations computed in test file.
- CR1/CR2: honor symbol table and flipping-point concentration cap 0.5.

### Initial Draft Commitments

- tasks/hermetic-sandbox-build-contract/task.toml
- tasks/hermetic-sandbox-build-contract/instruction.md
- tasks/hermetic-sandbox-build-contract/output_contract.toml
- tasks/hermetic-sandbox-build-contract/construction_manifest.json
- tasks/hermetic-sandbox-build-contract/tests/test.sh
- tasks/hermetic-sandbox-build-contract/tests/test_outputs.py
- tasks/hermetic-sandbox-build-contract/solution/solve.sh
- tasks/hermetic-sandbox-build-contract/environment/Dockerfile
- tasks/hermetic-sandbox-build-contract/environment/r7k/filter_mux.py
- tasks/hermetic-sandbox-build-contract/environment/r7k/scan_mux.py
- tasks/hermetic-sandbox-build-contract/environment/r7k/path_help.py
- tasks/hermetic-sandbox-build-contract/environment/n3p/root_mux.py
- tasks/hermetic-sandbox-build-contract/environment/n3p/tbl_l4.py
- tasks/hermetic-sandbox-build-contract/environment/n3p/mount_help.py
- tasks/hermetic-sandbox-build-contract/environment/w8q/stub_mux.py
- tasks/hermetic-sandbox-build-contract/environment/w8q/idx_mux.py
- tasks/hermetic-sandbox-build-contract/environment/w8q/cache_help.py
- tasks/hermetic-sandbox-build-contract/environment/t2m/cap_mux.py
- tasks/hermetic-sandbox-build-contract/environment/t2m/ring_mux.py
- tasks/hermetic-sandbox-build-contract/environment/t2m/hash_help.py
- tasks/hermetic-sandbox-build-contract/environment/pilot/entry.py
- tasks/hermetic-sandbox-build-contract/environment/engine/orch_v3.py
- tasks/hermetic-sandbox-build-contract/environment/engine/seg_mux.py
- tasks/hermetic-sandbox-build-contract/environment/engine/ready_g8.py
- tasks/hermetic-sandbox-build-contract/environment/demo_r9/CMakeLists.txt
- tasks/hermetic-sandbox-build-contract/environment/demo_r9/src/main.cpp
- tasks/hermetic-sandbox-build-contract/environment/docs/formal_rules.md
- tasks/hermetic-sandbox-build-contract/environment/docs/tgt_ids.txt
- tasks/hermetic-sandbox-build-contract/environment/docs/operator_cmds.txt
- tasks/hermetic-sandbox-build-contract/environment/data/gate_tbl.json
- tasks/hermetic-sandbox-build-contract/environment/data/cap_tbl.json
- tasks/hermetic-sandbox-build-contract/environment/data/perm_extra.toml
- tasks/hermetic-sandbox-build-contract/environment/data/variant_tbl.toml
- tasks/hermetic-sandbox-build-contract/environment/data/fix_stash/index_a.json
- tasks/hermetic-sandbox-build-contract/environment/data/fix_stash/index_b.json
- tasks/hermetic-sandbox-build-contract/environment/schemas/row_v3.schema.json
- tasks/hermetic-sandbox-build-contract/environment/k9d/seg_v/.gitkeep

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: environment/r7k/filter_mux.py
  symbol: fn_r7
  kind: function
  signature: fn_r7(witness_tbl: dict, mount_set: set) -> tuple[int, bytes]
  purpose: Fold allowlist witness tuples against observed mount inode set
- path: environment/n3p/root_mux.py
  symbol: fn_n3
  kind: function
  signature: fn_n3(sys_tbl: dict, env_map: dict) -> tuple[int, list]
  purpose: Apply sysroot overlay binds before exporting compiler search paths
- path: environment/w8q/stub_mux.py
  symbol: fn_w8
  kind: function
  signature: fn_w8(phase_tag: int, seed_hex: str, shard_tbl: dict) -> dict
  purpose: Select offline registry fixture shard for fetch phase
- path: environment/t2m/cap_mux.py
  symbol: fn_t2
  kind: function
  signature: fn_t2(cap_tbl: dict, blob_paths: list, seg_tag: int) -> tuple[int, dict]
  purpose: Purge undeclared outputs after journal commit and attach ELF section digests

#### flipping_point_contract

locations:
  - id: A
    path: environment/r7k/filter_mux.py
    controls_tests: [test_p1_shape_vecs, test_p2_pair_hex, test_p3_rc_fields, test_p4_label_text, test_p5_width_max]
  - id: B
    path: environment/n3p/root_mux.py
    controls_tests: [test_p6_reduce_hex, test_p7_anchor_hex, test_p8_hex_lower, test_p9_len_vecs]
  - id: C
    path: environment/w8q/stub_mux.py
    controls_tests: [test_p10_rerun_flow, test_p11_twice_same, test_p12_sens_mut, test_p13_flip_w8, test_p14_flip_both]
  - id: D
    path: environment/t2m/cap_mux.py
    controls_tests: [test_p15_flip_t2, test_p16_all_perms, test_p17_flip_k9_t2, test_p18_reg_first, test_p19_premature, test_p20_cli_seq]
no_single_location_flips_majority: true
concentration_cap: 0.5

#### decoy_manifest

- path: environment/r7k/path_help.py
  kind: helper
  rhymes_with: fn_r7
  non_fix_purpose: Normalizes relative path strings for logging without inode witness enforcement
- path: environment/n3p/mount_help.py
  kind: helper
  rhymes_with: fn_n3
  non_fix_purpose: Lists existing mount points for diagnostics without sysroot overlay ordering
- path: environment/w8q/cache_help.py
  kind: helper
  rhymes_with: fn_w8
  non_fix_purpose: Reads newest fixture file mtime for cache warming unrelated to shard selection
- path: environment/t2m/hash_help.py
  kind: helper
  rhymes_with: fn_t2
  non_fix_purpose: Hashes stdout logs for operator diagnostics without ELF section materialization

#### code_forbidden_tokens

code_forbidden_tokens: [hermetic, sandbox, build, contract, allowlisted, inputs, host, headers, sysroot, registry, fixture, dependency, metadata, network, captured, outputs, artifacts, deterministic, digests, audit, replay, phased, driver, offline, locked, workflow, durable, mirror, pairs, coherent, lag, lock, unit, facet, sync, steady, run_digest, manual, static, pipeline, regeneration, sources, rebuild, converge, rollback, recovery, attest, manifest, isolation, namespace, provenance, matrix, targets, argv, hook, reduction, module, comment, rows, summary, tgt_ids, operator_cmds, formal_rules, audit_report, run_traces, bind, bind_echo, upper, upper_echo, worker, worker_echo, facet_hex, sync_label, sched_rc, lock_rc, unit_rc, sixteen, hexadecimal, incoherent, perm_extra, variant_tbl, gauge, purge, shard, witness, overlay, capture, fetch, convergence, elf, section, compiler, include, paths, tarball, declared, terminal, status, subcommand, cmake, demo_r9, hs_run, production, supply, chain, reproducible, wrapper, complete, finishes, satisfies, properties, validating, insufficient, writes, emit, refreshed, shapes, defined, documented, primary, patterns, binds, matching, digit, lowercase, integer, vector, length, fingerprint, known, good, tampered, hand, written, consecutive, mutating, step, ladder, reverting, stock, decoy, helper, breaks, closure, extras, held, cross, precedes, runtime, reads, disagreeing, until, sequence, required, success, gate_tbl, cap_tbl, fix_stash, seg_mux, pipe_mux, gauge_mux, ring_mux, scan_mux, ladder_mux, idx_mux]
