### Decision
GO — C++ journal replay and recovery repair with coupled emit, fuse, coalesce, store, stitch, and recovery modules.

### Metadata
- version: 2
- Task name: rollback-catchup-race-variant-3-recovery-104
- Title: Rehearsal journal replay recovery
- Category: software-engineering
- Task shape: repair_existing_system
- Languages: ["cpp"]
- Difficulty: medium
- Codebase size: small
- Subcategories: []
- Tags: ["recovery", "journal", "replay", "cpp", "state-machine", "debugging"]
- Milestones: 0

## Authoring Brief

### Public contract
The rehearsal harness under `/app` writes `/app/output/readout.json` and persists checkpoint state under `/app/state/`. Agents rebuild `/app/build/rehearsal`, fix modules under `/app/src/`, and satisfy journal replay, margin carry, seal banner, fuse slab, coalesce ordering, and corruption recovery semantics documented in `instruction.md`.

### difficulty_mechanism_plan

- mechanisms: [rollback_recovery_requirements, cross_file_cross_format_invariants, stateful_multi_step_dependencies, false_green_intermediate_states]
- adversarial_layers_count: 4
- fairness_guardrails: Contract formulas and field semantics are in instruction.md and environment docs; no timing-based hardness
- mechanism: rollback_recovery_requirements
  placement: rollback token ee-t1 clears carry while rx-recover must rebuild head.carry_mux from the last valid journal mux_snapshot
  why_model_misses_it: Models apply the same carry-clearing logic to recovery and rollback, leaving recovery completion false after corruption
  fairness_guardrail: instruction.md contrasts ee-t1 wipe vs rx-recover tail rebuild
- mechanism: cross_file_cross_format_invariants
  placement: fuse labels, mux slab width, lane/vault hex, and blend_mux_print must agree across op_fuse, codec, and digest helpers
  why_model_misses_it: Models fix fuse scatter but leave decorative fuse labels that skew margin mux and lane prints
  fairness_guardrail: instruction documents empty fuse labels and four-byte slabs; digest.py cross-check helper ships in environment
- mechanism: stateful_multi_step_dependencies
  placement: cc-p4 publishes carry_mux into head before dd-s7 replay and ee-t1 rollback scenarios
  why_model_misses_it: Models patch replay idempotence in main.cpp but miss stitch carry publication or partial store_seq advancement rules
  fairness_guardrail: instruction names cc-p4, dd-s7, ee-t1, and rx-recover carry semantics separately
- mechanism: false_green_intermediate_states
  placement: seal phases set banner readiness true without dual_lane_armed and converged eye versus replay-admit slots
  why_model_misses_it: Models remove the initial banner_ready=true default in emit but ignore coalesce wave ordering that drives promotion blocking and span monotonicity flags
  fairness_guardrail: instruction documents banner readiness gating and wave-sorted coalesce flags

### calibration_plan
- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: Engineer reproduces journal append on replay and carry survival after rollback using instruction only
- shortcut_audit: Hand-written readout.json and static JSON edits must fail verifier rebuild
- ablation_plan: Revert single modules (emit, fuse, main persist, recover) and expect isolated test subsets to flip
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=Part E Hard threshold on worst-model accuracy

### verifier_scoring_plan
- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt=1 only when all pytest checks pass

### actionability_plan
- verifier_command_visible: cmake build and pytest via /tests/test.sh documented in instruction.md
- source_fix_intent_visible: yes — fix C++ under /app/src/; static readout insufficient
- generated_output_rule_visible: verifier rebuilds from sources before readout comparison
- exact_formula_home: /app/docs/readout_contract.md for sha256 digests, mod 997 slots, fuse scatter, and persistence field semantics
- schema_home: instruction.md points to /app/docs/readout_contract.md for the operational contract

### reference_pattern
- justification_if_none: No promoted reference in docs/reference_tasks/index.json covers C++ journal replay with margin fuse, seal banner, and corruption recovery across emit, store, and coalesce layers.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt with inline operational contract
- path: output_contract.toml
  role: local output declaration for readout.json and state paths
- path: tests/test.sh
  role: verifier entrypoint; pre-installed pytest with rc=$? reward footer
- path: tests/test_outputs.py
  role: domain verifier rebuilding rehearsal binary and asserting readout semantics
- path: solution/solve.sh
  role: oracle patching emit, fuse, coalesce, store, stitch, recover, and main
- path: environment/Dockerfile
  role: pinned python:3.13-slim-bookworm base; cmake, g++, pytest, tmux, asciinema
- path: construction_manifest.json
  role: local authoring artifact for symbol table and flipping-point contract

### fix_frontier

- count: 7
- distribution: src/ modules for emit, fuse, coalesce, store, stitch, recover, main
- naming_policy: Opaque C++ symbols on the fix path; instruction uses subsystem vocabulary only
- forbidden_stems: [rehearsal, recovery, journal, rollback, replay, margin, fuse_label]
- helpers_policy: lib/near_* decoys and utils/digest.py perform credible adjacent work; oracle must not patch decoy bodies to pass
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [mux digests, lane/vault hex layouts, journal segment counts, carry mux strings, slot reductions mod 997, run digest material]
- forbidden_assertion_styles: [scenario->field->expected tables, answer recital in instruction prose]
