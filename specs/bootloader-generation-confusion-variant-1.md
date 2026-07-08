### Decision
GO — Attempt 1. Synthetic exception justified as a minimized long-horizon coherence bug: staged workloads clear early checks while promotion-time digests and coordinator-facing summaries diverge after replay-heavy windows. Construction mirrors the observation-shaped reference pattern from `async-pipeline-premature-completion` while staying on the `state_recovery_crash_consistency` profile with three distributed fix roots and a flipping-point contract.

### Metadata
- version: 2
- Task name: bootloader-generation-confusion-variant-1
- Title: Bootloader generation drift
- Category: software-engineering
- Languages: ["python", "bash"]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: ["tool_specific"]
- Tags: ["recovery", "replay", "staging", "lineage", "coherence"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Operators report that staged workloads pass early integrity checks, then later promotion cycles disagree: packaged digests no longer line up with what the live coordinator materializes, promotion-tail generations drop out of replay spans, and cross-window comparisons drift after resume-heavy maintenance. The solver must repair Python sources under `/app/environment` so `/app/output/recovery_transcript.json` is always produced by the shipped runner after tests delete it, never by static writes.

The instruction plan must read like a natural bug report:
- What is wrong: intermittent agreement during bring-up followed by late drift across replay windows and promotion tails.
- What to change: fix `/app/environment` sources; bypassing the runner or hand-writing the transcript is insufficient.
- Where to look: directory-level scope only — journal ingest, coordinator merge paths, tail replay application, and the bundled contract docs under `/app/environment`.
- What the verifier checks: the visible command, regenerated transcript path, JSON observation shape, cross-phase digest chain rules, idempotent reruns, cleanup-window metamorphic behavior, and negative controls against stale hand-written outputs.
- What is not sufficient: editing tests, hardcoding transcript values, wrapper-only edits, or wiping all state without preserving required invariants.

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

- path: environment/runner.py
  role: ships repro command and regenerates recovery transcript
- path: environment/wal_slots/first_core.py
  role: fix-frontier digest builder
- path: environment/wal_slots/cold_mirror.py
  role: decoy cold-cache mirror
- path: environment/wal_slots/__init__.py
  role: package init
- path: environment/co_emitters/mid_slice.py
  role: fix-frontier coordinator merge
- path: environment/co_emitters/idle_prune.py
  role: decoy scratch pruner
- path: environment/co_emitters/__init__.py
  role: package init
- path: environment/journal_apply/last_apply.py
  role: fix-frontier tail replay applier
- path: environment/journal_apply/noop_pad.py
  role: decoy archival padder
- path: environment/journal_apply/__init__.py
  role: package init
- path: environment/studio/__init__.py
  role: studio package root
- path: environment/studio/app/__init__.py
  role: studio app package
- path: environment/studio/app/entry.py
  role: scenario orchestration
- path: environment/studio/app/flow.py
  role: normalizes run records
- path: environment/studio/app/core/types.py
  role: shared value objects
- path: environment/studio/app/core/checks.py
  role: non-frontier consistency helpers
- path: environment/studio/app/tools/inspect.py
  role: diagnostic helper
- path: environment/studio/app/tools/sample_env.sh
  role: example setup
- path: environment/studio/app/docs/contract.md
  role: visible schema, digest distance rules, and command documentation
- path: environment/studio/app/docs/operators.md
  role: operational context without patch guidance
- path: environment/studio/app/fixtures/schedule.json
  role: replay schedule fixture
- path: environment/studio/app/fixtures/promotion_tails.json
  role: promotion tail fixture
- path: environment/studio/app/fixtures/digest_sources.json
  role: mixed authority fixture
- path: environment/studio/app/fixtures/cleanup_spans.json
  role: cleanup span fixture
- path: environment/studio/app/scribe/archive.py
  role: non-fix historical writer
- path: environment/studio/app/readers/basefile.py
  role: baseline reader
- path: environment/studio/app/readers/localfile.py
  role: workspace reader

### fix_frontier

- count: 4
- distribution: one module under `environment/wal_slots` for digest builder logic, one under `environment/co_emitters` for coordinator merge behavior, one flow module for binding promotion-tail generations onto emitted rows, and one under `environment/journal_apply` for tail replay application; no root owns more than half of the pytest controls under the flipping-point contract.
- naming_policy: opaque fix-path symbols declared in the construction manifest; path segments avoid instruction domain nouns.
- forbidden_stems: ["workloads", "promotions", "digests", "summaries", "fingerprints", "harness", "coordinator", "checkpoints", "windows", "bundles"]
- helpers_policy: decoys perform genuine pruning, mirroring, or archival padding; studio helpers stay off the oracle symbol table unless listed.
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: ["run records", "cross-phase transcript comparisons", "derived digest chains", "promotion-tail span binding", "idempotent rerun checks", "cleanup-window metamorphic checks"]
- forbidden_assertion_styles: ["boolean answer keys", "scenario-to-value truth tables", "static copied transcripts", "shape-only JSON asserts"]

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis coordinated across replay ordering, promotion bookkeeping, generation propagation, span-token construction, and digest authority selection
- collapse_risk: naming the exact restore boundary file, trusted digest path, or cleanup phase order collapses the task to a one-line guard

### category_profile

- challenge_family: storage_recovery_lineage
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: crash/restart and replay workflows, durability expectations, recovery command, regenerated transcript path, cross-window invariants, idempotent rerun rule, and negative controls for static writes.
- forbidden_instruction_leaks: journal layout details, exact cleanup hook ordering, shadow-versus-canonical filenames, fix-path symbols, or patch recipe.
- category_specific_hardness_bar: partial writes, replay, cleanup, and rerun safety must coordinate; deleting one stale cache file is insufficient.
- category_specific_verifier_risks: nondeterministic crash timing, hidden snapshot expectations, verifier coupling to private internals.
- coverage_role: adds a generation-confusion variant under recovery profile distinct from single-phase journaling-only tasks.

### satisfiability_risk

- rc2_planned_name_risk: low; neutral roots and opaque symbols with noun ban on fix path.
- gx9_contract_risk: low; instruction avoids enumerating per-scenario expected field triples; tests derive from transcripts.
- cr1_symbol_frontier_risk: medium; three declared frontier symbols should keep bodies thin with helpers in sibling modules.
- hidden_contract_risk: low; every tested field and digest rule must be mirrored in `environment/studio/app/docs/contract.md` and cited at a high level from the public prompt.

### actionability_plan

- verifier_command_visible: instruction names the `python3` invocation of `/app/environment/runner.py` that tests use to regenerate `/app/output/recovery_transcript.json`.
- source_fix_intent_visible: instruction states fixes must live under `/app/environment` and flow through the runner, not hand-written outputs.
- generated_output_rule_visible: instruction states tests delete `/app/output/recovery_transcript.json` and require regeneration through the normal command.
- exact_formula_home: digest distance, window overlap, promotion-generation, and replay-span rules live in `environment/studio/app/docs/contract.md` and are summarized in instruction without per-scenario answer tables.
- schema_home: transcript top-level schema documented in contract.md and echoed descriptively in instruction.

### waiver_plan

- waivers_expected: no
- waiver_rationale: no waivers planned; synthetic exception review covers realism and verifier shape so checker pressure stays design-time.

### reference_pattern

- reference_task_id: async-pipeline-premature-completion

### realism_source

- source_type: synthetic_exception
- evidence_basis: Step-1 intake described a synthesized goal-sized Option B survivor seed without an attached upstream ticket.
- upstream_or_synthetic_rationale: Compresses recurring industry incidents where staging probes agree while promotion-time digests disagree after replay-heavy maintenance.
- minimization_preserves: multi-authority confusion, destructive replay windows, and late-generation divergence without a proprietary vendor tree.
- synthetic_exception_review: profile `state_recovery_crash_consistency` chosen; observation-shaped outputs avoid boolean verdict fields; formulas homed in visible contract.md; decoys must do real non-fix work; waivers not anticipated.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, rollback_recovery_requirements, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, stateful_multi_step_dependencies
- adversarial_layers_count: 5
- fairness_guardrails: difficulty comes from deterministic replay harnesses and locally discoverable authorities, not timing thresholds or ambiguous requirements.
- mechanism: false_green_intermediate_states
  placement: coordinator merge path plus schedule fixtures
  why_model_misses_it: early probes agree while later promotion phases expose stale coordinator slices.
  fairness_guardrail: instruction describes the two-phase disagreement without naming the mistaken branch.
- mechanism: rollback_recovery_requirements
  placement: tail replay applier and harness reruns
  why_model_misses_it: tail replay mutates evidence used by later validation unless ordering is coordinated.
  fairness_guardrail: deterministic injected schedules and idempotent rerun checks remove flake.
- mechanism: deceptive_but_valid_local_evidence
  placement: digest builder versus studio summaries
  why_model_misses_it: locally consistent summaries disagree with canonical artifact bytes.
  fairness_guardrail: both surfaces exist in-repo; solver picks the correct authority from behavior.
- mechanism: cross_file_cross_format_invariants
  placement: JSON transcripts plus on-disk fixture bytes and promotion-tail fixtures
  why_model_misses_it: digest chain must align bytes, coordinator entries, promotion generations, and tail replay markers simultaneously.
  fairness_guardrail: contract.md defines cross-format checks referenced by instruction.
- mechanism: stateful_multi_step_dependencies
  placement: runner-driven multi-phase scenario driver
  why_model_misses_it: later phases depend on mutated state from earlier replay and cleanup windows.
  fairness_guardrail: harness exposes deterministic phase labels inside transcripts for debugging.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: a storage-savvy engineer can trace two disagreeing authorities in under two hours using only bundled sources.
- shortcut_audit: static JSON paste, test-side-only digest math, broad env wipes, wrapper-only edits, and reward-file forgery.
- ablation_plan: remove tail replay coupling, remove digest authority swap, or freeze coordinator summaries and expect interpretable ease-ups while subsets fail.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent on this harness class

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt reads 1 only when every pytest case passes after fresh transcript regeneration.

### subtype_milestone_plan

- subcategories: ["tool_specific"]
- milestone_count: 0
- sequential_dependency: single-step task; dependencies are encoded as stateful command and transcript invariants.
- local_only_data: true
- sidecar_or_protocol_notes: fixtures live under `environment/studio/app/data`; no network or external APIs.

### Failure topology
Symptoms arrive late: early phases show coherent staged behavior, then promotion tails and replay windows disagree on durable lineage. Multiple authorities remain locally plausible—short-lived summaries, tail replay markers, and verifier-facing digest material—so a narrow fix can still produce false-green intermediate transcripts until cross-phase invariants are satisfied together.

### Environment shape
Ship a small Python service layout: a top-level runner, three sibling package roots for digest building, coordinator emission, and tail replay, plus a `studio` subtree for fixtures, docs, orchestration helpers, and archival utilities. Supporting docs carry the public numeric and schema rules; data JSON drives deterministic schedules.

### Required artifacts
Create a standard single-step task with `instruction.md`, `task.toml`, `output_contract.toml`, `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Populate at least twenty non-Docker files under `environment/` with substantive code, docs, and fixtures matching the topology above.

### Test plan
1. **`test_t01_alpha_phase_byte_lines`** — first-phase byte-line closure after regeneration.
2. **`test_t02_beta_phase_byte_lines`** — beta-phase byte-line closure to block one-file shortcuts.
3. **`test_t03_anchor_heads`** — coordinator-visible anchors align with canonical bytes per contract.md.
4. **`test_t04_lane_trace`** — transcript emission includes correct cross-phase markers after destructive replay steps.
5. **`test_t05_rerun_stability`** — idempotent reruns converge without hand-written transcripts surviving deletion.
6. **`test_t06_slot_crosscut`** — cleanup-window metamorphic check catches summaries that disagree with digests after tail replay.
7. **`test_t07_tail_generations`** — generation fixture values survive through emitted rows without a static transcript shortcut.
8. **`test_t08_replay_span_heads`** — replay span tokens bind phase, artifact, generation, global tail order, and emitted digest.

### Drafting guardrails
Do not place instruction nouns on fix-path symbols, directory names, or test function names. Keep every externally tested field, digest rule, and command visible in instruction or `environment/studio/app/docs/contract.md`, but never emit scenario-to-value truth tables or name the mistaken branch as the patch recipe.

### Triviality Ledger

- **Hand-writing `/app/output/recovery_transcript.json`** fails because tests delete it and require regeneration through the shipped runner across multiple phases.
- **Wrapper-only edits** fail because transcript slices must reflect coordinated changes in digest builder, coordinator merge, generation propagation, and tail replay modules.
- **Deleting one shadow mirror file** fails decoy checks and does not repair canonical digest selection for verifier-visible material.
- **Broad global wipes** fail idempotence and anchor-head checks that require nuanced state retention across reruns.
- **Reciting expected digest values in instruction** is forbidden; tests derive expectations from visible rules plus emitted transcripts.

### Per-gate Pitfall Inventory

- **RC1 / Oracle simplification**: oracle must coordinate digest authority, coordinator merge, promotion-tail propagation, and tail replay ordering, not flip one boolean flag.
- **RC2 / Oracle predictability**: fix-path code avoids instruction nouns workloads, promotions, digests, summaries, fingerprints, harness, coordinator, checkpoints, windows, bundles.
- **RC3 / Verifier shallowness**: assertions compare derived digest chains and cross-phase markers, not JSON shape alone.
- **RC4 / Tamper surface**: expected values come from contract rules plus observed transcripts, not mutable golden outputs under `environment/`.
- **RC5 / Reference artifacts**: fixtures are inputs; no golden transcript ships as a fixed answer file.
- **RC6 / Instruction specificity**: symptoms-only; no root-cause sentences or file-level patch map.
- **RC7 / Oracle triviality**: oracle touches four behavioral roots with substantive coordinated edits.
- **CR1 / Symbol frontier**: construction manifest lists every oracle-touched symbol explicitly.
- **CR8 / Orchestration fanout**: runner imports public entrypoints rather than inlining all frontier symbols in one file.
- **GX9 / Answer recital**: no scenario-key-value windows; instruction stays descriptive.
- **GX10 / Polarity contradiction**: avoid pairing stale/fresh or allow/deny polarities for one scenario in one sentence.
- **Static checks / packaging**: never place cache or build-style directory names (the usual shell-artifact folder names) directly under `environment/`; Dockerfile copies only committed sources.

### Initial Draft Commitments

- `tasks/bootloader-generation-confusion-variant-1/instruction.md`
- `tasks/bootloader-generation-confusion-variant-1/task.toml`
- `tasks/bootloader-generation-confusion-variant-1/output_contract.toml`
- `tasks/bootloader-generation-confusion-variant-1/construction_manifest.json`
- `tasks/bootloader-generation-confusion-variant-1/solution/solve.sh`
- `tasks/bootloader-generation-confusion-variant-1/tests/test.sh`
- `tasks/bootloader-generation-confusion-variant-1/tests/test_outputs.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/Dockerfile`
- `tasks/bootloader-generation-confusion-variant-1/environment/runner.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/wal_slots/__init__.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/wal_slots/first_core.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/wal_slots/cold_mirror.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/co_emitters/__init__.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/co_emitters/mid_slice.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/co_emitters/idle_prune.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/journal_apply/__init__.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/journal_apply/last_apply.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/journal_apply/noop_pad.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/__init__.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/__init__.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/entry.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/flow.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/core/types.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/core/checks.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/tools/inspect.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/tools/sample_env.sh`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/docs/contract.md`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/docs/operators.md`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/fixtures/schedule.json`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/fixtures/promotion_tails.json`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/fixtures/digest_sources.json`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/fixtures/cleanup_spans.json`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/scribe/archive.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/readers/basefile.py`
- `tasks/bootloader-generation-confusion-variant-1/environment/studio/app/readers/localfile.py`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/wal_slots/first_core.py
  symbol: n_quench_u
  kind: function
  signature: n_quench_u(ctx, ledger, probe)
  purpose: Builds digest-facing records from mixed inputs before promotion.

- path: environment/studio/app/flow.py
  symbol: _ambient_tail_gen
  kind: function
  signature: _ambient_tail_gen(...)
  purpose: Supplies generation metadata for row records when phase data is materialized.

- path: environment/studio/app/flow.py
  symbol: entries_for_phase
  kind: function
  signature: entries_for_phase(root, phase, dig)
  purpose: Materializes phase entries and carries generation metadata into row records.

- path: environment/studio/app/flow.py
  symbol: load_schedule
  kind: function
  signature: load_schedule(root)
  purpose: Loads schedule data for local operator helpers outside the verifier path.

- path: environment/co_emitters/mid_slice.py
  symbol: n_stitch_v
  kind: function
  signature: n_stitch_v(ctx, slices, cursor)
  purpose: Merges coordinator-visible slices after partial replay.

- path: environment/journal_apply/last_apply.py
  symbol: n_bind_w
  kind: function
  signature: n_bind_w(ctx, tail, staging)
  purpose: Applies tail replay mutations and cleanup side effects.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/wal_slots/first_core.py
    controls_tests: [test_t01_alpha_phase_byte_lines, test_t02_beta_phase_byte_lines]
  - id: B
    path: environment/co_emitters/mid_slice.py
    controls_tests: [test_t03_anchor_heads]
  - id: C
    path: environment/journal_apply/last_apply.py
    controls_tests: [test_t04_lane_trace, test_t05_rerun_stability, test_t06_slot_crosscut, test_t08_replay_span_heads]
  - id: D
    path: environment/studio/app/flow.py
    controls_tests: [test_t07_tail_generations, test_t08_replay_span_heads]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/co_emitters/idle_prune.py
  kind: module
  rhymes_with: n_stitch_v
  non_fix_purpose: Prunes unrelated scratch slices for diagnostics only.

- path: environment/wal_slots/cold_mirror.py
  kind: helper
  rhymes_with: n_quench_u
  non_fix_purpose: Maintains cold-cache mirrors that never feed the verifier path.

- path: environment/journal_apply/noop_pad.py
  kind: module
  rhymes_with: n_bind_w
  non_fix_purpose: Pads tail records for archival exports not consulted by tests.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [workloads, promotions, digests, summaries, fingerprints, harness, coordinator, checkpoints, windows, bundles]
```
