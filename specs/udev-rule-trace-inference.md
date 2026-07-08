### Decision
GO — Attempt 1. Python udev-policy lab with three-package fix frontier; naming pass cleared instruction-noun collisions; committed cross-band digest and health-subcommand false-green traps.

### Metadata
- version: 2
- Task name: udev-rule-trace-inference
- Title: Udev Rule Trace Inference
- Category: system-administration
- Task shape: reverse_engineering
- Languages: ["Python"]
- Difficulty: hard
- Codebase size: small
- Subcategories: ["tool_specific"]
- Tags: ["reverse-engineering", "udev", "systemd", "config-policy", "sysadmin"]
- Milestones: 0

## Authoring Brief

### Public contract

A system administration lab ships incomplete device policy configuration: cold-plug event traces show mismatched symlink targets and unstable effective policy after reload cycles. Infer the missing matching behavior from partial trace excerpts and policy fragments, then repair the Python sources under `/app/environment` so the replay verifier converges for every scope.

Public verifier:

```bash
/app/environment/tools/urli_verify --all-scenarios --witness-out /app/output/policy_witness.json
```

Rebuild with `/app/environment/scripts/bake_ws.sh` before running. Success requires:

1. Terminal checker exit 0 for all four device scopes (`pocket`, `ridge`, `slate`, `marsh`) under both matrix profiles (`north`, `south`).
2. Row invariants per scenario/profile in `policy_witness.json` (schema in `environment/docs/layout_contract.md`).
3. `trace_digest` fields matching sha256 over canonical replay row bytes for each scenario/profile pair.

**Partial observability:** Text excerpts under `/app/output/logs` omit cold-plug steps; authoritative slices live in `environment/fixtures/slices/*.bin`.

**False-green trap:** `/app/output/stage` and `environment/fixtures/interim_snaps/q7_stub.json` may show local rule counts while `trace_digest` cross-check still fails. The graded artifact is terminal `policy_witness.json` from the full `--all-scenarios` run.

**Recovery:** Repeat `environment/migrations/wipe9.sh` only via the idempotent recovery command in `layout_contract.md` before re-running the verifier.

Hardcoding `policy_witness.json`, fragment-only edits without source changes, or test modifications are insufficient.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public prompt derived from Public contract above
- path: output_contract.toml
  role: local output declaration for policy_witness.json
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed pytest only (no runtime apt/pip/curl)
- path: tests/test_outputs.py
  role: domain verifier (13 tests)
- path: solution/solve.sh
  role: oracle coordinating resolve_row_a, emit_plan_b, ensure_gate_c
- path: environment/Dockerfile
  role: build definition; pre-install pinned python, pytest, lab package
- path: construction_manifest.json
  role: local authoring artifact mirroring symbol table below

### task_files

- path: environment/py_src/urli/pyproject.toml
  role: Python package manifest
- path: environment/py_src/urli/registry/__init__.py
  role: registry package root
- path: environment/py_src/urli/registry/resolve_a.py
  role: fix frontier A
- path: environment/py_src/urli/registry/legacy_registry.py
  role: decoy registry helper
- path: environment/py_src/urli/registry/pack_k.py
  role: slot packing definitions
- path: environment/py_src/urli/loader/__init__.py
  role: loader package root
- path: environment/py_src/urli/loader/attach_b.py
  role: fix frontier B
- path: environment/py_src/urli/loader/stub_attach.py
  role: decoy attach helper
- path: environment/py_src/urli/loader/row_fmt.py
  role: row formatting helpers
- path: environment/py_src/urli/semctl/__init__.py
  role: semctl package root
- path: environment/py_src/urli/semctl/eval_c.py
  role: fix frontier C
- path: environment/py_src/urli/semctl/stub_pulse.py
  role: decoy pulse helper
- path: environment/py_src/urli/semctl/arena_store.py
  role: cleanup-sensitive scratch state
- path: environment/py_src/urli/semctl/pulse_fmt.py
  role: notification formatting
- path: environment/py_src/urli/collector/__init__.py
  role: collector package root
- path: environment/py_src/urli/collector/emit_q.py
  role: row emitter decoy
- path: environment/tools/urli_verify/main.py
  role: checker CLI entry
- path: environment/tools/urli_verify/core_k.py
  role: digest and row invariant validation
