### Decision
GO — Attempt 3. The task is a repair-shaped recovery problem whose public prompt can remain symptoms-only while the local environment forces diagnosis across replay, cleanup, durable artifacts, and regenerated observations.

- Attempt 1 and 2 design verdicts were sound but evidence IDs/labels did not match the strict schema; Attempt 3 fixes those structural evidence issues.
- The spec blocks the main collapse risk by distributing the fix frontier across four roots and keeping the trusted-artifact/authority mismatch out of public naming.
- No files under `tasks/` are created in this step; this file is the Step-2b authoring input.

### Metadata
- version: 2
- Task name: live-migration-shadow-state-variant-2
- Title: Migration Recovery Drift
- Category: software-engineering
- Task shape: repair_existing_system
- Languages: ["cpp", "bash"]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: ["recovery", "migration", "checkpoint", "replay", "state"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
A local migration harness restores workloads from checkpoint bundles and writes `/app/output/migration_observations.json`. A bug report says recovered workloads can pass the first health report, but later generations show drift in records, ownership lineage, and recovered artifacts after replay and cleanup sequences. The solver must fix source under `/app/environment` so the normal runner regenerates the observations, preserves active workload state across replay boundaries, and produces repeatable reports after output deletion. Static/manual output writes, test edits, bypassing the runner, or direct reward writes are insufficient.

The instruction plan must be a natural accepted-task prompt, not the old six-heading checklist. It must disclose the visible command, output path, JSON schema, regenerated-output rule, source-fix intent, and externally tested recovery guarantees. It must not name shadow metadata, active-state authority selection, the replay-order defect, exact patch files/functions, or the trusted-artifact replacement strategy.

### platform_files

- path: task.toml
  role: Edition 2 metadata
- path: instruction.md
  role: natural public task prompt
- path: output_contract.toml
  role: repo-local output declaration
- path: tests/test.sh
  role: verifier entrypoint
- path: tests/test_outputs.py
  role: domain verifier
- path: solution/solve.sh
  role: oracle
- path: environment/Dockerfile
  role: build definition
- path: construction_manifest.json
  role: local authoring artifact

### task_files

- path: environment/mig_exec
  role: user-facing command that regenerates observations
- path: environment/app/main.cpp
  role: command dispatch and scenario orchestration
- path: environment/app/flow.cpp
  role: normalizes run records
- path: environment/app/flow.hpp
  role: report construction interface
- path: environment/app/core/types.cpp
  role: shared value helpers
- path: environment/app/core/types.hpp
  role: shared value objects
- path: environment/app/core/ledger.cpp
  role: fix-frontier record combination
- path: environment/app/core/ledger.hpp
  role: fix-frontier declaration
- path: environment/app/core/checks.cpp
  role: decoy/helper sanity checks
- path: environment/app/core/checks.hpp
  role: decoy/helper declarations
- path: environment/app/ops/tape.cpp
  role: fix-frontier sequence handling
- path: environment/app/ops/tape.hpp
  role: fix-frontier declaration
- path: environment/app/ops/wash.cpp
  role: sweep sequence helper
- path: environment/app/ops/wash.hpp
  role: sweep declaration
- path: environment/app/ops/probe.cpp
  role: decoy diagnostic helper
- path: environment/app/ops/probe.hpp
  role: decoy diagnostic declaration
- path: environment/app/io/packs.cpp
  role: input fixture reader
- path: environment/app/io/packs.hpp
  role: input fixture declaration
- path: environment/app/io/store.cpp
  role: fix-frontier durable entry handling
- path: environment/app/io/store.hpp
  role: fix-frontier declaration
- path: environment/app/io/catalog.cpp
  role: scenario catalog helper
- path: environment/app/io/catalog.hpp
  role: scenario catalog declaration
- path: environment/app/emit/frame.cpp
  role: fix-frontier observation framing
- path: environment/app/emit/frame.hpp
  role: fix-frontier declaration
- path: environment/app/emit/write.cpp
  role: report writer
- path: environment/app/emit/write.hpp
  role: report writer declaration
- path: environment/app/emit/archive.cpp
  role: decoy diagnostic archive writer
- path: environment/app/emit/archive.hpp
  role: decoy archive declaration
- path: environment/app/fixtures/control_sets.json
  role: local input scenarios and negative controls
- path: environment/app/fixtures/packs.json
  role: local fixture metadata
- path: environment/app/fixtures/packs.tsv
  role: local checkpoint-like fixture data
- path: environment/app/fixtures/mutations.json
  role: deterministic sequence mutations
- path: environment/app/docs/report_schema.md
  role: visible product documentation for schema and recovery guarantees
- path: environment/app/docs/operators.md
  role: operator context without solution guidance
- path: environment/app/tools/inspect.sh
  role: diagnostic command used for reproduction

### fix_frontier

- count: 4
- distribution: one core combiner, one operation sequencer, one durable entry handler, and one observation emitter across distinct package roots; no location controls more than 25% of tests.
- naming_policy: Fix-path symbols use neutral engineering names and avoid every extracted instruction noun; tests use neutral numeric IDs.
- forbidden_stems: ["migration", "harness", "workload", "checkpoint", "bundle", "replay", "cleanup", "generation", "ownership", "lineage", "artifact", "recovery", "observation", "boundary", "health"]
- helpers_policy: Co-resident helpers and decoys perform genuine diagnostics or sanity checks; no cosmetic decoys or detector-padding files.
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: ["run records", "provenance traces", "metamorphic clean-vs-rerun comparisons", "artifact digests", "idempotence checks"]
- forbidden_assertion_styles: ["boolean answer keys", "scenario-to-value truth tables", "static copied reports", "tests that only check JSON shape"]

Output-contract design rule:
- Prefer observation records, generation traces, artifact summaries, and run records.
- Tests should derive verdicts from those records.
- Do not emit named boolean verdict fields.
- Do not use scenario-to-expected truth tables in `instruction.md`.
- Exact schema fields and digest derivation rules must be visible in `instruction.md` or `environment/app/docs/report_schema.md`.

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis plus coordinated repair across local recovery state and regenerated artifacts
- collapse_risk: naming the restore boundary or trusted artifact too directly could reduce the task to replacing one source in one emitter.

### category_profile

- challenge_family: live recovery replay boundary drift with durable artifact authority mismatch
- bug_family: live recovery replay boundary drift with durable artifact authority mismatch
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: Crash/restart or recovery workflow, durability guarantee, recovery command, regenerated output path, report schema, externally visible post-recovery state, and idempotent rerun expectations.
- forbidden_instruction_leaks: Journal/checkpoint internals, shadow-vs-active authority mismatch, broken recovery phase, corrupt record, replay function, cleanup path, exact phase ordering, or patch location.
- category_specific_hardness_bar: Partial writes, replay, cleanup, idempotence, and rerun safety must coordinate across generated observations and durable local artifacts.
- category_specific_verifier_risks: Nondeterministic crash timing, one hidden snapshot, verifier trusting private internals, static report writes, and special-casing one scenario.
- coverage_role: Adds a state recovery crash-consistency profile task using migration-style replay drift, complementing the promoted config-policy reference rather than duplicating it.

### difficulty_mechanism_plan

- mechanisms: stateful_multi_step_dependencies, deceptive_but_valid_local_evidence, rollback_recovery_requirements, cross_file_cross_format_invariants, partial_observability_experiment_design
- adversarial_layers_count: 5
- fairness_guardrails: all difficulty comes from deterministic local artifacts, visible commands, and inspectable source behavior; no timing, latency, web, multi-container, or ambiguity-based hardness is used.
- mechanism: stateful_multi_step_dependencies
  placement: runner scenarios perform restore, replay, cleanup, deletion, and rerun sequences before observations are stable.
  why_model_misses_it: a model can stop at the first healthy run and miss drift that appears only after later sequences.
  fairness_guardrail: all sequences are deterministic and reproducible through the public command and local fixtures.
- mechanism: deceptive_but_valid_local_evidence
  placement: initial health records and reconstructed summaries look internally consistent while later records expose divergence.
  why_model_misses_it: surface checks encourage premature closure around the wrong authority.
  fairness_guardrail: the final verifier derives invariants from full observation traces, not hidden facts.
- mechanism: rollback_recovery_requirements
  placement: cleanup and rerun behavior must be safe after output deletion and repeated recovery.
  why_model_misses_it: narrow fixes often pass one replay but fail idempotence or negative controls.
  fairness_guardrail: the public prompt names idempotent recovery and regeneration requirements.
- mechanism: cross_file_cross_format_invariants
  placement: C++ source, JSON fixtures, visible docs, emitted observations, and construction manifest must agree.
  why_model_misses_it: single-file fixes leave fixture semantics, docs, or report framing inconsistent.
  fairness_guardrail: every externally tested schema and artifact rule has a visible home.
- mechanism: partial_observability_experiment_design
  placement: the solver must run and compare generated traces across modes to isolate the durable drift.
  why_model_misses_it: static inspection alone may identify several plausible authorities that all look locally consistent.
  fairness_guardrail: no timing, latency, network, or nondeterministic crash injection is required.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: one careful human can solve using bundled source, fixtures, docs, public command, and regenerated observations in a few hours.
- shortcut_audit: attempt static JSON writes, runner-only patches, broad state clearing, summary-only trust, test edits/deletions, and direct reward writes.
- ablation_plan: remove one layer at a time: deceptive first health, cleanup rerun, durable artifact provenance, and cross-format schema checks; each removal should make a distinct shortcut viable.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target-agent trials on the finalized single-container task.

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when every semantic and static verifier check passes; partial metric weights are for author calibration.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step task; sequential dependency is encoded inside deterministic recovery scenarios rather than milestone folders.
- local_only_data: true
- sidecar_or_protocol_notes: all sidecar-like inputs are local JSON/docs fixtures under environment; no external service, database, UI, or runtime web access.

### satisfiability_risk

- rc2_planned_name_risk: low; fix-path paths use `app/core`, `app/ops`, `app/io`, and `app/emit` with neutral symbols while instruction nouns are banned from symbols and test names.
- gx9_contract_risk: low; the output is observation-shaped and tests derive invariants from traces rather than instruction scenario-field-value tables.
- cr1_symbol_frontier_risk: low; the construction manifest predeclares four symbol-thin frontier functions across distinct roots.
- hidden_contract_risk: medium but controlled; schema, command, regenerated output rule, digest rule, and recovery guarantees must be mirrored in `instruction.md` or visible environment docs.

### actionability_plan

- verifier_command_visible: instruction.md will name `/app/environment/mig_exec --write /app/output/migration_observations.json` as the normal regeneration command.
- source_fix_intent_visible: instruction.md will state that source under `/app/environment` must be fixed so normal regeneration produces correct observations; static output writes are insufficient.
- generated_output_rule_visible: instruction.md will state tests delete `/app/output/migration_observations.json`, rerun the harness, and inspect the regenerated records.
- exact_formula_home: instruction.md and visible environment docs will define only product-level derived checks: stable record digest from ordered observations and idempotent equality across reruns; implementation formula homes stay in docs/source, not tests alone.
- schema_home: instruction.md and `environment/app/docs/report_schema.md` will define `runs`, `steps`, `records`, `artifacts`, and per-record fields such as `name`, `generation`, `owner`, `lineage`, and `evidence`.

### waiver_plan

- waivers_expected: no
- waiver_rationale: no waivers planned; naming, output-contract shape, and multi-frontier construction address expected collapse and hidden-contract pressure.

### reference_pattern

- reference_task_id: async-pipeline-premature-completion

### realism_source

- source_type: synthetic_exception
- evidence_basis: Synthesized goal-sized survivor based on real classes of live migration, checkpoint replay, and recovery-controller bugs where a superficially healthy restored workload later diverges from canonical durable state.
- upstream_or_synthetic_rationale: No specific upstream bug is being cited; the synthetic exception is justified because the minimized local harness preserves a real workflow: restore, replay, cleanup, regenerated evidence, and post-recovery validation without external infrastructure.
- minimization_preserves: The design preserves false-green surface validation, multiple plausible authorities, replay-boundary mutation, cleanup windows, durable artifacts, idempotent reruns, and generated observation reports.
- synthetic_exception_review: Required and satisfied at spec level: no invented answer-key booleans, no metaphor-only prompt, local-only deterministic data, explicit actionability plan, no planned waivers, and extra collapse scrutiny via four-frontier flipping contract.

### Failure topology
The symptom cluster spans initial restore, replay after cleanup, repeated rerun after output deletion, and later-generation record comparison. The public contract can disclose the command, report schema, idempotent regeneration, and recovery guarantees, but the solver must discover why multiple local authorities stay internally consistent until the later generation exposes divergence.

The task should be hard after disclosure because no single local change satisfies all invariants. A fix that trusts the first health record fails later-generation continuity. A fix that clears all state can break negative controls and idempotence. A fix that changes only the emitter leaves durable artifacts inconsistent. A fix that changes only replay order can still frame observations from the wrong source.

### Environment shape
The environment should look like a small single-container service repo with a command runner, a C++ source tree split into core combination, operation sequencing, local IO, report emission, fixtures, docs, and diagnostic tooling. The docs describe product behavior and schema, not implementation causes. The fixtures provide multiple deterministic local scenarios. The emitted report is regenerated by the runner and never shipped as a golden answer.

### Required artifacts
Create a standard single-step task with `instruction.md`, `task.toml`, `output_contract.toml`, `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Under `environment/`, create at least 20 non-Docker files with substantive code, docs, fixtures, and helper modules matching the shape above. Do not create milestone folders, UI assets, multi-container compose files, reviewer appendices, or task files outside the Initial Draft Commitments without amending this spec.

### Test plan
1. **`test_r01`** — runs the public command and checks initial restore and later replay observations converge for the same active workload inputs; multiple fixes can satisfy by repairing combination or sequencing.
2. **`test_r02`** — derives generation continuity from ordered records and visible artifact summaries; catches one-row health shortcuts.
3. **`test_r03`** — verifies cleanup followed by replay preserves ownership lineage and does not resurrect removed records; sets up its own scenario.
4. **`test_r04`** — verifies repeated recovery after output deletion is idempotent and produces the same digest from regenerated observations.
5. **`test_r05`** — verifies durable artifact evidence agrees with emitted records across at least two generations; catches summary-only trust.
6. **`test_r06`** — verifies negative-control workloads that never cross the replay boundary remain stable; catches broad state clearing.
7. **`test_r07`** — verifies each record's owner and lineage are internally consistent with the visible schema and source docs.
8. **`test_r10`** — verifies the public driver, schema, and output path remain intact and that static report writes are insufficient.

### Drafting guardrails
Do not name the exact broken mechanism, authority mismatch, replay phase, or patch symbols in `instruction.md`, tests, comments, fixtures, or docs. Keep all externally tested schema fields, command paths, regenerated-output behavior, and recovery guarantees visible. Avoid a per-scenario answer table, boolean verdict fields, comments near fix lines using correctional vocabulary, or path/symbol tokens that repeat instruction nouns on the fix frontier.

### Triviality Ledger

- **Writing `/app/output/migration_observations.json` directly** fails because tests delete the file and regenerate it through the public runner across multiple scenarios.
- **Changing only the command wrapper** fails because tests inspect replay, cleanup, durable artifact evidence, and later-generation records that require source behavior to agree across modules.
- **Trusting the first health report** fails because later-generation observations and artifact digests expose drift not visible in the initial row.
- **Clearing all local state globally** fails the negative-control stability checks and can lose ownership lineage.
- **Swapping one source in the emitter** fails because replay order and durable entries must also converge under rerun and cleanup sequences.
- **Reciting fixed values in instruction.md** is avoided; tests derive expected properties from visible schema, local fixtures, and generated traces.

### Per-gate Pitfall Inventory

- **RC1 / Oracle simplification**: oracle must add coordinated behavior across four modules, not delete one guard or flip one branch.
- **RC2 / Oracle predictability**: fix-path symbols avoid instruction nouns such as migration, workload, checkpoint, replay, cleanup, generation, ownership, lineage, recovery, and observation.
- **RC3 / Verifier shallowness**: tests derive generation continuity, idempotence, and provenance from records rather than checking only JSON shape.
- **RC4 / Tamper surface**: expected values are computed from visible docs and generated output, not read from mutable environment goldens.
- **RC5 / Reference artifacts**: no golden final report lives under `environment/`; fixtures are inputs, not answer files.
- **RC6 / Instruction specificity**: instruction exposes schema and recovery guarantees but omits shadow/active authority, corrupt phase, files, functions, and root cause.
- **RC7 / Oracle triviality**: planned solution changes four real code paths with enough substantive logic to exceed the hard floor.
- **CR1 / Symbol frontier**: construction manifest predeclares all oracle-touched symbols and keeps the frontier symbol-thin.
- **CR2 / Flipping contract**: four locations each control two tests, with max concentration 25%, below the 50% cap.
- **CR8 / Orchestration fanout**: runner should call public package entrypoints, not directly import all frontier symbols in one visible file.
- **GX1 / Comment leakage**: no comments near fix lines may use bug/fix/wrong/expected/correctional vocabulary.
- **GX3 / Edit distance**: solve must perform substantive multi-module logic changes, not cosmetic rewrites or unchanged heredocs.
- **GX5/GX9 / Answer recital**: no scenario-field-value table; values and verdicts are derived from observations.
- **GX8 / Test-import consistency**: any digest or domain primitive used in tests must have a visible environment or instruction/docs home.
- **GX10 / Polarity contradiction**: avoid mixed fresh/stale, valid/invalid, pass/fail wording for one scenario in one sentence.
- **Static checks / packaging**: no forbidden output/build/bin directories under environment; Dockerfile copies only committed sources.

### Initial Draft Commitments

- `tasks/live-migration-shadow-state-variant-2/instruction.md`
- `tasks/live-migration-shadow-state-variant-2/task.toml`
- `tasks/live-migration-shadow-state-variant-2/output_contract.toml`
- `tasks/live-migration-shadow-state-variant-2/solution/solve.sh`
- `tasks/live-migration-shadow-state-variant-2/tests/test.sh`
- `tasks/live-migration-shadow-state-variant-2/tests/test_outputs.py`
- `tasks/live-migration-shadow-state-variant-2/environment/Dockerfile`
- `tasks/live-migration-shadow-state-variant-2/environment/mig_exec`
- `tasks/live-migration-shadow-state-variant-2/environment/app/main.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/flow.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/flow.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/core/types.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/core/types.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/core/ledger.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/core/ledger.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/core/checks.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/core/checks.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/ops/tape.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/ops/tape.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/ops/wash.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/ops/wash.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/ops/probe.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/ops/probe.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/io/packs.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/io/packs.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/io/store.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/io/store.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/io/catalog.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/io/catalog.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/emit/frame.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/emit/frame.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/emit/write.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/emit/write.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/emit/archive.cpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/emit/archive.hpp`
- `tasks/live-migration-shadow-state-variant-2/environment/app/fixtures/control_sets.json`
- `tasks/live-migration-shadow-state-variant-2/environment/app/fixtures/packs.json`
- `tasks/live-migration-shadow-state-variant-2/environment/app/fixtures/packs.tsv`
- `tasks/live-migration-shadow-state-variant-2/environment/app/fixtures/mutations.json`
- `tasks/live-migration-shadow-state-variant-2/environment/app/docs/report_schema.md`
- `tasks/live-migration-shadow-state-variant-2/environment/app/docs/operators.md`
- `tasks/live-migration-shadow-state-variant-2/environment/app/tools/inspect.sh`
- `tasks/live-migration-shadow-state-variant-2/construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/app/core/ledger.cpp
  symbol: fold_units
  kind: function
  signature: std::map<std::string, view::Row> fold_units(const std::vector<view::Row>& items, const std::string& mark)
  purpose: Combines collected records into the intermediate map used by the harness.

- path: environment/app/ops/tape.cpp
  symbol: advance_span
  kind: function
  signature: std::vector<view::Row> advance_span(const std::vector<view::Row>& batch, const std::string& marker)
  purpose: Builds the next operation sequence from a batch of local records.

- path: environment/app/io/store.cpp
  symbol: bind_entry
  kind: function
  signature: view::Artifact bind_entry(const std::string& slot, const view::Row& payload)
  purpose: Loads and stores structured local entries used by the runner.

- path: environment/app/emit/frame.cpp
  symbol: shape_rows
  kind: function
  signature: std::vector<std::string> shape_rows(const std::string& label, const std::map<std::string, view::Row>& frame, const std::vector<std::string>& order)
  purpose: Converts intermediate maps into externally visible observation rows.
```

#### flipping_point_contract

```
locations:
  - id: F1
    path: environment/app/core/ledger.cpp
    controls_tests: [test_r01, test_r02]
  - id: F2
    path: environment/app/ops/tape.cpp
    controls_tests: [test_r03, test_r04]
  - id: F3
    path: environment/app/io/store.cpp
    controls_tests: [test_r05, test_r06]
  - id: F4
    path: environment/app/emit/frame.cpp
    controls_tests: [test_r07, test_r08]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/app/emit/archive.cpp
  kind: helper
  rhymes_with: shape_rows
  non_fix_purpose: Writes diagnostic snapshots for operator inspection outside verifier-facing observations.

- path: environment/app/core/checks.cpp
  kind: helper
  rhymes_with: fold_units
  non_fix_purpose: Performs sanity checks for local fixture rows before execution begins.

- path: environment/app/ops/probe.cpp
  kind: helper
  rhymes_with: advance_span
  non_fix_purpose: Prints operator-facing dry-run traces for manual inspection.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [migration, harness, workload, checkpoint, bundle, replay, cleanup, generation, ownership, lineage, artifact, recovery, observation, boundary, health]
```
