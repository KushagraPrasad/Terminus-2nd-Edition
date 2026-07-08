### Decision
GO — Attempt 1. Synthetic-exception restart-consistency task with three distributed roots (replay window, vault mirror selection, writer digests), observation-shaped transcripts, flipping contract at 33% concentration each, and reference calibration to `layered-policy-reload-drift` for verifier discipline without cloning its policy domain.

### Metadata
- version: 2
- Task name: device-node-lineage-mismatch-variant-1
- Title: Planner generation drift
- Category: software-engineering
- Task shape: repair_existing_system
- Languages: ["python", "bash"]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: ["restart", "replay", "digest", "control-plane", "idempotence"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Operators run a deterministic transcript runner that rebuilds a JSON transcript after simulated restarts and replayed sequences. A bug report says some runs pass early surface checks yet later waves show crossed material when the same pipeline is rerun across replay boundaries. The solver must fix source under `/app/environment` so the normal command regenerates `/app/output/wave_transcript.json` (tests delete it first). Instruction stays symptoms-only; digest linkage, envelope identities, idempotence reruns, and transcript schema are documented in `environment/app/docs/wave_contract.md` and summarized at a high level in `instruction.md` without naming the defective branch.

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
  role: regenerates wave transcript JSON
- path: environment/app/__init__.py
  role: package marker
- path: environment/app/entry.py
  role: command dispatch and scenario orchestration
- path: environment/app/flow.py
  role: normalizes run records for transcripts
- path: environment/segwin/__init__.py
  role: package marker
- path: environment/segwin/window.py
  role: fix-frontier replay window and generation tagging
- path: environment/segwin/sweep.py
  role: drain phase ordering hooks
- path: environment/segwin/shadow_alt.py
  role: decoy parallel scheduling helper
- path: environment/vault/__init__.py
  role: package marker
- path: environment/vault/mirror.py
  role: fix-frontier reconciler-facing mirror vs live record
- path: environment/vault/store.py
  role: durable envelope persistence
- path: environment/vault/ledger_sidecar.py
  role: decoy ledger helper
- path: environment/writer/__init__.py
  role: package marker
- path: environment/writer/summary.py
  role: fix-frontier external digest emission
- path: environment/writer/frame.py
  role: transcript framing helpers
- path: environment/writer/archive.py
  role: non-fix historical writer
- path: environment/app/core/__init__.py
  role: package marker
- path: environment/app/core/types.py
  role: shared value objects
- path: environment/app/core/checks.py
  role: consistency checks used by runner
- path: environment/app/readers/basefile.py
  role: fixture reader
- path: environment/app/readers/seqfile.py
  role: sequence fixture reader
- path: environment/app/data/sequences.json
  role: replay sequence fixture
- path: environment/app/data/nodes.toml
  role: node fixture
- path: environment/app/docs/wave_contract.md
  role: solver-visible transcript schema, digest rules, and command semantics
- path: environment/app/docs/operators.md
  role: operational context without patch guidance
- path: environment/app/tools/inspect.py
  role: diagnostic helper
- path: environment/app/tools/sample_env.sh
  role: example setup

### fix_frontier

- count: 3
- distribution: one module in replay window tagging, one in vault mirror selection, one in writer digest emission; each owns a distinct flipping cluster.
- naming_policy: opaque fix-path symbols per construction manifest; package directories stay generic.
- forbidden_stems: ["workloads", "validation", "generations", "reconciler", "metadata", "drain", "verifier", "replay", "boundaries", "digests"]
- helpers_policy: decoy modules perform plausible sibling work; fix-path symbols remain thin and renamed away from instruction nouns.
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: ["run transcripts", "cross-run digest identities", "metamorphic clean-vs-replay comparisons", "idempotence reruns", "artifact provenance chains"]
- forbidden_assertion_styles: ["boolean answer keys", "scenario-to-value truth tables in instruction", "tests that only assert JSON presence"]

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis across replay windows, mirror read path, and summary emission without naming the defective branch
- collapse_risk: naming the restore boundary, flipping one trust bit on summaries, or patching a single ordering table

### category_profile

- challenge_family: crash-consistent restarts with replay-window lineage skew and false-green summaries
- bug_family: crash-consistent restarts with replay-window lineage skew and false-green summaries
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: crash/restart workflow, durability expectation, restart command, regenerated transcript path, externally tested digest and idempotence behavior summarized without causal patch hints.
- forbidden_instruction_leaks: journal internals, exact broken phase, mirror function names, sweep ordering recipe, or which module ignores the durable envelope.
- category_specific_hardness_bar: partial writes, replay, overlap windows, idempotent reruns, and verifier-visible digest provenance must stay aligned after disclosure.
- category_specific_verifier_risks: nondeterministic crash injection, hidden golden digests, tests that read private vault internals instead of public transcripts.
- coverage_role: Adds a synthetic-exception restart-consistency task with multi-authority skew, complementing filesystem reconstruction tasks and policy-precedence references.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, rollback_recovery_requirements, cross_file_cross_format_invariants, deceptive_but_valid_local_evidence
- adversarial_layers_count: 4
- fairness_guardrails: difficulty comes from deterministic state, documented formulas, and verifier-derived observations rather than latency thresholds or hidden requirements.
- mechanism: false_green_intermediate_states
  placement: early transcript waves look healthy while later waves pull skewed lineage when drain phases overlap replay.
  why_model_misses_it: models stop after the first passing surface check without chaining reruns.
  fairness_guardrail: failing behavior is visible through the documented command and transcript fields.
- mechanism: rollback_recovery_requirements
  placement: restart and replay scenarios require idempotent merges without clobbering durable envelopes.
  why_model_misses_it: a shortcut flush fixes one rerun but breaks another scenario.
  fairness_guardrail: commands and fixtures are deterministic with seeded ordering.
- mechanism: cross_file_cross_format_invariants
  placement: JSON transcripts, TOML fixtures, and vault byte records must agree on digest linkage.
  why_model_misses_it: editing one format leaves orphans elsewhere.
  fairness_guardrail: cross-format rules are documented in wave_contract.md.
- mechanism: deceptive_but_valid_local_evidence
  placement: mirror path returns consistent short-term answers that disagree with durable store after replay.
  why_model_misses_it: local reads look coherent so the mirror is mistaken for truth.
  fairness_guardrail: both paths are real code paths discoverable via reading modules.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: one careful human can trace three roots using transcripts and docs within a few hours.
- shortcut_audit: watch for static JSON writes, digest hardcoding, test edits, NOP oracle gaming.
- ablation_plan: drop mirror fix alone, drop writer fix alone, drop segwin window fix alone to show partial failures.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent on identical Harbor harness

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt equals 1 only when every required semantic test passes in test_outputs.py.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step task; ordering is expressed via stateful command sequences inside tests.
- local_only_data: true
- sidecar_or_protocol_notes: all fixtures and transcripts are local; no network or multi-container services.

### satisfiability_risk

- rc2_planned_name_risk: low; roots split segwin, vault, writer with neutral directory tokens.
- gx9_contract_risk: medium; instruction must disclose transcript fields and digest rules as derivations, not per-row expected literals.
- cr1_symbol_frontier_risk: low; manifest caps fix-path fan-in and pairs co-resident helpers explicitly.
- hidden_contract_risk: medium; every digest field, rerun command, and envelope rule must be mirrored into instruction.md or environment docs.

### actionability_plan

- verifier_command_visible: instruction.md names the python runner that writes the transcript path and the pytest entry the harness uses.
- source_fix_intent_visible: instruction.md states /app/environment source must be repaired so the normal pipeline regenerates outputs.
- generated_output_rule_visible: instruction.md states tests delete the transcript and rerun generation across crash/restart scenarios.
- exact_formula_home: digest linkage formulas and envelope identities live in environment/app/docs/wave_contract.md and are summarized without patch steps in instruction.md.
- schema_home: top-level transcript schema (runs, waves, envelope references, digest records) documented in wave_contract.md and echoed at a high level in instruction.md.

### waiver_plan

- waivers_expected: no
- waiver_rationale: no waivers planned; synthetic pattern stays inside standard collapse and output-contract policy.

### reference_pattern

- reference_task_id: layered-policy-reload-drift

### realism_source

- source_type: synthetic_exception
- evidence_basis: No single upstream CVE or public patch; distilled from operator reports about control-plane managers that reconcile against stale mirrors and accept summary digests.
- upstream_or_synthetic_rationale: Exception justified because the seed encodes a recurring control-plane class (post-restart false greens) while remaining fully local and evidence-anchored.
- minimization_preserves: Delayed symptom after early mutation, multiple internally consistent authorities, replay ordering effects, and verifier trust in the wrong surface.
- synthetic_exception_review: Category profile state_recovery_crash_consistency applied; instruction stays symptoms-only; output contract uses observation transcripts not boolean verdict maps; discovery budget names three non-obvious code obligations; waivers not used to bypass fairness.

### Failure topology
Symptoms arrive late: early transcript waves look acceptable, then later waves expose crossed material after operators rerun the pipeline across replay boundaries. Multiple authorities stay locally coherent—reconciler-facing views, refreshed live records, and externally consumed digests—so naive patches that trust the first green surface fail deeper reruns. Hardness survives honest disclosure because digest rules live in public docs while the bug is which authority feeds the verifier when drain phases overlap.

### Environment shape
Ship a small Python service layout: a runner that writes transcripts, packages split into segwin timing, vault persistence, and writer emission, plus readers, fixtures, and operator-facing docs. Decoy helpers live beside fix paths but stay off the oracle frontier per manifest.

### Required artifacts
Create a standard single-step task with `instruction.md`, `task.toml`, `output_contract.toml`, `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Under `environment/`, deliver 26+ non-Docker files matching `task_files` and `Initial Draft Commitments`.

### Test plan
1. **`test_tseq_a`** — ordered replay sequence A: checks digest linkage across waves after restart; fails if mirror-only shortcut ignores durable envelopes.
2. **`test_tseq_b`** — ordered replay sequence B: different interleaving; catches ordering assumptions baked into one helper.
3. **`test_idempo_twice`** — reruns the runner twice with identical inputs; requires idempotent transcript merge without duplicate envelope references.
4. **`test_digest_chain`** — derives expected digest records from public rules in wave_contract.md plus observed vault bytes; blocks static JSON lifts.
5. **`test_restore_twice`** — simulates back-to-back restarts with overlapping drain phases; fails if the drain window drops refreshed live identifiers.
6. **`test_fork_paths_compare`** — compares parallel scenario branches inside one transcript; catches writer summaries that disagree with store-backed envelopes for the same wave.

### Drafting guardrails
Keep symptoms and externally tested rules in honest vocabulary, but ban instruction nouns on fix-path symbols, test function names, and package path tokens that grep-collapse to the bug. Do not put per-scenario answer tables in instruction.md. Do not name `op_a`, `reconcile_b`, or `phase_c` in instruction prose.

### Triviality Ledger

- **Hand-writing `/app/output/wave_transcript.json`** fails because tests delete and regenerate it through the runner across scenarios.
- **Mirror-only trust flip** fails `test_digest_chain` and `test_restore_twice` when envelopes disagree with summaries after overlap.
- **Global cache wipe** fails idempotence and fork-path invariants that require nuanced invalidation.
- **Editing only `sweep.py`** fails replay tagging tests that depend on coordinated window and writer behavior.
- **Reciting literals in instruction.md** is forbidden; tests derive expectations from documented formulas plus observed artifacts.

### Per-gate Pitfall Inventory

- **RC1 / oracle simplification**: oracle must touch three behavioral files with coordinated logic, not one heredoc replacement.
- **RC2 / grep resistance**: keep instruction noun tokens out of fix-path code symbols and planned test names; verify with collapse grep pass after build.
- **RC6 / instruction audit**: maintain symptoms-only repair prose; put formulas only in wave_contract.md.
- **RC7–RC8 / oracle size and symbol fan-in**: spread real logic across window, mirror, and writer; avoid one mega-file owning every symbol.
- **CR1–CR2 / symbol frontier and flipping**: honor construction manifest symbol table and flipping subsets exactly.
- **CR7–CR9 / contract helpers**: keep derivation implementations in env, not only in tests.
- **GX1 / comment leaks**: no bug/fix vocabulary in env comments near oracle edits.
- **GX5–GX6 / instruction-test overlap and causal density**: avoid mirroring test keys in instruction; limit causal connective stacking in symptoms prose.
- **GX9–GX10 / answer tables and polarity traps**: use observation records; never bind both polarities of one status to a single scenario sentence.
- **GX3 / edit distance**: plan oracle with substantive multi-site coordination, not padding.
- **Static / packaging gates**: ensure Dockerfile provides python3 for runner and tests.

### Initial Draft Commitments

- environment/runner.py
- environment/app/__init__.py
- environment/app/entry.py
- environment/app/flow.py
- environment/segwin/__init__.py
- environment/segwin/window.py
- environment/segwin/sweep.py
- environment/segwin/shadow_alt.py
- environment/vault/__init__.py
- environment/vault/mirror.py
- environment/vault/store.py
- environment/vault/ledger_sidecar.py
- environment/writer/__init__.py
- environment/writer/summary.py
- environment/writer/frame.py
- environment/writer/archive.py
- environment/app/core/__init__.py
- environment/app/core/types.py
- environment/app/core/checks.py
- environment/app/readers/basefile.py
- environment/app/readers/seqfile.py
- environment/app/data/sequences.json
- environment/app/data/nodes.toml
- environment/app/docs/wave_contract.md
- environment/app/docs/operators.md
- environment/app/tools/inspect.py
- environment/app/tools/sample_env.sh
- instruction.md
- task.toml
- output_contract.toml
- tests/test.sh
- tests/test_outputs.py
- solution/solve.sh
- environment/Dockerfile
- construction_manifest.json

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/segwin/window.py
  symbol: op_a
  kind: function
  signature: op_a(ctx, phase_id, seq_bundle)
  purpose: Computes generation tagging across replay segments for downstream readers.
- path: environment/vault/mirror.py
  symbol: reconcile_b
  kind: function
  signature: reconcile_b(store_handle, view_handle, mode_flag)
  purpose: Selects reconciler inputs for durable reads versus cached views.
- path: environment/writer/summary.py
  symbol: phase_c
  kind: function
  signature: phase_c(transcript_row, envelope_bytes, policy_id)
  purpose: Builds externally visible digest records for verifier consumption.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/segwin/window.py
    controls_tests: [test_tseq_a, test_tseq_b]
  - id: B
    path: environment/vault/mirror.py
    controls_tests: [test_idempo_twice, test_digest_chain]
  - id: C
    path: environment/writer/summary.py
    controls_tests: [test_restore_twice, test_fork_paths_compare]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/segwin/shadow_alt.py
  kind: module
  rhymes_with: op_a
  non_fix_purpose: Provides an alternate scheduling helper used only in optional diagnostics.
- path: environment/vault/ledger_sidecar.py
  kind: helper
  rhymes_with: reconcile_b
  non_fix_purpose: Maintains an archival ledger unrelated to live mirror selection.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [workloads, validation, generations, reconciler, metadata, drain, verifier, replay, boundaries, digests]
```

### Internal Diagnostic Notes
Structured evidence attempt 1 scored 0F/0W; plateau not triggered. Evidence path: `specs/.runs/device-node-lineage-mismatch-variant-1/attempt-1-evidence.json`.