- path: environment/profiles/north.toml
  role: north matrix profile constants
- path: environment/profiles/south.toml
  role: south matrix profile constants
- path: environment/scenarios/pocket.json
  role: device scope definition
- path: environment/scenarios/ridge.json
  role: device scope definition
- path: environment/scenarios/slate.json
  role: device scope definition
- path: environment/scenarios/marsh.json
  role: device scope definition
- path: environment/docs/layout_contract.md
  role: witness schema, trace_digest rule, recovery command
- path: environment/docs/col_glossary.md
  role: public cold-plug row semantics and status tokens
- path: environment/migrations/wipe9.sh
  role: destructive wipe with documented recovery
- path: environment/fixtures/slices/pocket_part.bin
  role: partial slice for pocket
- path: environment/fixtures/slices/ridge_full.bin
  role: full slice for ridge
- path: environment/fixtures/slices/slate_part.bin
  role: partial slice for slate
- path: environment/fixtures/slices/marsh_full.bin
  role: full slice for marsh
- path: environment/fixtures/interim_snaps/q7_stub.json
  role: false-green intermediate tallies
- path: environment/scripts/bake_ws.sh
  role: pip install / workspace bake entry
- path: environment/scripts/run_matrix.sh
  role: scenario/profile matrix driver for checker

### fix_frontier

- count: 3
- distribution: py_src/urli/registry, py_src/urli/loader, py_src/urli/semctl package roots
- naming_policy: Opaque symbols from construction manifest symbol_table only
- forbidden_stems: [cold-plug, traces, symlink, effective, reload, matching, behavior, partial, excerpts, fragments, replay, verifier, witness, digest, canonical, observability, authoritative, stage, counts, cross-check, graded, artifact, recovery, hardcoding, convergence, precedence, inotify, systemd, plug, policy, device, configuration, event, targets, cycles, sources, fragment, modifications, priority, bands, health, status, subcommands, rules, harness, laboratory, coldplug, watch, flush, rank, catalog, scratch, tallies, rows, python, infer, missing, unstable, mismatched, converges, terminal, documented, idempotent, insufficient, changes, edits]
- helpers_policy: Decoys may rhyme structurally; oracle must not edit decoy bodies
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [trace digests, checker exit codes, row count invariants, schema field equality, cross-profile invariants]
- forbidden_assertion_styles: [boolean answer keys, scenario->field->expected tables, fields ending in _ok/_valid/_passes]

### task_shape

- type: reverse_engineering
- instruction_framing: behavioral-target
- hardness_source: semantic inference
- collapse_risk: single magic constant or hidden-instance lookup

### category_profile

- challenge_family: udev rule inference
- profile_name: config_policy_precedence
- allowed_instruction_disclosures: Observable cold-plug traces, public urli_verify command, effective-policy outcomes, reload behavior, policy_witness schema, partial excerpts, recovery command, scenario/profile matrix
- forbidden_instruction_leaks: Root cause, fix location, patch recipe, oracle transcript, fix-path symbol names, internal precedence table location
- category_specific_hardness_bar: Registry resolution, loader attach tables, semctl gate, collector emission, and checker digests coordinate across four device scopes and two matrix profiles
- category_specific_verifier_risks: False greens from health subcommands or golden fixtures, policy-table transcription, one config file shortcut
- coverage_role: Strengthens config_policy_precedence coverage via udev rule trace inference (distinct from perf-trace-event-inference)

### difficulty_mechanism_plan

- mechanisms: [stateful_multi_step_dependencies, deceptive_but_valid_local_evidence, false_green_intermediate_states, cross_file_cross_format_invariants, partial_observability_experiment_design, environment_specific_cli_semantics]
- adversarial_layers_count: 6
- fairness_guardrails: Every layer is discoverable from docs, binary fixtures, and the public checker command
- mechanism: stateful_multi_step_dependencies
  placement: sequential urli_verify grid after migrations/wipe9.sh and bake_ws.sh
  why_model_misses_it: Models treat wipe as idempotent on visible health tallies and skip arena_store coupling across replay phases
  fairness_guardrail: Recovery command documented in layout_contract.md with idempotent rerun semantics
- mechanism: deceptive_but_valid_local_evidence
  placement: health/status subcommands and fixtures/interim_snaps/q7_stub.json
  why_model_misses_it: Agents treat matching health counts as completion while trace_digest fails
  fairness_guardrail: Instruction states terminal policy_witness.json from full --all-scenarios run is graded
