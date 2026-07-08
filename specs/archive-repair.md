### Decision
GO — Attempt 1. Security authority-split reverse-engineering task with three distributed roots (rollback generation, canonical selector, bind emission), observation-shaped audit traces, flipping contract at 33% concentration each, and reference calibration to `layered-policy-reload-drift` for verifier discipline without cloning its policy domain.

### Metadata
- version: 2
- Task name: archive-repair
- Title: Archive policy reconciliation
- Category: security
- Task shape: reverse_engineering
- Languages: ["cpp", "bash"]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: ["security", "policy", "replay", "authority", "reconciliation", "audit"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Operators run a deterministic observation runner (`/app/bin/ark_run`) that rebuilds `/app/output/ark_trace.json` after scripted restart and rollback sequences on a hardened storage gateway. Observed behavior: intermediate health summaries report allowed principal transitions while durable seal markers and later-wave digest linkages disagree—especially after a single process restart boundary and when overlapping policy bundles are replayed. Catalog rows, sealed envelope index entries, and rollback manifest slices can each look self-consistent in isolation yet fail cross-surface linkage checks in later waves.

The solver must repair implementation under `/app/environment` so every tested scenario regenerates a trace whose principal transitions, freshness tokens, seal generation counts, and cross-format digest linkages stay consistent across replay and rollback phases. Do not hand-author `/app/output/ark_trace.json`; tests delete it and invoke the normal runner.

Required observation sections, CLI flags, digest formulas, and schema are documented in `environment/app/docs/ark_contract.md` and summarized at a high level in `instruction.md` without naming defective modules or patch order.

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

- path: environment/runner.cpp
  role: layout marker for runner module
- path: environment/app/entry.cpp
  role: command dispatch and scenario orchestration
- path: environment/app/flow.cpp
  role: normalizes run records for audit traces
- path: environment/rx/gen_track.cpp
  role: fix-frontier generation tracking across replay boundaries
- path: environment/rx/phase_hook.cpp
  role: rollback phase ordering hooks
- path: environment/rx/shadow_clip.cpp
  role: decoy clip helper
- path: environment/vx/selector.cpp
  role: fix-frontier canonical surface selection
- path: environment/vx/store.cpp
  role: durable envelope persistence
- path: environment/vx/side_index.cpp
  role: decoy side index helper
- path: environment/wx/link.cpp
  role: fix-frontier digest and principal transition emission
- path: environment/wx/frame.cpp
  role: trace framing helpers
- path: environment/wx/hist_lane.cpp
  role: non-fix historical writer lane
- path: environment/app/core/types.cpp
  role: shared value objects for principals and seals
- path: environment/app/core/checks.cpp
  role: consistency checks used by runner
- path: environment/app/readers/basefile.cpp
  role: fixture reader
- path: environment/app/readers/kitfile.cpp
  role: policy kit fixture reader
- path: environment/app/readers/princfile.cpp
  role: principal fixture reader
- path: environment/util/tag_core.cpp
  role: hash helpers for linkage tags
- path: environment/util/json_write.cpp
  role: JSON emission helpers
- path: environment/app/data/kits.toml
  role: policy kit fixture
- path: environment/app/data/principals.json
  role: principal and revocation fixture
- path: environment/app/docs/ark_contract.md
  role: solver-visible observation schema, digest rules, CLI semantics
- path: environment/app/docs/operators.md
  role: operational context without patch guidance
- path: environment/app/tools/inspect.sh
  role: diagnostic helper
- path: environment/app/tools/sample_env.sh
  role: example setup

### fix_frontier

- count: 3
- distribution: one module each under environment/rx, environment/vx, and environment/wx
- naming_policy: opaque fix-path symbols per construction manifest; neutral rx/vx/wx package directories
- forbidden_stems: ["gateway", "policy", "checkpoint", "replays", "restart", "rollback", "health", "summaries", "allowed", "durable", "seal", "markers", "verifier", "digest", "catalog", "envelope", "manifest", "linkage", "waves", "principal", "transitions", "freshness", "tokens", "generation", "counts"]
- helpers_policy: decoy modules perform plausible sibling work; fix-path symbols remain thin
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: ["audit trace runs and waves", "cross-run digest identities", "principal transition chains", "metamorphic clean-vs-replay comparisons", "idempotence reruns", "freshness token provenance"]
- forbidden_assertion_styles: ["boolean answer keys", "scenario-to-value truth tables in instruction", "tests that only assert JSON presence"]

### task_shape

- type: reverse_engineering
- instruction_framing: constraint-complete
- hardness_source: semantic inference across split encode/decode/enforce authorities with false-green durability
- collapse_risk: leaking replay ordering bug or authoritative artifact path collapses to one-file repair

### category_profile

- challenge_family: policy reconciliation
- profile_name: security_authority_split
- allowed_instruction_disclosures: assets, principals, allowed/denied outcomes, audit trace command and path, authority boundary description, externally tested freshness and digest linkage summarized without patch hints
- forbidden_instruction_leaks: vulnerable sink location, trust-boundary implementation file, exploit primitive, patch rule, sanitizer name, exact guard function, or which surface is canonical by default
- category_specific_hardness_bar: encode/decode/enforce authorities must reconcile under changing principals, freshness, and revocation across replay boundaries
- category_specific_verifier_risks: toy checklist, blocklist bypass, one exploit-string test, process-only assertions without durable seal checks
- coverage_role: Adds security_authority_split coverage with policy reconciliation and reverse_engineering shape distinct from config_policy_precedence references

### difficulty_mechanism_plan

- mechanisms: environment_specific_cli_semantics, cross_file_cross_format_invariants, false_green_intermediate_states, rollback_recovery_requirements
- adversarial_layers_count: 4
- fairness_guardrails: difficulty comes from deterministic state, documented formulas, and verifier-derived observations rather than latency thresholds or hidden requirements
- mechanism: environment_specific_cli_semantics
  placement: ark_run scenario flags control restart injection and rollback phase ordering documented in ark_contract.md
  why_model_misses_it: models assume generic CLI success codes imply durable reconciliation
  fairness_guardrail: flag meanings and scenario matrix are fully documented locally
- mechanism: cross_file_cross_format_invariants
  placement: JSON audit traces, TOML bundles, and sealed byte envelopes must agree on digest linkage
  why_model_misses_it: editing one format leaves orphans that still pass shallow checks
  fairness_guardrail: cross-format rules are in ark_contract.md with worked examples
- mechanism: false_green_intermediate_states
  placement: early waves show allowed health summaries while durable seals and later-wave linkages disagree
  why_model_misses_it: agents stop after first green health summary without chaining reruns
  fairness_guardrail: failing behavior visible through documented command and trace fields
- mechanism: rollback_recovery_requirements
  placement: rollback phases require idempotent merges without clobbering durable seals or principal transitions
  why_model_misses_it: shortcut flush fixes one rerun but breaks another rollback scenario
  fairness_guardrail: deterministic fixtures with seeded ordering

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: expert can trace three roots using ark traces and ark_contract.md within a few hours
- shortcut_audit: watch for static JSON writes, digest hardcoding, test edits, NOP oracle gaming
- ablation_plan: drop rollback fix alone, drop selector fix alone, drop bind fix alone to show partial failures
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent on identical Harbor harness

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt equals 1 only when every weighted semantic check passes in test_outputs.py

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: single-step task; ordering expressed via stateful command sequences inside tests
- local_only_data: true
- sidecar_or_protocol_notes: all fixtures and traces are local; single-container only; no network fetch

### satisfiability_risk

- rc2_planned_name_risk: medium; neutral rx/vx/wx roots with decoys; instruction uses standard security vocabulary kept off fix path
- gx9_contract_risk: low; instruction discloses schema and derivation rules, not per-row expected literals
- cr1_symbol_frontier_risk: medium; three thin fix symbols with co-resident helpers listed in task_files
- hidden_contract_risk: low; verifier command, regeneration rule, and digest formulas planned in ark_contract.md and instruction summary

### actionability_plan

- verifier_command_visible: instruction.md names /app/bin/ark_run, /app/output/ark_trace.json, and pytest entry via tests/test.sh
- source_fix_intent_visible: instruction.md requires repairing /app/environment so the normal pipeline regenerates the observation report
- generated_output_rule_visible: instruction.md states tests delete ark_trace.json and rerun generation across restart and rollback scenarios
- exact_formula_home: digest linkage, freshness token binding, and generation count rules in environment/app/docs/ark_contract.md mirrored at high level in instruction.md
- schema_home: observation report top-level shape (runs, waves, principal_transitions, digest_records) in ark_contract.md

### waiver_plan

- waivers_expected: no
- waiver_rationale: design stays within standard collapse, actionability, and output-contract policy without checker false positives

### reference_pattern

- reference_task_id: async-pipeline-premature-completion

### realism_source

- source_type: real_system
- evidence_basis: minimized from operator incidents on hardened archive gateways where health probes green early while sealed generation state and audit digests diverge after checkpointed replays
- upstream_or_synthetic_rationale: pattern matches internal postmortems on split authority stores in policy engines; local fixtures replace proprietary payloads
- minimization_preserves: false-green intermediate states, stale generation across one restart, conflicting artifact surfaces, and rollback/replay coupled invariants
- synthetic_exception_review: not a synthetic_exception; real_system minimization with documented causal structure

### Failure topology
Symptoms arrive late: early audit waves show allowed health summaries, then later waves expose crossed digest linkages after operators rerun the pipeline across replay boundaries. Multiple authorities stay locally coherent—catalog views, sealed envelope indices, and rollback manifest slices—so naive patches that trust the first green surface fail deeper reruns. Hardness survives honest disclosure because digest and freshness rules live in public docs while the bug is which authority feeds the verifier when rollback phases overlap restart boundaries.

### Environment shape
Ship a small C++ service layout: a runner that writes audit traces, packages split into rx rollback timing, vx persistence/selection, and wx bind emission, plus readers, fixtures, and operator-facing docs. Decoy helpers live beside fix paths but stay off the oracle frontier per manifest. Single-container only.

### Required artifacts
Create a standard single-step task with `instruction.md`, `task.toml`, `output_contract.toml`, `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Under `environment/`, deliver 26+ non-Docker files matching `task_files` and `Initial Draft Commitments`.

### Test plan
1. **`test_m7_qz_emit`** — restart boundary sequence: generation markers must invalidate correctly across one process restart; fails if rollback-only shortcut ignores durable seals.
2. **`test_n4_pl_pair`** — paired replay ordering: different interleavings catch ordering assumptions baked into one helper.
3. **`test_idempo_dup`** — reruns ark_run twice with identical inputs; requires idempotent trace merge without duplicate envelope references.
4. **`test_f2_kx_cycle`** — derives expected digest records from public rules in ark_contract.md plus observed store bytes; blocks static JSON lifts.
5. **`test_pl_n8_cycle`** — simulates back-to-back rollback phases with overlapping replay windows; fails if link emission drops refreshed principal identifiers.
6. **`test_fork_x9`** — compares parallel scenario branches inside one report; catches link rows that disagree with store-backed envelopes for the same wave.

### Drafting guardrails
Keep constraint-complete public vocabulary in honest terms, but ban instruction nouns on fix-path symbols, test function names, and package path tokens that grep-collapse to the bug. Do not put per-scenario allow/deny answer tables in instruction.md. Do not name `op_a`, `reconcile_b`, or `phase_c` in instruction prose. Do not leak which artifact surface is authoritative or the exact replay ordering defect.

### Triviality Ledger

- **Hand-writing `/app/output/ark_trace.json`** fails because tests delete and regenerate it through ark_run across scenarios.
- **Health-summary-only trust flip** fails `test_f2_kx_cycle` and `test_pl_n8_cycle` when envelopes disagree with link rows after overlap.
- **Global cache wipe** fails idempotence and fork-path invariants that require nuanced invalidation.
- **Editing only `phase_hook.cpp`** fails replay tagging tests that depend on coordinated rollback and bind behavior.
- **Reciting literals in instruction.md** is forbidden; tests derive expectations from documented formulas plus observed artifacts.

### Per-gate Pitfall Inventory

- **RC1 / oracle simplification**: oracle must touch three behavioral files with coordinated logic, not one heredoc replacement.
- **RC2 / grep resistance**: keep instruction noun tokens out of fix-path code symbols and planned test names; verify with collapse grep pass after build.
- **RC6 / instruction audit**: maintain constraint-complete reverse_engineering prose; put formulas in ark_contract.md without causal patch chains.
- **RC7–RC8 / oracle size and symbol fan-in**: spread real logic across rollback, selector, and bind; avoid one mega-file owning every symbol.
- **CR1–CR2 / symbol frontier and flipping**: honor construction manifest symbol table and flipping subsets exactly.
- **CR7–CR9 / contract helpers**: keep derivation implementations in env, not only in tests.
- **GX1 / comment leaks**: no bug/fix vocabulary in env comments near oracle edits.
- **GX5–GX6 / instruction-test overlap and causal density**: avoid mirroring test keys in instruction; limit causal connective stacking in public prose.
- **GX9–GX10 / answer tables and polarity traps**: use observation records; never bind both polarities of one status to a single scenario sentence.
- **GX3 / edit distance**: plan oracle with substantive multi-site coordination, not padding.
- **Static / packaging gates**: ensure Dockerfile provides python3 for runner and tests.

### Initial Draft Commitments

- environment/CMakeLists.txt
- environment/runner.cpp
- environment/app/entry.cpp
- environment/app/flow.cpp
- environment/rx/gen_track.cpp
- environment/rx/phase_hook.cpp
- environment/rx/shadow_clip.cpp
- environment/vx/selector.cpp
- environment/vx/store.cpp
- environment/vx/side_index.cpp
- environment/wx/link.cpp
- environment/wx/frame.cpp
- environment/wx/hist_lane.cpp
- environment/app/core/types.cpp
- environment/app/core/checks.cpp
- environment/app/readers/basefile.cpp
- environment/app/readers/kitfile.cpp
- environment/app/readers/princfile.cpp
- environment/util/tag_core.cpp
- environment/util/json_write.cpp
- environment/app/data/kits.toml
- environment/app/data/principals.json
- environment/app/docs/ark_contract.md
- environment/app/docs/operators.md
- environment/app/tools/inspect.sh
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
- path: environment/rx/gen_track.cpp
  symbol: op_a
  kind: function
  signature: op_a(ctx, phase_id, seq_bundle)
  purpose: Tracks generation markers across replay and rollback segments for downstream readers.
- path: environment/vx/selector.cpp
  symbol: reconcile_b
  kind: function
  signature: reconcile_b(store_handle, view_handle, mode_flag)
  purpose: Chooses reconciler inputs among catalog, envelope index, and manifest views.
- path: environment/wx/link.cpp
  symbol: phase_c
  kind: function
  signature: phase_c(trace_row, envelope_bytes, policy_id)
  purpose: Materializes externally visible digest rows and principal transition records.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/rx/gen_track.cpp
    controls_tests: [test_m7_qz_emit, test_n4_pl_pair]
  - id: B
    path: environment/vx/selector.cpp
    controls_tests: [test_idempo_dup, test_f2_kx_cycle]
  - id: C
    path: environment/wx/link.cpp
    controls_tests: [test_pl_n8_cycle, test_fork_x9]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/rx/shadow_clip.cpp
  kind: module
  rhymes_with: op_a
  non_fix_purpose: Optional clip helper for diagnostics-only replay slices.
- path: environment/vx/side_index.cpp
  kind: helper
  rhymes_with: reconcile_b
  non_fix_purpose: Maintains a historical side index not used for live canonical selection.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [gateway, policy, checkpoint, replays, restart, rollback, health, summaries, allowed, durable, seal, markers, verifier, digest, catalog, envelope, manifest, linkage, waves, principal, transitions, freshness, tokens, generation, counts]
```
