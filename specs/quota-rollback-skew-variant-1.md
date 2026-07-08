### Decision
GO — Attempt 1. Quota rollback skew is framed as a `distributed_reconciliation` repair with symptoms-only instructions, observation-shaped coordinator output, three-root flipping frontier, and a promoted reference mapping to `layered-policy-reload-drift` for multi-surface observation patterns.

### Metadata
- version: 2
- Task name: quota-rollback-skew-variant-1
- Title: Quota rollback skew
- Category: software-engineering
- Task shape: repair_existing_system
- Languages: ["python", "bash"]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: ["reconciliation", "rollback", "quotas", "observability", "distributed-systems"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Our distributed admission plane intermittently clears quotas for healthy tenants right after partial replays, yet later scheduling rounds still hand out holdings that conflict with what durable accounting expects once rollup windows finish. Regional probes and central rollups each look locally sane while disagreeing with each other until engineers trigger a full resynchronization.

Fix the sources under `/app/environment` so `/app/output/coordinator_bundle.json` is produced only by the normal inspection driver after each verifier run deletes any prior file. Static JSON writes, wrapper-only edits, or test changes are insufficient.

The instruction plan must stay bug-report-shaped: describe the false clears, the delayed cross-surface disagreement, the required command and output path, and the regeneration rule—without naming the broken functions, internal phase names, or which authority should win.

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

- path: environment/l7w/a9f.py
  role: ingest reconciliation and batch selection (fix frontier A)
- path: environment/l7w/decoy_g1.py
  role: decoy batching module
- path: environment/l7w/__init__.py
  role: package marker
- path: environment/q3p/b2c.py
  role: merge window and cleanup orchestration (fix frontier B)
- path: environment/q3p/decoy_g2.py
  role: decoy merge toy helper
- path: environment/q3p/__init__.py
  role: package marker
- path: environment/r8s/d4e.py
  role: coordinator row assembly for bundled reports (fix frontier C)
- path: environment/r8s/__init__.py
  role: package marker
- path: environment/exec/run_inspection.sh
  role: driver entrypoint invoked by tests
- path: environment/docs/op_handbook.md
  role: solver-visible semantics for reconciliation windows
- path: environment/docs/c_fields.md
  role: solver-visible coordinator row field semantics and formulas
- path: environment/fixtures/window_a.json
  role: seed fixture for first replay window
- path: environment/fixtures/window_b.json
  role: seed fixture for second replay window
- path: environment/fixtures/pr_prof.json
  role: partial replay stress profile
- path: environment/fixtures/c9_policy.json
  role: cleanup window parameters
- path: environment/fixtures/ledger_baseline.json
  role: durable accounting baseline
- path: environment/fixtures/alt_snapshot.json
  role: secondary snapshot inputs
- path: environment/fixtures/v9_expect.json
  role: expected regen markers
- path: environment/logging/l7_format.txt
  role: log line format reference
- path: environment/logging/l7_samples.log
  role: example log samples for orientation
- path: environment/schemas/c_row.schema.json
  role: JSON schema fragment for coordinator rows
- path: environment/schemas/mv_event.schema.json
  role: JSON schema fragment for window events
- path: environment/tooling/merge_c.py
  role: CLI helper used by driver
- path: environment/tooling/replay_c.py
  role: CLI helper for replay checks
- path: environment/etc/service.env
  role: non-secret defaults for driver
- path: environment/etc/version.txt
  role: pinned tool version string

### fix_frontier

- count: 3
- distribution: one module under `environment/l7w/` for ingest selection, one under `environment/q3p/` for cleanup ordering, one under `environment/r8s/` for coordinator row assembly; decoys stay colocated without sharing symbols.
- naming_policy: opaque stems and short alphanumeric-heavy filenames; fix-path symbols and path components avoid instruction domain nouns listed in the construction manifest.
- forbidden_stems: [tenants, probes, accounting, rollup, resynchronization, admission, quotas, workloads, holdings]
- helpers_policy: decoys perform credible adjacent work; fix symbols stay thin and split across files per manifest.
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [trace-derived numeric bands, cross-run row equality on derived fields, regen fingerprint checks, idempotent rerun counters, metamorphic comparisons across windows]
- forbidden_assertion_styles: [scenario-key-value boolean tables, raw truth bits without observations, instruction-only literals not homed in env/docs]

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis across interacting authorities under rollback and replay
- collapse_risk: naming the restore boundary, secondary snapshot tier, or coordinator assembly file explicitly could reduce the task to a one-file conditional flip.

### category_profile

- challenge_family: distributed_reconciliation
- bug_family: quota_rollback_skew
- profile_name: distributed_reconciliation
- allowed_instruction_disclosures: conflicting authority symptoms, reconciliation window behavior class, inspection command, regenerated coordinator bundle path, idempotence expectation, partial replay scenario class.
- forbidden_instruction_leaks: canonical source choice, shadow-vs-active symbol names, cleanup ordering patch site, coordinator assembly recipe, exact fix-path file names from the manifest.
- category_specific_hardness_bar: multiple truth surfaces with replay lineage, idempotent reruns, and stale metadata must interact; no single precedence table suffices.
- category_specific_verifier_risks: golden merged fixtures, count-only health checks, scenario-to-answer tables, GX9 answer saturation.
- coverage_role: adds a rollback-heavy reconciliation skew variant in the distributed reconciliation family, complementing promoted policy-reload reference patterns.

### satisfiability_risk

- rc2_planned_name_risk: medium — opaque stems and noun ban reduce grep collapse; risk rises if Step 2b reintroduces descriptive directory names.
- gx9_contract_risk: medium — coordinator rows are rich; keep instruction descriptive without co-locating scenario/key/value answer triples.
- cr1_symbol_frontier_risk: low — three thin symbols across files with helpers kept in decoys.
- hidden_contract_risk: low — formulas and schemas duplicated into `op_handbook.md` and `c_fields.md` as solver-visible homes.

### actionability_plan

- verifier_command_visible: instruction.md will name the bundled driver (`/app/environment/exec/run_inspection.sh`) and `/app/output/coordinator_bundle.json`, plus deletion/regeneration behavior.
- source_fix_intent_visible: instruction.md will require fixing Python sources under `/app/environment`, not hand-writing the bundle.
- generated_output_rule_visible: instruction.md will state tests remove `/app/output/coordinator_bundle.json` and regenerate it through the normal driver.
- exact_formula_home: row delta and window formulas live in `environment/docs/c_fields.md` and schema fragments under `environment/schemas/`.
- schema_home: `environment/schemas/*.schema.json` plus `c_fields.md` for nested field meanings.

### waiver_plan

- waivers_expected: no
- waiver_rationale: design avoids known never-waivable failures; expect no waivers if naming and GX6/GX9 hygiene hold during Step 2b.

### reference_pattern

- justification_if_none: No promoted reference in docs/reference_tasks/index.json matches this distributed-reconciliation coordinator-bundle repair; the sole promoted entry (async-pipeline-premature-completion) calibrates C++ xfer premature-completion matrices, not Python quota rollback skew, so hardness is calibrated independently.

### realism_source

- source_type: synthetic_exception
- evidence_basis: synthesized Option-B survivor seed from internal hardness exploration (no upstream CVE attached)
- upstream_or_synthetic_rationale: compresses recurring incident motifs—reconcilers reading secondary snapshots, cleanup windows reordering lineage, and inspection drivers trusting reconstructed summaries instead of canonical artifacts.
- minimization_preserves: asymmetric authorities, delayed false greens, rollback-sensitive lineage, and regeneration-dependent verification.
- synthetic_exception_review: category profile locked to distributed_reconciliation; actionability satisfied by docs plus schemas; output contract stays observation-shaped; extra scrutiny on GX9/GX10 and boolean field caps; no Greek or rubric-shaped module names.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, rollback_recovery_requirements, cross_file_cross_format_invariants, deceptive_but_valid_local_evidence
- adversarial_layers_count: 4
- fairness_guardrails: difficulty comes from deterministic artifacts, bundled docs, and verifier-derived invariants—not timing thresholds or hidden requirements.
- mechanism: false_green_intermediate_states
  placement: `environment/l7w/a9f.py` short-horizon probe path vs durable accounting path
  why_model_misses_it: models often patch the first green surface without proving later-generation rows still disagree.
  fairness_guardrail: instruction states delayed disagreement; traces expose both horizons.
- mechanism: rollback_recovery_requirements
  placement: `environment/q3p/b2c.py` cleanup and replay boundary hooks
  why_model_misses_it: rollback reorders events so naive idempotence keys reuse stale generations.
  fairness_guardrail: partial replay profile and deterministic seeds are public fixtures.
- mechanism: cross_file_cross_format_invariants
  placement: `environment/r8s/d4e.py` row assembly crossing JSON rows and log span tokens
  why_model_misses_it: row math looks locally consistent while violating cross-format bindings to ledger fixtures.
  fairness_guardrail: schemas and docs publish the cross-field obligations tested.
- mechanism: deceptive_but_valid_local_evidence
  placement: decoy modules under `environment/l7w/` and `environment/q3p/`
  why_model_misses_it: plausible duplicate APIs tempt edits away from the true coupling surface.
  fairness_guardrail: decoys are not on the driver import graph for production invocations.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: engineer can diff two bundle generations after scripted replays and spot inconsistent lineage keys without reading tests.
- shortcut_audit: watch static JSON writes, test-only shims, broad cache wipes, and single-location reverts that clear one symptom class.
- ablation_plan: drop row assembly checks, drop regeneration, or drop replay sequencing separately; each should ease agent success disproportionately if mechanisms matter.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger of target agent trials per repo calibration defaults.

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when every required semantic test passes; partial metric reasoning is used for author calibration.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step task; dependencies are encoded as stateful command/output invariants.
- local_only_data: true
- sidecar_or_protocol_notes: no auxiliary databases; all data lives under `environment/fixtures` with local JSON and logs only.

### Failure topology
The symptom cluster spans immediate post-replay clears, later scheduling generations, durable accounting expectations after rollup windows, and divergent regional versus central summaries. The public contract can disclose window semantics, the coordinator bundle schema, and the inspection command, but the solver must discover how ingest selection, cleanup ordering, and row assembly interact so locally consistent views still disagree until a forced resynchronization. A one-location fix is insufficient because tightening probes without fixing assembly—or vice versa—preserves plausible false greens.

### Environment shape
Ship a small Python service layout: opaque ingest package (`l7w`), orchestration package (`q3p`), row assembly package (`r8s`), an `exec` driver entrypoint, `docs` for formulas, `fixtures` for deterministic windows, `schemas` for JSON fragments, `tooling` CLIs, and lightweight logging samples. Decoys sit beside frontier modules without sharing their symbols.

### Required artifacts
Create a standard single-step task with `instruction.md`, `task.toml`, `output_contract.toml`, `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Under `environment/`, create at least 20 non-Docker files with substantive code, docs, fixtures, and helpers matching the shape above, plus `construction_manifest.json` at the task root mirroring the blocking manifest in this spec.

### Test plan
1. **`test_lineage_tag_matches_slice_and_rank_invariant`** — replays two windows and checks early versus late coordinator rows agree on derived holdings bands; catches single-horizon fixes.
2. **`test_stable_fingerprint_and_volatile_span_id_across_regens`** — reruns the driver twice with identical inputs and demands identical bundle fingerprints except for documented volatile span ids; catches static writes.
3. **`test_alloc_band_matches_pulse_ladder`** — cross-checks numeric bands implied by fixtures against assembled rows; catches summary-only shortcuts.
4. **`test_sequence_signature_follows_ascending_cleanup_rank`** — exercises cleanup ordering permutations from `c9_policy.json` and asserts lineage keys remain coherent; catches reorder bugs.
5. **`test_regen_markers_match_marker_pattern`** — deletes `/app/output/coordinator_bundle.json`, regenerates, and verifies regen markers align with `v9_expect.json` patterns; catches stale reconstruction sources.

### Drafting guardrails
Do not name the exact broken mechanism, internal phase names, or manifest symbols in `instruction.md`, tests, comments, fixtures, or docs beyond this construction manifest. Keep every externally tested field, command path, and formula visible in docs or schemas, but avoid scenario-to-answer tables and avoid recycling instruction nouns as code symbols or path stems on the fix frontier.

### Triviality Ledger

- **Hand-writing `/app/output/coordinator_bundle.json`** fails because tests delete the file and regenerate it through the driver for multiple replay permutations.
- **Wrapper-only edits** fail because row assembly, cleanup ordering, and ingest selection each gate distinct flipping subsets.
- **Broad global cache wipes** fail idempotent rerun and stability controls that require nuanced invalidation.
- **Patching only fixtures** fails because the bug lives in source reconciliation behavior, not seeded numbers alone.
- **Reciting answer triples in instruction.md** is forbidden; tests derive expectations from visible formulas plus emitted observations.

### Per-gate Pitfall Inventory

- **RC1 / Oracle simplification**: oracle must coordinate semantics across three modules, not one heredoc replacement.
- **RC2 / Oracle predictability**: keep opaque stems; ban instruction nouns on the fix path per manifest tokens.
- **RC3 / Verifier shallowness**: assert cross-window and cross-surface relations, not JSON presence alone.
- **RC4 / Tamper surface**: expected values derive from visible docs/schemas and emitted rows, not hidden goldens.
- **RC5 / Reference artifacts**: fixtures are inputs only; no pre-baked bundle answers under `environment/`.
- **RC6 / Instruction specificity**: symptoms-only; disclose commands, paths, schemas, formulas, but not patch sites.
- **RC7 / Oracle triviality**: oracle must include substantive multi-file coordination clearing GX3 floors.
- **CR1 / Symbol frontier**: construction manifest predeclares all oracle-touched symbols.
- **CR8 / Orchestration fanout**: driver imports public package surfaces, not every frontier symbol from one file.
- **GX9 / Answer recital**: forbid co-located scenario/key/value windows; keep values derivable from observations.
- **GX10 / Polarity contradiction**: avoid both polarities of one status word for a single scenario sentence.
- **Static checks / packaging**: forbid cache or build trees under `environment/` per repo `FORBIDDEN_ENV_COMPONENTS` policy; Dockerfile copies only committed sources.

### Initial Draft Commitments

- `tasks/quota-rollback-skew-variant-1/instruction.md`
- `tasks/quota-rollback-skew-variant-1/task.toml`
- `tasks/quota-rollback-skew-variant-1/output_contract.toml`
- `tasks/quota-rollback-skew-variant-1/solution/solve.sh`
- `tasks/quota-rollback-skew-variant-1/tests/test.sh`
- `tasks/quota-rollback-skew-variant-1/tests/test_outputs.py`
- `tasks/quota-rollback-skew-variant-1/environment/Dockerfile`
- `tasks/quota-rollback-skew-variant-1/environment/l7w/a9f.py`
- `tasks/quota-rollback-skew-variant-1/environment/l7w/decoy_g1.py`
- `tasks/quota-rollback-skew-variant-1/environment/l7w/__init__.py`
- `tasks/quota-rollback-skew-variant-1/environment/q3p/b2c.py`
- `tasks/quota-rollback-skew-variant-1/environment/q3p/decoy_g2.py`
- `tasks/quota-rollback-skew-variant-1/environment/q3p/__init__.py`
- `tasks/quota-rollback-skew-variant-1/environment/r8s/d4e.py`
- `tasks/quota-rollback-skew-variant-1/environment/r8s/__init__.py`
- `tasks/quota-rollback-skew-variant-1/environment/exec/run_inspection.sh`
- `tasks/quota-rollback-skew-variant-1/environment/docs/op_handbook.md`
- `tasks/quota-rollback-skew-variant-1/environment/docs/c_fields.md`
- `tasks/quota-rollback-skew-variant-1/environment/fixtures/window_a.json`
- `tasks/quota-rollback-skew-variant-1/environment/fixtures/window_b.json`
- `tasks/quota-rollback-skew-variant-1/environment/fixtures/pr_prof.json`
- `tasks/quota-rollback-skew-variant-1/environment/fixtures/c9_policy.json`
- `tasks/quota-rollback-skew-variant-1/environment/fixtures/ledger_baseline.json`
- `tasks/quota-rollback-skew-variant-1/environment/fixtures/alt_snapshot.json`
- `tasks/quota-rollback-skew-variant-1/environment/fixtures/v9_expect.json`
- `tasks/quota-rollback-skew-variant-1/environment/logging/l7_format.txt`
- `tasks/quota-rollback-skew-variant-1/environment/logging/l7_samples.log`
- `tasks/quota-rollback-skew-variant-1/environment/schemas/c_row.schema.json`
- `tasks/quota-rollback-skew-variant-1/environment/schemas/mv_event.schema.json`
- `tasks/quota-rollback-skew-variant-1/environment/tooling/merge_c.py`
- `tasks/quota-rollback-skew-variant-1/environment/tooling/replay_c.py`
- `tasks/quota-rollback-skew-variant-1/environment/etc/service.env`
- `tasks/quota-rollback-skew-variant-1/environment/etc/version.txt`
- `tasks/quota-rollback-skew-variant-1/construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/l7w/a9f.py
  symbol: fn_u7
  kind: function
  signature: def fn_u7(ctx, batch, tier):
  purpose: Selects reconciliation inputs for ingest batches before persistence.

- path: environment/q3p/b2c.py
  symbol: fn_v2
  kind: function
  signature: def fn_v2(window, events, ledger):
  purpose: Orders merge and cleanup transitions across replay windows.

- path: environment/r8s/d4e.py
  symbol: fn_w4
  kind: function
  signature: def fn_w4(rows, bases, mode):
  purpose: Builds coordinator-visible rows from supplied bases and modes.

- path: environment/l7w/a9f.py
  symbol: _window_trace_pad
  kind: helper
  purpose: Co-resident static footprint helper mirrored on each frontier module (never invoked by the driver).
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/l7w/a9f.py
    controls_tests: [test_lineage_tag_matches_slice_and_rank_invariant]
  - id: B
    path: environment/q3p/b2c.py
    controls_tests: [test_sequence_signature_follows_ascending_cleanup_rank]
  - id: C
    path: environment/r8s/d4e.py
    controls_tests: [test_alloc_band_matches_pulse_ladder]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/l7w/decoy_g1.py
  kind: module
  rhymes_with: fn_u7
  non_fix_purpose: Implements alternate batching heuristics for cold-cache simulations unrelated to coordinator authority.

- path: environment/q3p/decoy_g2.py
  kind: helper
  rhymes_with: fn_v2
  non_fix_purpose: Provides deterministic toy merge demos for docs examples without participating in live driver paths.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [tenants, probes, accounting, rollup, resynchronization, admission, quotas, workloads, holdings]
```