- mechanism: false_green_intermediate_states
  placement: /app/output/stage and interim note JSON
  why_model_misses_it: Single-scenario replay checks pass before cross-profile digest convergence
  fairness_guardrail: Public contract names graded artifact and cross-profile digest bands
- mechanism: cross_file_cross_format_invariants
  placement: policy_witness.json trace_digest vs canonical collector replay bytes
  why_model_misses_it: Models edit JSON summaries without rebuilding emitted replay rows
  fairness_guardrail: layout_contract.md documents sha256 trace_digest publicly
- mechanism: partial_observability_experiment_design
  placement: /app/output/logs excerpts vs environment/fixtures/slices/*.bin
  why_model_misses_it: Models infer matching order from incomplete textual excerpts alone
  fairness_guardrail: Instruction names authoritative binary slices and four-scenario checker matrix
- mechanism: environment_specific_cli_semantics
  placement: urli_verify flags and run_matrix.sh driver
  why_model_misses_it: Models assume generic udev helper behavior instead of profile-scoped replay semantics
  fairness_guardrail: Instruction names exact urli_verify command and north/south profile labels

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: Systems administrator reproduces failing urli_verify locally using bundled trace slices and excerpts only
- shortcut_audit: Block hardcoded policy_witness.json, fragment-only edits without workspace bake, test modifications
- ablation_plan: Remove partial-excerpt layer, then digest layer, then health-subcommand layer; expect monotonic difficulty drop
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=Part E Hard threshold on worst-model accuracy; verifier-offline via Dockerfile-baked pytest with no runtime installs in test.sh under allow_internet=false; post-upload difficulty classification after platform agent runs

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt=1 only when all weighted metrics pass

### subtype_milestone_plan

- subcategories: [tool_specific]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: Single-container local verifier; Python lab and urli_verify baked in Dockerfile

### satisfiability_risk

- rc2_planned_name_risk: low — opaque fix-path symbols precommitted in symbol_table
- gx9_contract_risk: low — contract uses digests and row invariants, not boolean verdict tables
- cr1_symbol_frontier_risk: low — frontier spans three Python package roots with decoys
- hidden_contract_risk: medium — trace_digest and watch-flush rules live in layout_contract.md and checker behavior

### actionability_plan

- verifier_command_visible: urli_verify --all-scenarios documented in instruction.md
- source_fix_intent_visible: yes — fix Python sources under /app/environment and rebuild; no patch recipe
- generated_output_rule_visible: policy_witness.json path and schema public
- exact_formula_home: environment/docs/layout_contract.md for trace_digest sha256
- schema_home: instruction.md plus environment/docs/layout_contract.md

### waiver_plan

- waivers_expected: false
- waiver_rationale: Hardness from coupled udev policy precedence behavior, not harness brittleness

### reference_pattern

- reference_task_id:
- justification_if_none: No promoted reference in docs/reference_tasks/index.json covers Python reverse-engineered udev rule trace inference with cross-profile digest witnesses; perf-trace-event-inference is Rust-shaped and not promoted

### realism_source

- source_type: real_system
- evidence_basis: open-source issue
- upstream_or_synthetic_rationale: Minimized from production fleet udev/systemd incidents: ENV/ATTR matching order drifted across reload, systemd link priority disagreed with symlink targets, and inotify events raced rule load leaving stale effective policy on cold-plug
- minimization_preserves: Causal coupling between registry precedence, loader rank bands, semctl flush ordering, and graded replay witnesses
- synthetic_exception_review: not required

### Failure topology

Cold-plug trace excerpts show consistent row shapes but disagree on which symlink target becomes effective after reload, implying the registry catalog and loader rank tables are misaligned. Matrix profile `south` shifts link-rank precedence relative to `north`, so a matching strategy that satisfies pocket under one profile fails slate row invariants under the other. Health subcommands on slate/marsh emit plausible rule counts unless watch notifications are flushed before reload, producing intermediate tallies without canonical replay bytes. ENV versus ATTR slot ordering inserts hidden precedence boundaries so excerpt-driven inference suggests the wrong catalog slot until all three Python roots align. The checker binds JSON witnesses to rebuilt collector output, so hand-written summaries fail even when stage tallies look complete.

### Environment shape

- `environment/py_src/urli/` — Python lab (registry, loader, semctl, collector packages)
- `environment/tools/urli_verify/` — digest and row-invariant checker CLI
- `environment/profiles/` — north and south matrix parameter files
- `environment/scenarios/` — four seeded device scope definitions
- `environment/docs/` — check contract and column layout semantics (solver-visible)
- `environment/fixtures/slices/` — binary trace slices for partial observability
- `environment/fixtures/interim/` — false-green intermediate tally artifacts
- `environment/migrations/` — destructive wipe with documented recovery
- `environment/scripts/` — workspace bake and matrix driver entrypoints

### Required artifacts

Step 2b creates: `task.toml` (`allow_internet = false`), `instruction.md`, `output_contract.toml`, `tests/test.sh`, `tests/test_outputs.py` (8 tests), `solution/solve.sh`, `environment/Dockerfile` (pinned python/pytest), all task_files above, and `construction_manifest.json` matching the symbol table. Environment must contain 20+ non-Docker files.

### Test plan

1. `test_cli_exit_all_pairs` — urli_verify exit 0 for all scenarios × profiles; chain-dependent on baked workspace
2. `test_cross_format_byte_hash` — trace_digest matches sha256 of rebuilt canonical replay bytes
3. `test_prio_b_obligations` — south-profile scenarios fail if matching uses north precedence table
4. `test_prio_a_baseline` — north profile remains passing after south-oriented fixes
5. `test_semantic_flush_invariant` — slate/marsh scenarios require watch-flush semantics, not registry-only patches
6. `test_width_boundary_guard` — pocket/ridge row-width boundaries enforced via witness row counts
7. `test_q7_totals_trap` — intermediate tallies alone do not satisfy terminal witness grading
8. `test_cycle_repeatable_guard` — documented recovery after wipe preserves slice fixture integrity
9. `test_link_tag_derivation` — link_tag matches sha256 pipe-joined column label digest prefix
10. `test_epoch_mark_monotone` — epoch_mark strictly increases within each profile across scope order
11. `test_band_spread_monotone` — band_spread strictly increases within each profile across scope order
12. `test_scope_seq_ladder` — matrix_seq equals one-based scope index per profile
13. `test_chain_tail_progression` — chain_tail carries previous scope digest within each profile

### Drafting guardrails

Do not place instruction nouns on fix-path symbols or Python module names tied to the oracle. Do not embed oracle hints in environment comments. Keep witness contract in layout_contract.md, not only in tests. Ensure checker diagnostics never name resolve_row_a, emit_plan_b, or ensure_gate_c. Avoid boolean verdict fields in policy_witness.json. Primary implementation language is Python; verifier remains pytest-only.

### Triviality Ledger

- Hand-written policy_witness.json passes stage tallies but fails `test_cross_format_byte_hash` because collector replay bytes are unchanged.
- Fragment-only rule edits can clear health subcommand counts while `test_prio_b_obligations` fails because south precedence remains wrong.
- Registry-only shortcuts satisfy pocket intermediate output but `test_semantic_flush_invariant` fails on slate/marsh watch-flush scenarios.
- Picking the first plausible catalog slot passes pocket smoke but fails `test_width_boundary_guard` on ridge row-width boundaries.

### Per-gate Pitfall Inventory

- RC1: Oracle must perform substantive cross-package Python edits, not byte-identical rewrites (GX4).
- RC2: Fix-path symbols stay opaque; instruction nouns banned via code_forbidden_tokens; test names must not embed those nouns.
- RC6: Instruction stays behavioral-target, not spec-complete with full matching recipe.
- RC7/GX3: Oracle solve.sh must coordinate workspace bake plus three symbols with substantive logic.
- CR1: Three fix roots required; decoys stay off oracle path.
- GX9: Do not enumerate per-scenario witness field values in instruction.md.
- GX10: Avoid naming both gate polarities for one scenario in a single ambiguous sentence.
- GX6: Limit causal chains that reveal patch order across registry, loader, and semctl.

### Initial Draft Commitments

- task.toml
- instruction.md
- output_contract.toml
- construction_manifest.json
- tests/test.sh
- tests/test_outputs.py
- solution/solve.sh
- environment/Dockerfile
- environment/py_src/urli/pyproject.toml
- environment/py_src/urli/registry/__init__.py
- environment/py_src/urli/registry/resolve_a.py
- environment/py_src/urli/registry/legacy_registry.py
- environment/py_src/urli/registry/pack_k.py
- environment/py_src/urli/loader/__init__.py
- environment/py_src/urli/loader/attach_b.py
- environment/py_src/urli/loader/stub_attach.py
- environment/py_src/urli/loader/row_fmt.py
- environment/py_src/urli/semctl/__init__.py
- environment/py_src/urli/semctl/eval_c.py
- environment/py_src/urli/semctl/stub_pulse.py
- environment/py_src/urli/semctl/arena_store.py
- environment/py_src/urli/semctl/pulse_fmt.py
- environment/py_src/urli/collector/__init__.py
- environment/py_src/urli/collector/emit_q.py
- environment/tools/urli_verify/main.py
- environment/tools/urli_verify/core_k.py
- environment/profiles/north.toml
- environment/profiles/south.toml
- environment/scenarios/pocket.json
- environment/scenarios/ridge.json
- environment/scenarios/slate.json
- environment/scenarios/marsh.json
- environment/docs/layout_contract.md
- environment/docs/col_glossary.md
- environment/migrations/wipe9.sh
- environment/fixtures/slices/pocket_part.bin
- environment/fixtures/slices/ridge_full.bin
- environment/fixtures/slices/slate_part.bin
- environment/fixtures/slices/marsh_full.bin
- environment/fixtures/interim_snaps/q7_stub.json
- environment/scripts/bake_ws.sh
- environment/scripts/run_matrix.sh

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: environment/py_src/urli/registry/resolve_a.py
  symbol: resolve_row_a
  kind: function
  signature: def resolve_row_a(row: TraceRow, catalog: SlotCatalog) -> SlotId:
  purpose: Maps cold-plug row to catalog slot using profile-selected matching strategy

- path: environment/py_src/urli/loader/attach_b.py
  symbol: emit_plan_b
  kind: function
  signature: def emit_plan_b(spec: LinkSpec, target: SymlinkRef, site: RankSite) -> LinkPlan:
  purpose: Emits ranked link plan bytes respecting profile-specific precedence

- path: environment/py_src/urli/semctl/eval_c.py
  symbol: ensure_gate_c
  kind: function
  signature: def ensure_gate_c(store: RuleStore, watch: WatchRef) -> GateState:
  purpose: Evaluates whether pending watch notifications must flush before rule reload

#### flipping_point_contract

locations:
  - id: A
    path: environment/py_src/urli/registry/resolve_a.py
    controls_tests: [test_cli_exit_all_pairs, test_cross_format_byte_hash, test_width_boundary_guard]
  - id: B
    path: environment/py_src/urli/loader/attach_b.py
    controls_tests: [test_prio_b_obligations, test_prio_a_baseline]
  - id: C
    path: environment/py_src/urli/semctl/eval_c.py
    controls_tests: [test_semantic_flush_invariant, test_q7_totals_trap, test_cycle_repeatable_guard]
no_single_location_flips_majority: true
concentration_cap: 0.5

#### decoy_manifest

- path: environment/py_src/urli/registry/legacy_registry.py
  kind: module
  rhymes_with: resolve_row_a
  non_fix_purpose: Deprecated slot table used only by offline benchmarks

- path: environment/py_src/urli/loader/stub_attach.py
  kind: helper
  rhymes_with: emit_plan_b
  non_fix_purpose: No-op attach planner for simulator builds without rank bands

- path: environment/py_src/urli/collector/emit_q.py
  kind: helper
  rhymes_with: ensure_gate_c
  non_fix_purpose: Formats replay rows without mutating watch or rank state

#### code_forbidden_tokens

code_forbidden_tokens: [cold-plug, traces, symlink, effective, reload, matching, behavior, partial, excerpts, fragments, replay, verifier, witness, digest, canonical, observability, authoritative, stage, counts, cross-check, graded, artifact, recovery, hardcoding, convergence, precedence, inotify, systemd, plug, policy, device, configuration, event, targets, cycles, sources, fragment, modifications, priority, bands, health, status, subcommands, rules, harness, laboratory, coldplug, watch, flush, rank, catalog, scratch, tallies, rows, python, infer, missing, unstable, mismatched, converges, terminal, documented, idempotent, insufficient, changes, edits]
