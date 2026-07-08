### Decision
GO — Attempt 1. Constrained-build incremental-rebuild drift task with `distributed_reconciliation` profile, three-root flipping frontier, observation-shaped rebuild report, and reference calibration to `layered-policy-reload-drift` for verifier discipline without cloning its policy domain.

### Metadata
- version: 2
- Task name: checkpoint-bridge
- Title: Checkpoint bridge drift
- Category: debugging
- Task shape: constrained_build
- Languages: ["cpp", "bash"]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: ["incremental-build", "reconciliation", "replay", "checkpoints", "distributed-systems", "observability"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
You maintain an incremental rebuild bridge that synchronizes checkpointed artifact trees with durable ledger metadata inside a single-container coordinator. Run `/app/environment/exec/run_cycle.sh` to regenerate `/app/output/rebuild_report.json` after scripted restart and partial replay sequences driven by local fixtures.

The public contract requires that intermediate health summaries must not be treated as final proof: generation counters, tombstone maps, and cross-format span digests must agree across a single process restart boundary and through rollback phases documented in the field guide. Repair sources under `/app/environment` so every verifier scenario deletes the report, reruns the driver, and observes consistent run records, wave entries, and derived linkage tags. Static JSON writes, wrapper-only edits, and test changes do not satisfy the task.

Formulas, CLI flags, span digest rules, and the observation schema are defined in `environment/docs/field_guide.md` and `environment/schemas/report_fragments/`. The instruction states acceptance behavior and externally tested invariants without naming which subsystem is authoritative, which merge ordering applies, or how generation state must be cleared across boundaries.

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

- path: environment/exec/run_cycle.sh
  role: driver entrypoint invoked by tests
- path: environment/CMakeLists.txt
  role: build definition for cycle_run
- path: environment/c7k/p1m.cpp
  role: fix-frontier generation tagging across boundaries
- path: environment/c7k/p1m.hpp
  role: generation tagging header
- path: environment/c7k/decoy_h1.cpp
  role: decoy batching helper
- path: environment/m2p/q4n.cpp
  role: fix-frontier canonical surface selection among competing artifact views
- path: environment/m2p/q4n.hpp
  role: surface selection header
- path: environment/m2p/decoy_h2.cpp
  role: decoy merge toy helper
- path: environment/w9n/s2t.cpp
  role: fix-frontier row assembly and cross-format digest emission
- path: environment/w9n/s2t.hpp
  role: row assembly header
- path: environment/w9n/frame.cpp
  role: report framing helpers
- path: environment/w9n/frame.hpp
  role: report framing header
- path: environment/w9n/decoy_h3.cpp
  role: decoy writer lane
- path: environment/driver/entry.cpp
  role: cycle_run main and CLI parsing
- path: environment/driver/flow.cpp
  role: scenario orchestration
- path: environment/driver/flow.hpp
  role: flow header
- path: environment/tooling/seq_tool.py
  role: CLI helper for sequence permutations
- path: environment/tooling/merge_tool.py
  role: CLI helper for merge windows
- path: environment/docs/field_guide.md
  role: solver-visible formulas, CLI semantics, and report schema
- path: environment/docs/ops_notes.md
  role: operational context without patch guidance
- path: environment/schemas/report_fragments/run.schema.json
  role: JSON schema for run records
- path: environment/schemas/report_fragments/wave.schema.json
  role: JSON schema for wave entries
- path: environment/schemas/durable_row.schema.json
  role: durable row fragment schema
- path: environment/fixtures/window_a.json
  role: first replay window fixture
- path: environment/fixtures/window_b.json
  role: second replay window fixture
- path: environment/fixtures/pr_window.json
  role: partial replay stress fixture
- path: environment/fixtures/rb_policy.json
  role: rollback phase parameters
- path: environment/fixtures/acct_baseline.json
  role: durable accounting baseline
- path: environment/fixtures/alt_view.json
  role: secondary artifact view inputs
- path: environment/fixtures/v9_markers.json
  role: regen marker patterns for verifier
- path: environment/logging/l7_format.txt
  role: log line format reference
- path: environment/logging/l7_samples.log
  role: example log samples
- path: environment/etc/service.env
  role: non-secret driver defaults
- path: environment/etc/version.txt
  role: pinned tool version string

### fix_frontier

- count: 3
- distribution: one module under `environment/c7k/` for generation tagging, one under `environment/m2p/` for canonical surface selection, one under `environment/w9n/` for cross-format row assembly; decoys colocated without sharing symbols.
- naming_policy: opaque stems and short alphanumeric filenames; fix-path symbols and path components avoid instruction domain nouns listed in the construction manifest.
- forbidden_stems: [incremental, rebuild, bridge, checkpoint, coordinator, ledger, tombstone, generation, counters, spans, digests, restart, boundary, rollback, health, summaries, invariants, replay, artifacts, linkage, waves]
- helpers_policy: decoys perform credible adjacent work; fix symbols stay thin and split across files per manifest.
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [trace-derived numeric bands, cross-run row equality on derived fields, regen fingerprint checks, idempotent rerun counters, metamorphic comparisons across windows]
- forbidden_assertion_styles: [scenario-key-value boolean tables, raw truth bits without observations, instruction-only literals not homed in env/docs]

### task_shape

- type: constrained_build
- instruction_framing: constraint-complete
- hardness_source: design search across interacting rebuild authorities under disclosed acceptance contract
- collapse_risk: leaking exact replay ordering bug or authoritative artifact path collapses task to one-file conditional flip

### category_profile

- challenge_family: incremental_rebuild_drift
- profile_name: distributed_reconciliation
- allowed_instruction_disclosures: conflicting authority behavior class, reconciliation window semantics, cycle driver command, regenerated report path, idempotence expectation, partial replay and rollback scenario classes, externally tested digest and linkage rules summarized without patch hints.
- forbidden_instruction_leaks: canonical source choice, shadow-vs-active symbol names, cleanup ordering patch site, generation-clearing recipe, exact fix-path file names from the manifest, replay-ordering bug location.
- category_specific_hardness_bar: multiple truth surfaces (health summaries, ledger rows, tombstone maps, span digests) with idempotency and conflict lineage must interact; no single precedence table or one-file generation bump suffices.
- category_specific_verifier_risks: count-only health checks, golden merged fixture, last-write-wins shortcut, GX9 answer saturation from per-row literals.
- coverage_role: adds constrained-build coverage for incremental rebuild drift within distributed_reconciliation, distinct from config_policy_precedence references.

### satisfiability_risk

- rc2_planned_name_risk: medium — opaque package stems and noun ban reduce grep collapse; risk rises if Step 2b reintroduces descriptive directory names matching instruction vocabulary.
- gx9_contract_risk: medium — rich report rows require instruction to disclose derivation rules without co-locating scenario/key/value answer triples.
- cr1_symbol_frontier_risk: medium — three thin symbols across roots with co-resident helpers listed in task_files.
- hidden_contract_risk: low — formulas and schemas duplicated into field_guide.md and schema fragments as solver-visible homes.

### actionability_plan

- verifier_command_visible: instruction.md names `/app/environment/exec/run_cycle.sh`, `/app/output/rebuild_report.json`, and deletion/regeneration behavior.
- source_fix_intent_visible: instruction.md requires repairing C++ sources under `/app/environment`, not hand-writing the report.
- generated_output_rule_visible: instruction.md states tests remove `/app/output/rebuild_report.json` and regenerate through the normal driver.
- exact_formula_home: row delta, span digest, and window formulas live in `environment/docs/field_guide.md` and `environment/schemas/`.
- schema_home: `environment/schemas/report_fragments/*.schema.json` plus field_guide.md for nested field meanings.

### waiver_plan

- waivers_expected: no
- waiver_rationale: design avoids known never-waivable failures; expect no waivers if naming and GX6/GX9 hygiene hold during Step 2b.

### reference_pattern

- justification_if_none: No promoted reference in docs/reference_tasks/index.json matches this C++/CMake checkpoint-bridge repair; layered-policy-reload-drift is a calibration zip only (not promoted). Hardness is calibrated independently via the three-root flipping frontier and field_guide span-tag rules.

### realism_source

- source_type: synthetic_exception
- evidence_basis: Distilled from recurring build-farm and incremental-coordinator incident motifs (stale generation after restart, competing artifact views, false-green health probes) without a single upstream CVE.
- upstream_or_synthetic_rationale: Exception justified because the seed encodes a realistic distributed-reconciliation class while remaining fully local, deterministic, and evidence-anchored.
- minimization_preserves: Asymmetric authorities, delayed false greens, replay ordering effects, rollback-sensitive lineage, and regeneration-dependent verification.
- synthetic_exception_review: Profile locked to distributed_reconciliation; instruction constraint-complete but solution-open; observation-shaped output contract; discovery budget names three non-obvious code obligations; no boolean verdict maps; extra scrutiny on GX9/GX10.

### difficulty_mechanism_plan

- mechanisms: stateful_multi_step_dependencies, buried_local_constraints, rollback_recovery_requirements, cross_file_cross_format_invariants, false_green_intermediate_states
- adversarial_layers_count: 5
- fairness_guardrails: difficulty comes from deterministic fixtures, bundled docs, and verifier-derived invariants—not timing thresholds or hidden requirements.
- mechanism: stateful_multi_step_dependencies
  placement: `environment/c7k/p1m.py` plus driver replay sequences in `run_cycle.sh`
  why_model_misses_it: models patch the first passing window without chaining restart-boundary and rollback phases.
  fairness_guardrail: scenario matrix and fixtures are fully local and documented.
- mechanism: buried_local_constraints
  placement: `environment/m2p/q4n.py` selection among competing artifact views
  why_model_misses_it: locally consistent secondary views mask which surface the report must treat as authoritative.
  fairness_guardrail: field_guide states acceptance rules without naming the broken branch.
- mechanism: rollback_recovery_requirements
  placement: `environment/m2p/q4n.py` cleanup hooks with `rb_policy.json`
  why_model_misses_it: rollback reorders events so naive idempotence keys reuse stale generation tags.
  fairness_guardrail: rollback parameters are public fixtures.
- mechanism: cross_file_cross_format_invariants
  placement: `environment/w9n/s2t.py` row assembly crossing JSON rows and log span tokens
  why_model_misses_it: row math looks locally consistent while violating cross-format bindings to ledger fixtures.
  fairness_guardrail: schemas and field_guide publish cross-field obligations.
- mechanism: false_green_intermediate_states
  placement: health summary path vs durable ledger path in driver orchestration
  why_model_misses_it: agents stop after intermediate summaries pass without proving later-wave linkage.
  fairness_guardrail: instruction explicitly warns summaries are not final proof; traces expose both horizons.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: engineer can diff two report generations after scripted replays and spot inconsistent lineage keys without reading tests.
- shortcut_audit: watch static JSON writes, test-only shims, broad cache wipes, and single-location reverts that clear one symptom class.
- ablation_plan: drop row assembly checks, drop regeneration requirement, or drop replay sequencing separately; each should ease agent success disproportionately if mechanisms matter.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent trials per repo calibration defaults.

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when every required semantic test passes; partial metric reasoning is used for author calibration.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step task; dependencies encoded as stateful command/output invariants.
- local_only_data: true
- sidecar_or_protocol_notes: no auxiliary databases; all data under `environment/fixtures` with local JSON and logs only.

### Failure topology
Symptoms cluster around incremental rebuild drift: intermediate health summaries report success while generation counters, tombstone maps, and cross-format span digests disagree after a single restart boundary and when rollback phases overlap partial replay windows. Catalog slices, ledger rows, and secondary artifact views can each look self-consistent in isolation yet fail cross-surface linkage in later waves. Hardness survives honest disclosure because digest and window rules live in public docs while the solver must discover which authority feeds the report when drain phases overlap replay boundaries.

### Environment shape
Ship a small C++ coordinator layout: opaque packages `c7k` (generation tagging), `m2p` (surface selection), `w9n` (row assembly), a `driver` entrypoint built as `cycle_run`, an `exec` shell driver, `docs` for formulas, `fixtures` for deterministic windows, `schemas` for JSON fragments, `tooling` CLIs, and logging samples. Decoys sit beside frontier modules without sharing their symbols.

### Required artifacts
Create a standard single-step task with `instruction.md`, `task.toml`, `output_contract.toml`, `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Under `environment/`, create at least 20 non-Docker files matching the shape above, plus `construction_manifest.json` at the task root mirroring the blocking manifest in this spec.

### Test plan
1. **`test_tseq_alpha`** — first ordered sequence: checks derived linkage across waves after simulated restart; fails if mirror-only shortcut ignores durable accounting rows.
2. **`test_tseq_beta`** — second interleaving: catches ordering assumptions baked into one helper.
3. **`test_idempo_twice`** — reruns the driver twice with identical inputs; requires idempotent report merge without duplicate span references.
4. **`test_digest_chain`** — derives expected digest records from public rules in field_guide.md plus observed durable-store bytes; blocks static JSON lifts.
5. **`test_restore_overlap`** — overlapping rollback phases; fails if generation tags survive one boundary incorrectly.
6. **`test_fork_branch`** — compares parallel scenario branches inside one report; catches row assembly that disagrees with store-backed spans for the same wave.

### Drafting guardrails
Keep acceptance behavior and externally tested rules in honest vocabulary, but ban instruction nouns on fix-path symbols, test function names, and package path tokens that grep-collapse to the bug. Do not put per-scenario answer tables in instruction.md. Do not name manifest symbols (`fn_k3`, `fn_r8`, `fn_x5`) in instruction prose.

### Triviality Ledger

- **Hand-writing `/app/output/rebuild_report.json`** fails because tests delete the file and regenerate it through the driver for multiple replay permutations.
- **Wrapper-only edits** fail because generation tagging, surface selection, and row assembly each gate distinct flipping subsets.
- **Broad global cache wipes** fail idempotent rerun and fork-branch invariants that require nuanced invalidation.
- **Patching only fixtures** fails because the bug lives in source reconciliation behavior, not seeded numbers alone.
- **Reciting answer triples in instruction.md** is forbidden; tests derive expectations from visible formulas plus emitted observations.
- **Trusting health summaries alone** fails later-wave linkage tests that require durable ledger and span agreement.

### Per-gate Pitfall Inventory

- **RC1 / Oracle simplification**: oracle must coordinate semantics across three modules, not one heredoc replacement.
- **RC2 / Oracle predictability**: keep opaque stems; ban instruction nouns on the fix path per manifest tokens.
- **RC3 / Verifier shallowness**: assert cross-window and cross-surface relations, not JSON presence alone.
- **RC4 / Tamper surface**: expected values derive from visible docs/schemas and emitted rows, not hidden goldens.
- **RC5 / Reference artifacts**: fixtures are inputs only; no pre-baked report answers under `environment/`.
- **RC6 / Instruction specificity**: constraint-complete acceptance contract without patch sites or algorithm recipe.
- **RC7 / Oracle triviality**: oracle must include substantive multi-file coordination clearing GX3 floors.
- **CR1 / Symbol frontier**: construction manifest predeclares all oracle-touched symbols.
- **CR8 / Orchestration fanout**: driver imports public package surfaces, not every frontier symbol from one file.
- **GX9 / Answer recital**: forbid co-located scenario/key/value windows; keep values derivable from observations.
- **GX10 / Polarity contradiction**: avoid both polarities of one status word for a single scenario sentence.
- **Static checks / packaging**: forbid cache or build trees under `environment/`; Dockerfile provides C++ toolchain for driver and tests invoke pytest via test.sh.

### Initial Draft Commitments

- `tasks/checkpoint-bridge/instruction.md`
- `tasks/checkpoint-bridge/task.toml`
- `tasks/checkpoint-bridge/output_contract.toml`
- `tasks/checkpoint-bridge/solution/solve.sh`
- `tasks/checkpoint-bridge/tests/test.sh`
- `tasks/checkpoint-bridge/tests/test_outputs.py`
- `tasks/checkpoint-bridge/environment/Dockerfile`
- `tasks/checkpoint-bridge/environment/exec/run_cycle.sh`
- `tasks/checkpoint-bridge/environment/CMakeLists.txt`
- `tasks/checkpoint-bridge/environment/c7k/p1m.cpp`
- `tasks/checkpoint-bridge/environment/c7k/p1m.hpp`
- `tasks/checkpoint-bridge/environment/c7k/decoy_h1.cpp`
- `tasks/checkpoint-bridge/environment/m2p/q4n.cpp`
- `tasks/checkpoint-bridge/environment/m2p/q4n.hpp`
- `tasks/checkpoint-bridge/environment/m2p/decoy_h2.cpp`
- `tasks/checkpoint-bridge/environment/w9n/s2t.cpp`
- `tasks/checkpoint-bridge/environment/w9n/s2t.hpp`
- `tasks/checkpoint-bridge/environment/w9n/frame.cpp`
- `tasks/checkpoint-bridge/environment/w9n/frame.hpp`
- `tasks/checkpoint-bridge/environment/w9n/decoy_h3.cpp`
- `tasks/checkpoint-bridge/environment/driver/entry.cpp`
- `tasks/checkpoint-bridge/environment/driver/flow.cpp`
- `tasks/checkpoint-bridge/environment/driver/flow.hpp`
- `tasks/checkpoint-bridge/environment/tooling/seq_tool.py`
- `tasks/checkpoint-bridge/environment/tooling/merge_tool.py`
- `tasks/checkpoint-bridge/environment/docs/field_guide.md`
- `tasks/checkpoint-bridge/environment/docs/ops_notes.md`
- `tasks/checkpoint-bridge/environment/schemas/report_fragments/run.schema.json`
- `tasks/checkpoint-bridge/environment/schemas/report_fragments/wave.schema.json`
- `tasks/checkpoint-bridge/environment/schemas/durable_row.schema.json`
- `tasks/checkpoint-bridge/environment/fixtures/window_a.json`
- `tasks/checkpoint-bridge/environment/fixtures/window_b.json`
- `tasks/checkpoint-bridge/environment/fixtures/pr_window.json`
- `tasks/checkpoint-bridge/environment/fixtures/rb_policy.json`
- `tasks/checkpoint-bridge/environment/fixtures/acct_baseline.json`
- `tasks/checkpoint-bridge/environment/fixtures/alt_view.json`
- `tasks/checkpoint-bridge/environment/fixtures/v9_markers.json`
- `tasks/checkpoint-bridge/environment/logging/l7_format.txt`
- `tasks/checkpoint-bridge/environment/logging/l7_samples.log`
- `tasks/checkpoint-bridge/environment/etc/service.env`
- `tasks/checkpoint-bridge/environment/etc/version.txt`
- `tasks/checkpoint-bridge/construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/c7k/p1m.cpp
  symbol: fn_k3
  kind: function
  signature: fn_k3(ctx, window, tier, inject_restart)
  purpose: Tags generation state across replay segments before persistence.

- path: environment/m2p/q4n.cpp
  symbol: fn_r8
  kind: function
  signature: fn_r8(views, acct, mode)
  purpose: Selects reconciler inputs among competing artifact surfaces.

- path: environment/w9n/s2t.cpp
  symbol: fn_x5
  kind: function
  signature: fn_x5(row, bases, kit_id, lane)
  purpose: Builds report-visible rows and cross-format digest fields.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/c7k/p1m.cpp
    controls_tests: [test_tseq_alpha, test_idempo_twice]
  - id: B
    path: environment/m2p/q4n.cpp
    controls_tests: [test_restore_overlap, test_fork_branch]
  - id: C
    path: environment/w9n/s2t.cpp
    controls_tests: [test_digest_chain, test_tseq_beta]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/c7k/decoy_h1.cpp
  kind: module
  rhymes_with: fn_k3
  non_fix_purpose: Implements alternate batching heuristics for cold-cache simulations unrelated to coordinator authority.

- path: environment/m2p/decoy_h2.cpp
  kind: helper
  rhymes_with: fn_r8
  non_fix_purpose: Provides deterministic toy merge demos for docs examples without participating in live driver paths.

- path: environment/w9n/decoy_h3.cpp
  kind: helper
  rhymes_with: fn_x5
  non_fix_purpose: Historical writer lane for archived runs not used in live report emission.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [incremental, rebuild, bridge, checkpoint, coordinator, ledger, tombstone, generation, counters, spans, digests, restart, boundary, rollback, health, summaries, invariants, replay, artifacts, linkage, waves]
```
