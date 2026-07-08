### Decision

GO — Attempt 1. Validated seed from system-administration#2 post strict hard-only screening. Reframes to `reverse_engineering` task shape with `state_recovery_crash_consistency` category profile. Core hardness derives from coordinating partial writes, replay, cleanup, and rerun safety for frozen cgroup descendants state. Three mandated discoveries, three coordinated implementation topologies, flipping-point ablations across freezer controller semantics, and behavioral-target public obligations without leaking journal internals, recovery phase ordering, or corruption source.

### Metadata

- version: 2
- Task name: cgroup-freezer-resume
- Title: Cgroup freezer resume recovery
- Category: system-administration
- Task shape: reverse_engineering
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["cgroup", "freezer", "process-tree", "state-recovery", "crash-consistency", "resume"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract

After simulated cgroup freezer events, process tree state must resume coherently. The freezer controller tracks frozen/thawed state across a hierarchy. When a subsystem crashes mid-resume, partial state writes can leave descendant processes in inconsistent frozen states that appear recovered locally while violating durable invariants.

Implement a recovery tool under `/app` that:
1. Reads `/app/data/capture.json` and `/app/data/stream.log` to infer the intended frozen/thawed state
2. Repairs source files under `/app/p9/x3/src`, `/app/m2/k81/src`, `/app/p7/y5/src` so that `/app/target/release/resume` produces `/app/output/observations.json`
3. The output file contains traces of the recovery process: process tree captures, phase transitions, and durable integrity markers

The freezer hierarchy uses three controller files per cgroup: `freezer.state` (active), `freezer.parent_freezing` (inherited), and `cgroup.procs` (member processes). A coherent resume requires:
- All leaf cgroups have consistent `freezer.state` and `freezer.parent_freezing` bits
- Descendants honor parent freezing semantics (parent frozen implies descendants frozen)
- The append log records state transitions atomically; partial transitions leave orphaned entries
- Recovery must be idempotent: re-running after successful resume produces identical observations

Verifier tests rebuild from sources, run the recovery tool, and validate observations. See visible argv documentation for verifier command details.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and document category_profile
- path: instruction.md
  role: natural public task prompt (behavioral-target obligations; must not name patch sites or recovery phase internals)
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
- path: environment/a1/b2/src/c3.rs
  role: oracle frontier B — log replay and idempotency detection
- path: environment/d4/e5/src/f6.rs
  role: oracle frontier A — process topology reconstruction from partial writes
- path: environment/g7/h8/src/i9.rs
  role: oracle frontier C — controller phase machine and descendant coherence
- path: environment/a1/b2/src/j0.rs
  role: decoy helper co-resident with c3.rs (non-fix)
- path: environment/d4/e5/src/k1.rs
  role: decoy helper co-resident with f6.rs (non-fix)
- path: environment/g7/h8/src/l2.rs
  role: decoy helper co-resident with i9.rs (non-fix)
- path: environment/data/capture.json
  role: durable state capture before crash
- path: environment/data/stream.log
  role: append-only transition stream with partial write markers
- path: environment/docs/semantics.md
  role: internal contract doc for controller semantics and recovery rules

### fix_frontier

- count: 3
- distribution: `environment/a1/b2/src/c3.rs`, `environment/d4/e5/src/f6.rs`, `environment/g7/h8/src/i9.rs` (distinct crate roots under a1, d4, g7)
- naming_policy: Keep opaque Rust identifiers on the fix path (`rebuild_hierarchy`, `replay_entries`, `coerce_descendants`); do not rename to instruction nouns
- forbidden_stems: cgroup, freezer, resume, recovery, process, descendant, frozen, thawed, controller, hierarchy, parent, child, leaf, durable, partial, replay, cleanup, idempotent, rerun, coherent, inconsistent, orphan, entry, transition, semantic, integrity, marker, observation, fixture, recover, repair, cargo_toml
- helpers_policy: Co-resident crate roots and rhyming decoys perform credible adjacent work; `j0.rs`, `k1.rs`, `l2.rs` are declared co-resident helpers; frontier stays thin at three fix symbols
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 10
- preferred_assertion_styles: observation traces, state transition logs, integrity checksums, idempotency verification, hierarchy coherence checks
- forbidden_assertion_styles: scenario→key→expected boolean tables in instruction.md; per-scenario answer rows in docs; boolean answer-key JSON fields named `overall_pass` or `scenario_pass`

### task_shape

- type: reverse_engineering
- instruction_framing: behavioral-target
- hardness_source: semantic inference — infer latent freezer controller semantics from traces and malformed fixtures to produce compatible recovery implementation
- collapse_risk: leaking journal replay algorithm, exact recovery phase ordering, or corruption source location collapses to localized one-file repair

### category_profile

- challenge_family: process_tree_resume_recovery
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: crash/restart workflow, durability guarantee, recovery command, expected observable state, freezer controller semantics (FROZEN/THAWED), hierarchy rules, idempotency requirement, observation schema
- forbidden_instruction_leaks: journal/checkpoint internals, broken recovery phase, corruption source, replay function, cleanup path, exact phase ordering
- category_specific_hardness_bar: partial writes, replay, cleanup, idempotence, and rerun safety must all coordinate
- category_specific_verifier_risks: nondeterministic crash timing, one hidden snapshot, verifier reading internals
- coverage_role: Adds system-administration coverage for reverse_engineering using freezer descendants state topology

### satisfiability_risk

- rc2_planned_name_risk: low — planned names use opaque crate paths (p9/x3, m2/k81, p7/y5) with neutral function identifiers
- gx9_contract_risk: low — observation traces contain process tree snapshots and state transitions; booleans are product-shaped consistency markers
- cr1_symbol_frontier_risk: low — three substantive Rust modules plus distributed helper stubs
- hidden_contract_risk: low — commands, schemas, and recovery workflow are instruction-visible; partial write markers are discoverable from fixtures

### actionability_plan

- verifier_command_visible: `cargo build --release` from `/app` and driver at `/app/target/release/resume`; pytest via pre-installed environment
- source_fix_intent_visible: instruction requires inferring freezer semantics to satisfy durability and coherence constraints; does not name `rebuild_hierarchy`, `replay_entries`, or `coerce_descendants`
- generated_output_rule_visible: `/app/output/observations.json` path and field names
- exact_formula_home: module comments in `environment/d4/e5/src/main.rs` plus `environment/docs/semantics.md` (state machine rules, hierarchy coherence invariants)
- schema_home: instruction.md public contract + output_contract.toml paths

### waiver_plan

- waivers_expected: no
- waiver_rationale: Standard freezer semantics are documented in kernel documentation; task avoids hidden-instance puzzles through deterministic fixture design

### reference_pattern

- justification_if_none: Construction follows state_recovery_crash_consistency profile with reverse_engineering task shape. No promoted reference in `docs/reference_tasks/index.json` matches this exact cgroup/freezer domain combination. Task draws on real cgroup freezer controller semantics from Linux kernel documentation.

### realism_source

- source_type: real_system
- evidence_basis: tool behavior
- upstream_or_synthetic_rationale: Based on real cgroup v1 freezer controller semantics from Linux kernel documentation; minimized to core state recovery challenge without requiring actual kernel namespaces
- minimization_preserves: Causal structure of partial write recovery, idempotency requirements, and hierarchical state coherence
- synthetic_exception_review: Not required for real_system source

### difficulty_mechanism_plan

- mechanisms: rollback_recovery_requirements, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, partial_observability_experiment_design, buried_local_constraints, stateful_multi_step_dependencies
- adversarial_layers_count: 6
- fairness_guardrails: All tested invariants derive from documented freezer semantics; deterministic rebuild; no timing/latency thresholds
- mechanism: rollback_recovery_requirements
  placement: stream.log scenarios spanning simulated crash, partial capture write, then recovery replay
  why_model_misses_it: agents fix visible state without ensuring idempotent re-run safety
  fairness_guardrail: capture.json and stream.log fixtures document crash scenarios
- mechanism: deceptive_but_valid_local_evidence
  placement: probe.rs in p9/x3 shows coherent local state that may diverge from durable capture
  why_model_misses_it: runtime-visible state looks correct while stream replay reveals inconsistencies
  fairness_guardrail: docs/semantics.md defines durable vs runtime state distinction
- mechanism: cross_file_cross_format_invariants
  placement: JSON capture vs text stream log vs binary state representation must agree on process membership
  why_model_misses_it: editing one format leaves orphans that pass shallow state checks
  fairness_guardrail: cross-format agreement rules in semantics.md
- mechanism: partial_observability_experiment_design
  placement: stream.log contains partial write markers requiring inference of intended complete state
  why_model_misses_it: models treat complete stream entries as authoritative without detecting truncation
  fairness_guardrail: stream format documents partial write markers explicitly
- mechanism: buried_local_constraints
  placement: rebuild_hierarchy must detect and repair parent/child state violations, not just parse topology
  why_model_misses_it: looks like simple topology parsing exercise
  fairness_guardrail: ablation test reverts hierarchy repair body
- mechanism: stateful_multi_step_dependencies
  placement: driver phases select which recovery surfaces participate before final observation scoring
  why_model_misses_it: default phase hides capture/stream conflicts until full recovery runs
  fairness_guardrail: semantics.md documents recovery phases without naming internal functions

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert can satisfy durability and coherence constraints using freezer_semantics.md and regenerated observations within a few hours
- shortcut_audit: static JSON, test deletion, stale-doc-only edits, reward file writes, state hardcoding, single-surface recovery
- ablation_plan: revert rebuild_hierarchy only, replay_entries only, coerce_descendants only — each should drop pass rate on disjoint test subsets
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

Cgroup freezer state recovery requires reconciling three surfaces after a simulated crash mid-resume: the durable capture.json, the append-only stream.log with partial write markers, and the runtime-visible process tree state. Local coherence checks can pass while durable invariants fail — a parent cgroup may report THAWED while descendants remain FROZEN due to incomplete stream replay, or orphaned stream entries may reference processes that no longer exist. Hardness requires inferring the complete intended state from partial evidence, implementing idempotent recovery (re-running produces identical observations), and ensuring hierarchical coherence (parent state dominates descendants) without the instruction naming which replay ordering, which cleanup phase, or which state coercion logic is defective.

### Environment shape

Rust Cargo workspace under `/app` with driver in `d4/e5/src/main.rs` and fix frontier across `a1/b2/src/c3.rs`, `d4/e5/src/f6.rs`, `g7/h8/src/i9.rs`. Helper stubs `a1/b2/src/j0.rs`, `d4/e5/src/k1.rs`, `g7/h8/src/l2.rs` provide decoy functionality. Fixtures under `environment/data/` (`capture.json`, `stream.log`). Contract in `environment/docs/semantics.md`. Output at `/app/output/observations.json`. Minimum 20 non-Docker environment files across source, fixtures, and documentation.

### Required artifacts

instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh, solution/oracle.patch, and the environment tree listed in Initial Draft Commitments.

### Test plan

- `test_cfr_t1_shape`: observation JSON shape; required fields present
- `test_cfr_t2_hierarchy`: process tree hierarchy reconstructed from fixtures
- `test_cfr_t3_mode`: controller mode FROZEN/THAWED values valid per semantics
- `test_cfr_t4_ancestor`: ancestor frozen implies descendants frozen (hierarchical invariant)
- `test_cfr_t5_stray`: stray stream entries detected and handled
- `test_cfr_t6_truncated`: truncated write markers detected in stream.log
- `test_cfr_t7_repeat`: consecutive runs produce identical observations
- `test_cfr_t8_digest`: integrity digests consistent across hierarchy
- `test_cfr_t9_durable`: durable capture precedence over runtime state
- `test_cfr_t10_sequence`: stream replay produces correct transition sequence
- `test_cfr_t11_manual`: static/manual JSON write detected (pipeline trap)
- `test_cfr_a1_ab`: reverting f6.rs hierarchy repair breaks coherence
- `test_cfr_a2_cd`: reverting c3.rs replay breaks idempotency
- `test_cfr_a3_ef`: reverting i9.rs coercion breaks ancestor-descendant invariant
- `test_cfr_k1_gh`: fast-path state read without stream replay fails
- `test_cfr_k2_ij`: ignoring stray entries produces false coherence

Test names must not contain instruction forbidden stems as substrings. Each flipping-point location controls at most 50% of tests.

### Drafting guardrails

Instruction is behavioral-target: state the durability and coherence constraints, expected observations, and freezer semantics without naming `rebuild_hierarchy`, `replay_entries`, `coerce_descendants`, journal replay phase, or recovery ordering. Do not use overlay mold language — this is a reverse_engineering task where the agent infers semantics from fixtures. Tests derive verdicts from regenerated JSON, idempotency traps, hierarchy coherence checks, and ablations—not static answer keys.

### Triviality Ledger

- Hand-writing observations.json fails `test_cfr_t11_manual` because verifier reruns cargo + driver.
- Fixing only f6.rs without c3.rs fails `test_cfr_t7_repeat` and sequence subsets.
- Fixing only stream replay without hierarchy repair fails `test_cfr_t4_ancestor` and `test_cfr_a1_ab`.
- Satisfying runtime state without durable capture precedence fails `test_cfr_t9_durable`.
- Single-pass mode update without repeatability check fails `test_cfr_t7_repeat` and `test_cfr_a2_hold`.
- Ignoring stray stream entries fails `test_cfr_t5_stray` and `test_cfr_k2_stray`.

### Per-gate Pitfall Inventory

- RC1/GX2: oracle patch must change semantics in three roots; forbid single-file wholesale workspace replace.
- RC2: instruction nouns listed in code_forbidden_tokens must not appear as fix-path symbol or directory names.
- RC3/RC4: instruction stays behavioral-target about observations, not cause-revealing.
- RC5/RC6: schemas and state rules in semantics.md; no boolean answer grid in instruction.
- RC7/GX3: oracle.patch coordinated across f6/c3/i9 with substantive bodies.
- GX9/GX10: derived integrity markers and hierarchy checks; no per-scenario expected literals in instruction.
- GX4/GX5: ablation tests patch sources in-container; expectations computed from contract functions in test file.
- Static: run `collapse_check.py --check flipping_point_compliance` and `grep_resistance` after Step 2b.

### Initial Draft Commitments

- tasks/cgroup-freezer-resume/task.toml
- tasks/cgroup-freezer-resume/instruction.md
- tasks/cgroup-freezer-resume/output_contract.toml
- tasks/cgroup-freezer-resume/construction_manifest.json
- tasks/cgroup-freezer-resume/tests/test.sh
- tasks/cgroup-freezer-resume/tests/test_outputs.py
- tasks/cgroup-freezer-resume/solution/solve.sh
- tasks/cgroup-freezer-resume/solution/oracle.patch
- tasks/cgroup-freezer-resume/environment/Dockerfile
- tasks/cgroup-freezer-resume/environment/Cargo.toml
- tasks/cgroup-freezer-resume/environment/Cargo.lock
- tasks/cgroup-freezer-resume/environment/a1/b2/src/c3.rs
- tasks/cgroup-freezer-resume/environment/a1/b2/src/j0.rs
- tasks/cgroup-freezer-resume/environment/a1/b2/Cargo.toml
- tasks/cgroup-freezer-resume/environment/d4/e5/src/f6.rs
- tasks/cgroup-freezer-resume/environment/d4/e5/src/k1.rs
- tasks/cgroup-freezer-resume/environment/d4/e5/src/main.rs
- tasks/cgroup-freezer-resume/environment/d4/e5/Cargo.toml
- tasks/cgroup-freezer-resume/environment/g7/h8/src/i9.rs
- tasks/cgroup-freezer-resume/environment/g7/h8/src/l2.rs
- tasks/cgroup-freezer-resume/environment/g7/h8/Cargo.toml
- tasks/cgroup-freezer-resume/environment/data/capture.json
- tasks/cgroup-freezer-resume/environment/data/stream.log
- tasks/cgroup-freezer-resume/environment/docs/semantics.md
- tasks/cgroup-freezer-resume/environment/docs/build_hints.txt

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/d4/e5/src/f6.rs
  symbol: rebuild_hierarchy
  kind: function
  signature: rebuild_hierarchy(capture: &Capture, partial_topology: &mut ProcessTopology) -> Result<HierarchyState, TopologyError>
  purpose: Reconstructs complete process topology from capture and partial runtime state, detecting parent/child violations
- path: environment/a1/b2/src/c3.rs
  symbol: replay_entries
  kind: function
  signature: replay_entries(stream: &StreamLog, mode: &mut ControllerMode) -> Result<ReplaySummary, LogError>
  purpose: Replays stream entries idempotently, handling partial write markers and stray entries
- path: environment/g7/h8/src/i9.rs
  symbol: coerce_descendants
  kind: function
  signature: coerce_descendants(parent_mode: ControllerMode, topology: &ProcessTopology, out: &mut Vec<ModeCmd>)
  purpose: Generates mode commands to enforce hierarchical coherence (parent frozen implies descendants frozen)
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/d4/e5/src/f6.rs
    controls_tests: [test_cfr_t2_hierarchy, test_cfr_t4_ancestor, test_cfr_t9_durable, test_cfr_a1_ab, test_cfr_k2_ij]
  - id: B
    path: environment/a1/b2/src/c3.rs
    controls_tests: [test_cfr_t6_truncated, test_cfr_t7_repeat, test_cfr_t10_sequence, test_cfr_a2_cd, test_cfr_k1_gh]
  - id: C
    path: environment/g7/h8/src/i9.rs
    controls_tests: [test_cfr_t3_mode, test_cfr_t5_stray, test_cfr_t8_digest, test_cfr_a3_ef, test_cfr_t11_manual]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/a1/b2/src/j0.rs
  kind: module
  rhymes_with: c3
  non_fix_purpose: Helper functions co-resident with c3.rs; performs real pack operations
- path: environment/d4/e5/src/k1.rs
  kind: helper
  rhymes_with: f6
  non_fix_purpose: Step key utilities co-resident with f6.rs; not the topology fix
- path: environment/g7/h8/src/l2.rs
  kind: helper
  rhymes_with: i9
  non_fix_purpose: Fold utilities co-resident with i9.rs; not the mode fix
```

#### code_forbidden_tokens

```
cgroup, freezer, resume, recovery, process, descendant, frozen, thawed, controller, hierarchy, parent, child, leaf, durable, partial, replay, cleanup, idempotent, rerun, coherent, inconsistent, orphan, entry, transition, semantic, integrity, marker, observation, fixture, recover, repair, cargo_toml
```
