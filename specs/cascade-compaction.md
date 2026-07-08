### Decision
GO — Attempt 1. C++ namespace compaction recovery with six cross-invocation durability properties, opaque fix roots (k7w/m9p/n4q), session high-water registry, and ledger-anchor chaining—raised from prior trivial pass rate via multi-invocation state and append semantics.

### Metadata
- version: 2
- Task name: cascade-compaction
- Title: Cascade Compaction
- Category: system-administration
- Task shape: formal_reasoning
- Languages: ["cpp", "bash"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["compaction", "namespace", "crash-consistency", "replay", "recovery"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Operate the bundled single-node namespace compaction recovery stack under `/app/environment`. After deterministic crash drills used by the verifier, the stack must satisfy the durability obligations in `/app/environment/docs/formal_rules.md`.

Run `/app/bin/cc_run` as documented there to emit `/app/output/cc_report.json`, logs under `/app/output/run_logs/`, and an updated `/app/environment/state/session.registry` after each invocation. Report and ledger shapes are defined in `formal_rules.md`. Profile `d` combines restart-boundary and conflicting-summary behavior in one run.

Required properties across restart boundaries:
1. Active generation stamps advance only after sealed segments are recorded in the authoritative manifest chain.
2. When intermediate health summaries disagree with compaction manifest digests, verification must treat the manifest chain as authoritative for downstream checks.
3. Rollback phases must not truncate the replay cursor while tail segments remain unsealed; re-executing recovery must be idempotent on already-sealed records.
4. Sequential invocations append report and ledger artifacts without overwriting prior invocations.
5. Each appended ledger run carries a `ledger_anchor_hex` chaining to the prior run fingerprint.
6. Session registry `gen_high_water` carries across invocations and floors later generation stamps.

Repair implementation under `/app/environment` so all properties hold. Do not satisfy tests by hand-writing output files without executing the normal driver pipeline.

### platform_files
- path: task.toml
  role: metadata
- path: instruction.md
  role: natural public task prompt
- path: output_contract.toml
  role: local output declaration
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
- path: environment/k7w/lane_mux.cpp
  role: replay lane mux and sealed tail recording
- path: environment/m9p/stamp_mux.cpp
  role: generation stamp registry across restarts
- path: environment/n4q/mux_sel.cpp
  role: manifest digest folding
- path: environment/tools/summary_mux.cpp
  role: intermediate health summaries
- path: environment/pilot/entry.cpp
  role: published recovery driver entrypoint
- path: environment/engine/pipeline.cpp
  role: multi-phase orchestration
- path: environment/engine/session_registry.cpp
  role: cross-invocation generation high-water persistence
- path: environment/docs/formal_rules.md
  role: formal properties and schema references

### fix_frontier
- count: 3
- distribution: One opaque function each under environment/k7w, environment/m9p, and environment/n4q; plus orchestration in pilot/entry, pipeline floor, and session_registry persistence.
- naming_policy: Opaque identifiers (fn_k2, fn_h8, fn_w4) with neutral parameter names; no instruction nouns on fix path.
- forbidden_stems: authoritative, boundaries, cascade, chain, compaction, digests, durability, generation, health, idempotent, ledgers, manifest, namespace, records, recovery, replay, restart, rollback, sealed, segments, summaries, tail, truncate
- helpers_policy: Decoys perform credible adjacent work; frontier stays thin at three symbols with driver/registry orchestration separate.
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 0
- direct_boolean_assertions_max: 2
- preferred_assertion_styles: trace row digests, ledger run fingerprints, cross-boundary generation stamp monotonicity, manifest-chain equality, anchor chaining, session high-water
- forbidden_assertion_styles: readiness boolean verdict fields, scenario-key-expected tables in instruction

### task_shape
- type: formal_reasoning
- instruction_framing: constraint-complete
- hardness_source: formal correctness across multi-invocation append and registry state
- collapse_risk: Leaking replay-phase ordering or the authoritative manifest path collapses the task to a one-file conditional repair.

### category_profile
- challenge_family: namespace restore
- profile_name: state_recovery_crash_consistency
- allowed_instruction_disclosures: Crash/restart workflow, durability obligations, recovery driver command class, expected trace and ledger artifacts, formal invariants and schema homes.
- forbidden_instruction_leaks: Journal/checkpoint internals, broken recovery phase identity, corruption source coordinates, replay ordering recipe, fix-path symbol names.
- category_specific_hardness_bar: Partial writes, replay, cleanup, and rerun safety must coordinate across restart boundaries with conflicting observability and cross-invocation registry/append semantics.
- category_specific_verifier_risks: Nondeterministic crash timing, one hidden snapshot shortcuts, verifier reading private internals instead of emitted traces.
- coverage_role: Adds formal_reasoning depth to state_recovery_crash_consistency under system-administration with namespace-restore topology distinct from filesystem reconstruction repair tasks.

### satisfiability_risk
- rc2_planned_name_risk: low — opaque package roots and renamed verifier cases avoid fix-path/test token overlap.
- gx9_contract_risk: low — tests derive verdicts from trace rows and digests rather than boolean answer keys.
- cr1_symbol_frontier_risk: medium — three thin symbols plus documented decoys and driver/registry orchestration must stay explicit in manifest.
- hidden_contract_risk: low — formal_rules.md and cc_run document formulas and driver steps mirrored in tests.

### actionability_plan
- verifier_command_visible: Instruction cites C++ recovery driver `/app/bin/cc_run` built from `/app/environment` and output roots under `/app/output/`.
- source_fix_intent_visible: Prompt requires repairing implementation under /app/environment without naming frontier files.
- generated_output_rule_visible: Instruction mandates deleting then rebuilding cc_report.json and run_logs via the normal driver pipeline.
- exact_formula_home: environment/docs/formal_rules.md defines digest-chain, monotonicity, anchor, and high-water rules exercised by tests.
- schema_home: environment/schemas/report_row.schema.json plus formal_rules.md; output_contract.toml lists artifact paths only.

### waiver_plan
- waivers_expected: false
- waiver_rationale: Design keeps contracts observation-shaped with solver-visible formal homes; waivers should be unnecessary if Step 2b follows manifest.

### reference_pattern
- justification_if_none: Promoted reference layered-policy-reload-drift targets config_policy_precedence observation reloads, not formal_reasoning namespace-restore crash consistency; no promoted reference_task_id in docs/reference_tasks/index.json applies.

### realism_source
- source_type: real_system
- evidence_basis: Minimized from etcd/kubernetes-style namespace compaction and WAL recovery incident patterns where health checks green before durable invariants hold.
- upstream_or_synthetic_rationale: Preserves conflicting observability surfaces and restart-boundary generation skew seen in real control-plane compaction stacks without cloning a single CVE.
- minimization_preserves: False-green summaries, manifest authority, sealed-segment replay, rollback-sensitive cursor semantics, and multi-invocation append/registry continuity.
- synthetic_exception_review: Not required for real_system sourcing; formal contract is disclosed while implementation coordinates remain discoverable.

### difficulty_mechanism_plan
- mechanisms: rollback_recovery_requirements, cross_file_cross_format_invariants, partial_observability_experiment_design, stateful_multi_step_dependencies, false_green_intermediate_states
- adversarial_layers_count: 5
- fairness_guardrails: Deterministic local crash fixtures; all formal properties and schema homes are solver-visible; no timing-as-hardness.
- mechanism: rollback_recovery_requirements
  placement: environment/k7w/lane_mux.cpp with crash fixtures under environment/fixtures/crash_profiles/
  why_model_misses_it: Agents patch forward progress without ensuring rollback leaves replay cursors able to re-apply sealed tails idempotently.
  fairness_guardrail: Crash profiles are deterministic and bundled locally; formal_rules.md states idempotence obligations.
- mechanism: cross_file_cross_format_invariants
  placement: environment/n4q/mux_sel.cpp versus environment/tools/summary_mux.cpp and report JSON under /app/output/
  why_model_misses_it: Models trust human-readable summaries instead of manifest digest chains required by formal properties.
  fairness_guardrail: Authority rule is disclosed; tests compare derived digests from emitted artifacts.
- mechanism: partial_observability_experiment_design
  placement: summary_mux summaries versus cc_report.json rows after scripted crashes
  why_model_misses_it: Intermediate probes look healthy before generation and sealing invariants converge across restart boundaries.
  fairness_guardrail: All observability surfaces are local; verifier reruns driver after deleting outputs.
- mechanism: stateful_multi_step_dependencies
  placement: multi-phase cc_run workflow with persisted state under environment/state/
  why_model_misses_it: Single-pass edits fix one phase while leaving stale registry snapshots for the next restart drill.
  fairness_guardrail: State transitions are deterministic and exposed through visible commands and ledgers.
- mechanism: false_green_intermediate_states
  placement: environment/tools/summary_mux.cpp before manifest-chain tests in pytest ordering
  why_model_misses_it: Agents stop after a passing health summary without validating cross-boundary generation monotonicity.
  fairness_guardrail: Final verifier contract requires trace-derived invariants, not probe booleans alone.

### calibration_plan
- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: One careful human can satisfy invariants using only formal_rules.md, bundled fixtures, and cc_run without web access.
- shortcut_audit: Watch for hand-written JSON, static manifest copies, test edits, and reward-file writes bypassing driver regeneration.
- ablation_plan: Remove manifest-authority layer, then rollback idempotence layer, then false-green probes; expect interpretable difficulty drops.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent trials on comparable state-recovery formal tasks

### verifier_scoring_plan
- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt is 1 only when every semantic pytest case passes.

### subtype_milestone_plan
- subcategories: []
- milestone_count: 0
- sequential_dependency: Single-step task; dependencies encoded as stateful driver/output invariants across crash phases and sequential invocations.
- local_only_data: true
- sidecar_or_protocol_notes: All fixtures and protocols are local; no runtime web fetching.

### Failure topology
Compaction recovery reports healthy intermediate summaries while durable invariants fail across scripted restart boundaries. Generation stamps can appear to advance before sealed segments enter the manifest chain; health probes may disagree with digest chains until authority selection aligns; rollback can truncate replay cursors while tails remain unsealed, breaking idempotent reruns; sequential invocations may overwrite prior artifacts or break anchor chaining and session high-water. Hardness depends on tracing coupled replay, registry, folding, and driver behavior—not spotting one corrupted checksum file.

### Environment shape
Split C++ modules across k7w (lane mux and buffering), m9p (stamp registry), n4q (folding and rank diagnostics), tools (summary mux), pilot entrypoint, engine pipeline and session registry, docs (formal contract), schemas, fixtures (crash profiles), and small state directories. Single-container only; no multi-service compose beyond Harbor template.

### Required artifacts
instruction.md, task.toml, output_contract.toml, construction_manifest.json mirroring the manifest below, Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh, plus at least 20 C++/text/schema assets under environment/ excluding Docker-only boilerplate.

### Test plan
- test_p1_boundary_monotone_seals: restart boundary — generation stamps and sealed segments align in regenerated trace rows after drill a.
- test_p2_row_digest_matches_rows: manifest authority — folded digest matches emitted rows per formal property.
- test_p3_authority_over_health_probe: manifest authority — when health summaries and manifest digests disagree, verification uses folded digest per formal property.
- test_p4_rollback_idempotent: rollback idempotence — recovery reruns do not duplicate sealed records or leave truncated cursors.
- test_p5_append_preserves_prior: append semantics — sequential invocations retain prior report and ledger artifacts.
- test_p6_anchor_across_appends: anchor chaining — ledger_anchor_hex chains fingerprints across appended invocations.
- test_p7_rw_high_water_carries: session registry — gen_high_water carries across invocations.
- test_p8_cross_invocation_floor: session floor — later invocations respect prior high-water after restart drill.
- test_p9_combined_restart_conflict: drill d — combined restart and conflicting-summary behavior in one run.
- test_p10_repeated_no_clobber: append hygiene — repeated drills do not overwrite prior ledger objects.

Each test must tolerate multiple legitimate implementations provided trace and ledger invariants hold.

### Drafting guardrails
Keep instruction.md constraint-complete about formal properties and artifacts without naming fix-path files, replay-phase ordering bugs, or oracle symbols. Ban instruction nouns from fix-path code and test identifiers. No boolean readiness fields in planned outputs. Strip corrective vocabulary from environment comments per GX1.

### Triviality Ledger
- Bumping generation counters alone cannot pass: manifest authority and cursor idempotence tests remain red until reconcile and persist logic align.
- Editing only summary_mux formatting cannot pass: digest-chain tests still fail until mux_sel treats manifests as authoritative.
- Truncating cursors aggressively fails idempotence and restart-boundary cases even if probes look green—forces coupled sealing and authority reasoning.
- Overwriting prior outputs or ignoring session high-water fails append, anchor, and cross-invocation floor cases.

### Per-gate Pitfall Inventory
- RC1/RC2: Spread substantive edits across lane_mux, stamp_mux, and mux_sel; avoid one-file oracle rewrites.
- RC6/GX9/GX10: Instruction states properties and schemas without scenario→key answer tables or polarity contradictions.
- RC7/GX3: Oracle must encode real cross-module coordination, not inflated heredocs with trivial deltas.
- GX1/GX4/GX5: Keep tested derivations in environment code and formal_rules.md, not prose-only or test-only literals.
- GX2: Avoid bulk replace templates whose semantic delta is near-zero.
- CR1/CR2: Honor symbol table and flipping-point contract concentration cap 0.5 across three roots.

### Initial Draft Commitments
- task.toml
- instruction.md
- output_contract.toml
- construction_manifest.json
- tests/test.sh
- tests/test_outputs.py
- solution/solve.sh
- environment/Dockerfile
- environment/k7w/lane_mux.cpp
- environment/m9p/stamp_mux.cpp
- environment/n4q/mux_sel.cpp
- environment/tools/summary_mux.cpp
- environment/pilot/entry.cpp
- environment/engine/pipeline.cpp
- environment/engine/session_registry.cpp
- environment/docs/formal_rules.md
- environment/schemas/report_row.schema.json
- environment/schemas/ledger_run.schema.json
- environment/fixtures/crash_profiles/profile_a.json
- environment/fixtures/crash_profiles/profile_b.json
- environment/fixtures/crash_profiles/profile_c.json
- environment/state/README
- environment/logging/README
- environment/config/defaults.env

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```
- path: environment/k7w/lane_mux.cpp
  symbol: fn_k2
  kind: function
  signature: fn_k2(buf, mark_a, mark_b)
  purpose: Advances replay cursor state and records sealed tail segments for recovery reruns.
- path: environment/m9p/stamp_mux.cpp
  symbol: fn_h8
  kind: function
  signature: fn_h8(ctx, gen_a, gen_b)
  purpose: Computes active generation stamps after restart boundaries using registry snapshots.
- path: environment/n4q/mux_sel.cpp
  symbol: fn_w4
  kind: function
  signature: fn_w4(rows, tag_p, tag_q)
  purpose: Folds competing observation rows into manifest-chain digests used by verification.
```

#### flipping_point_contract
```
locations:
  - id: A
    path: environment/k7w/lane_mux.cpp
    controls_tests: [test_p1_boundary_monotone_seals, test_p4_rollback_idempotent]
  - id: B
    path: environment/m9p/stamp_mux.cpp
    controls_tests: [test_p3_authority_over_health_probe, test_p8_cross_invocation_floor]
  - id: C
    path: environment/n4q/mux_sel.cpp
    controls_tests: [test_p2_row_digest_matches_rows, test_p9_combined_restart_conflict]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest
```
- path: environment/k7w/lane_buffer.cpp
  kind: module
  rhymes_with: fn_k2
  non_fix_purpose: Buffers ephemeral lane events for offline benchmarks unrelated to sealed recovery tails.
- path: environment/n4q/fold_apply.cpp
  kind: module
  rhymes_with: fn_w4
  non_fix_purpose: Applies offline fold transforms for diagnostics without participating in manifest authority.
- path: environment/n4q/rank_lane.cpp
  kind: module
  rhymes_with: fn_w4
  non_fix_purpose: Ranks diagnostic tuples for support tooling without participating in manifest-chain authority.
```

#### code_forbidden_tokens
```
authoritative, boundaries, cascade, chain, compaction, digests, durability, generation, health, idempotent, ledgers, manifest, namespace, records, recovery, replay, restart, rollback, sealed, segments, summaries, tail, truncate
```
