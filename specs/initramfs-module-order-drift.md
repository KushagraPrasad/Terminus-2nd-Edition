### Decision
GO — repair_existing_system with constraint-complete k4_contract framing, multi-wave carry chain, and cross-surface loader/manifest/journal invariants in a Go early-boot staging pipeline.

### Metadata
- version: 2
- Task name: initramfs-module-order-drift
- Title: Initramfs Module Order Drift
- Category: system-administration
- Task shape: repair_existing_system
- Languages: ["Go", "bash"]
- Difficulty: hard
- Codebase size: small
- Subcategories: ["tool_specific"]
- Tags: ["go", "initramfs", "depmod", "early-boot", "toolchain"]
- Milestones: 0

## Authoring Brief

### Public contract

A Go staging driver under `/app/environment` must regenerate `/app/output/staging_manifest.json`, `/app/output/phase_journal.json`, and `/app/output/loader_trace.json` after outputs are removed. The cold boot profile mis-orders module nodes: loader simulation drops nodes even when the driver status line still reads clean. Fix source under `/app/environment`, rebuild with `/app/environment/scripts/build_driver.sh`, and rerun `/app/environment/run_driver.sh`.

Field semantics, carry chaining, hook gating, journal ordering, replay `rev` stability, and cross-surface availability are in `/app/environment/docs/k4_contract.md`. Stamp derivation aligns with `/app/environment/scripts/stamp_helper.py`.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt derived from Public contract above
- path: output_contract.toml
  role: local output declaration for staging_manifest, phase_journal, loader_trace
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed pytest only (no runtime apt/pip/curl)
- path: tests/test_outputs.py
  role: domain verifier (opaque test_j* names)
- path: solution/solve.sh
  role: oracle applying patch bundle and rebuilding driver
- path: environment/Dockerfile
  role: build definition; pre-install golang, pytest, tmux, asciinema, patch, python3
- path: construction_manifest.json
  role: local authoring artifact mirroring symbol table below

### task_files

- path: environment/cmd/m8_driver/main.go
  role: driver CLI entrypoint
- path: environment/internal/driver/pipeline.go
  role: multi-wave driver coordinating carry chain and output emission (fix frontier C)
- path: environment/forge/carry_mix.go
  role: carry token selection for P3 stamp binding (fix frontier B)
- path: environment/forge/index_map.go
  role: dependency index views and stamp derivation (fix frontier A)
- path: environment/lane/phase_core.go
  role: staged copy phases for firmware blobs and kernel objects (fix frontier D)
- path: environment/frame/orchestrator.go
  role: hook script scheduling after blob visibility markers (fix frontier E)
- path: environment/internal/loader/sim.go
  role: loader simulation and read_order emission
- path: environment/internal/manifest/emit.go
  role: staging_manifest row emission
- path: environment/internal/ledger/store.go
  role: decoy epoch ledger persistence helpers
- path: environment/internal/replay/gate.go
  role: decoy replay gate persistence
- path: environment/forge/index_lane.go
  role: decoy offline dependency graph visualization
- path: environment/lane/phase_lane.go
  role: decoy copy timing buffers
- path: environment/frame/bridge_orchestrator.go
  role: bridge orchestration helper
- path: environment/lane/bridge_phase.go
  role: bridge phase lane helper
- path: environment/forge/bridge_index.go
  role: bridge index helper
- path: environment/fixtures/waves/wave_a.json
  role: first wave fixture bundle
- path: environment/fixtures/waves/wave_b.json
  role: second wave fixture bundle
- path: environment/fixtures/waves/wave_c.json
  role: third wave fixture bundle
- path: environment/fixtures/k6preserve/note_a.txt
  role: immutable witness note (must not be edited)
- path: environment/fixtures/k6preserve/note_b.txt
  role: immutable witness note (must not be edited)
- path: environment/data/scratch_lane/operator_hint.txt
  role: scratch lane hint preserved across reruns
- path: environment/state/epoch_ledger.json
  role: replay rev bookkeeping sidecar
- path: environment/state/replay_gate.json
  role: replay gate sidecar
- path: environment/docs/k4_contract.md
  role: carry, stamp, hook, journal, and replay formulas
- path: environment/docs/verifier_notes.md
  role: supplementary verifier orientation (no oracle hints)
- path: environment/schemas/k4_row.schema.json
  role: manifest row JSON schema
- path: environment/scripts/build_driver.sh
  role: go build wrapper for m8_driver
- path: environment/scripts/stamp_helper.py
  role: stamp derivation reference helper
- path: environment/run_driver.sh
  role: driver wrapper with ROOT/BIN/exec literals
- path: environment/go.mod
  role: Go module definition

### fix_frontier

- count: 5
- distribution: forge/, lane/, frame/, internal/driver module roots
- naming_policy: Opaque symbols from construction manifest symbol_table only
- forbidden_stems: [incremental, earlyboot, staging, cold, boot, kernel, witness, scratch_lane, rebuild, regenerates]
- helpers_policy: Decoys may rhyme structurally; oracle must not touch decoy bodies
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [stamp digests, carry chain equality, journal lane ordering, avail_metric cross-checks, loader read_order, replay rev stability]
- forbidden_assertion_styles: [boolean answer keys, scenario->field->expected tables, fields ending in _ok/_valid/_passes]

### task_shape

- type: repair_existing_system
- instruction_framing: constraint-complete
- hardness_source: cross-surface early-boot pipeline correctness
- collapse_risk: patching one emitter while leaving carry, hook gating, or journal ordering inconsistent

### category_profile

- challenge_family: initramfs module ordering and early-boot staging
- profile_name: tool_specific
- allowed_instruction_disclosures: wave fixture order, k4_contract formulas, build_driver/run_driver commands, field semantics with means cues, ROOT/BIN/exec literals, k6preserve/scratch_lane preservation
- forbidden_instruction_leaks: Oracle patch recipes, fix-path symbol names, exact byte-level golden JSON, per-wave expected stamp tables
- category_specific_hardness_bar: Carry chain, hook gating, journal ordering, loader simulation, and replay rev must coordinate across three waves
- category_specific_verifier_risks: False greens from status=clean while loader_trace shows avail_metric 0.0; single-surface JSON edits; fixture tampering
- coverage_role: Strengthens tool_specific via initramfs module-order drift with multi-wave carry and cross-surface invariants

### difficulty_mechanism_plan

- mechanisms: [false_green_intermediate_states, cross_file_cross_format_invariants, stateful_multi_step_dependencies, environment_specific_cli_semantics, deceptive_but_valid_local_evidence]
- adversarial_layers_count: 5
- fairness_guardrails: Every layer is discoverable from k4_contract.md, wave fixtures, state sidecars, and regenerated outputs
- mechanism: false_green_intermediate_states
  placement: driver emits status=clean while loader_trace shows avail_metric 0.0 for mis-ordered nodes
  why_model_misses_it: Models trust validation-only status lines and skip cross-surface loader_trace checks
  fairness_guardrail: Instruction and k4_contract require manifest/journal/loader agreement
- mechanism: cross_file_cross_format_invariants
  placement: staging_manifest rows, phase_journal lane codes, and loader_trace read_order must agree on ordering and availability
  why_model_misses_it: Models patch one emitter while leaving hook gating or journal blob/object ordering inconsistent
  fairness_guardrail: k4_contract documents each surface and the cross-check rules
- mechanism: stateful_multi_step_dependencies
  placement: carry token folds across wave_a, wave_b, and wave_c into P3 stamp binding and replay rev bookkeeping
  why_model_misses_it: Models fix the final wave only and ignore carry propagation from earlier profiles
  fairness_guardrail: Carry formula and wave order are explicit in k4_contract.md
- mechanism: environment_specific_cli_semantics
  placement: P3 dependency sort uses fixture weights; hook_gen must equal blob_epoch before hooks commit; build_driver/run_driver wrappers use ROOT/BIN/exec literals
  why_model_misses_it: Models apply lexicographic sorting or unconditional hook scheduling instead of profile-specific rules
  fairness_guardrail: P3 tie-break and hook gating conditions are documented in k4_contract.md
- mechanism: deceptive_but_valid_local_evidence
  placement: status=clean driver line and locally valid manifest rows tempt models to skip loader_trace cross-checks
  why_model_misses_it: Models trust the first green surface and stop before verifying journal lane ordering or carry binding
  fairness_guardrail: Instruction states all three JSON outputs must agree per k4_contract cross-surface rules

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: Systems engineer reproduces failing loader_trace/manifest mismatch using k4_contract and wave fixtures only
- shortcut_audit: Block hand-written JSON under /app/output, fixture edits under k6preserve/waves, and shim binaries
- ablation_plan: Remove carry layer, then hook gating layer, then journal ordering layer; expect monotonic verifier drop
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=Part E Hard threshold on worst-model accuracy

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt=1 only when all pytest checks pass

### subtype_milestone_plan

- subcategories: [tool_specific]
- milestone_count: 0
- sequential_dependency: Single repair task across multi-wave driver pipeline
- local_only_data: true
- sidecar_or_protocol_notes: Single-container local verifier; Go driver and pytest baked in Dockerfile with offline runtime

### satisfiability_risk

- rc2_planned_name_risk: low — opaque fix-path symbols and code_forbidden_tokens precommitted in construction_manifest.json
- gx9_contract_risk: low — contract uses stamps, lane codes, and structured rows, not boolean verdict tables
- cr1_symbol_frontier_risk: medium — five fix roots across forge/lane/frame/internal/driver with decoys
- hidden_contract_risk: medium — carry formula, hook gating, and journal ordering live in k4_contract.md cross-artifact behavior

### actionability_plan

- verifier_command_visible: build_driver.sh, run_driver.sh, and pytest documented in instruction.md
- source_fix_intent_visible: yes — fix Go sources under /app/environment; static output writes insufficient
- generated_output_rule_visible: three JSON outputs under /app/output must be pipeline-regenerated
- exact_formula_home: environment/docs/k4_contract.md for carry, stamp, hook, and replay formulas
- schema_home: instruction.md plus environment/docs/k4_contract.md

### waiver_plan

- waivers_expected: no
- waiver_rationale: Hardness from coupled early-boot pipeline behavior, not harness brittleness; collapse WARN on frontier concentration is informational

### reference_pattern

- reference_task_id:
- justification_if_none: No promoted reference in docs/reference_tasks/index.json matches initramfs module-order drift with multi-wave carry and cross-surface loader simulation

### realism_source

- source_type: real_system
- evidence_basis: production early-boot staging pattern
- upstream_or_synthetic_rationale: Initramfs module dependency ordering, depmod-style weight sorting, and multi-wave firmware staging mirror production bring-up failures
- minimization_preserves: Causal coupling across carry chain, hook gating, journal ordering, and loader simulation
- synthetic_exception_review: not required

### Failure topology

The Go staging driver fails verification for different root causes depending on wave and profile. Index map stamping can satisfy local manifest shape while carry_mix still binds the wrong token into P3 stamps. Phase core may emit journal blobs in the wrong lane order while orchestrator schedules hooks before blob_epoch matches hook_gen. Pipeline carry advancement can fix wave_c locally while earlier wave carry never propagates into later stamp binding. Loader simulation can report status=clean while read_order omits mis-ordered nodes. No single subsystem edit satisfies all three waves and cross-surface manifest/journal/loader agreement.

### Environment shape

- `environment/cmd/m8_driver/` — driver CLI entrypoint
- `environment/internal/driver/` — multi-wave pipeline and carry advancement
- `environment/forge/` — carry selection and index map derivation
- `environment/lane/` — phase execution and decoy timing buffers
- `environment/frame/` — hook orchestration
- `environment/internal/loader/` — loader simulation
- `environment/internal/manifest/` — manifest emission
- `environment/fixtures/waves/` — wave_a, wave_b, wave_c fixture bundles
- `environment/fixtures/k6preserve/` — immutable witness notes
- `environment/data/scratch_lane/` — operator hint preserved across reruns
- `environment/state/` — epoch ledger and replay gate sidecars
- `environment/docs/` — k4_contract and verifier notes

### Required artifacts

Step 2b creates: `task.toml` (`allow_internet = false`), `instruction.md`, `output_contract.toml`, `tests/test.sh`, `tests/test_outputs.py`, `solution/solve.sh`, `environment/Dockerfile` (Go toolchain + pytest baked in), all task_files above, and `construction_manifest.json` matching the symbol table.

### Test plan

1. `test_j1` — m8_driver is a native ELF executable invoked via run_driver.sh literals
2. `test_j2` — staging output includes expected profile_key/object_name pairs with correct stamp shape
3. `test_j3` — epoch_ledger rev unchanged when manifest fingerprint unchanged across reruns
4. `test_j4` — loader_trace avail_metric agrees with staging_manifest and hook gating
5. `test_j5` — rolling digest propagates across sequential fixture bundles into P3 stamps
6. `test_j6` — phase_journal lists blob lane B before object lane O per segment
7. `test_j7` — rebuild and rerun regenerate all three outputs from fixed sources
8. `test_j8` — k6preserve notes and scratch_lane hint remain intact across reruns

### Drafting guardrails

Do not place instruction nouns on fix-path symbols or directories. Do not embed oracle hints in environment comments. Keep carry/stamp/hook formulas in k4_contract.md, not only in tests. Ensure driver diagnostics never name EffectiveCarry, fn_j2, fn_j3, fn_j4, or advanceCarryFromRows. Avoid boolean verdict fields in output JSON. Do not publish per-wave expected stamp tables in instruction.md.

### Triviality Ledger

- Fixing only loader sim read_order passes local loader checks but fails carry-chain tests because P3 stamps still bind the wrong rolling carry from earlier waves.
- Hand-written staging_manifest.json can match stamp shape locally but cross-surface tests fail because phase_journal lane ordering and loader_trace avail_metric disagree.
- Patching only phase_core journal ordering passes test_j6 locally but test_j4 fails because hook_gen never equals blob_epoch under orchestrator scheduling.
- Lexicographic dependency sorting passes wave_a smoke but P3 weight-based tie-break in k4_contract fails wave_c ordering tests.

### Per-gate Pitfall Inventory

- RC1: Oracle must perform substantive cross-file Go edits via patch bundle, not byte-identical rewrites.
- RC2: Fix-path symbols stay opaque; instruction nouns banned via code_forbidden_tokens; paths use forge/lane/frame/internal not staging/boot/kernel/witness.
- RC6: Instruction stays constraint-complete with field semantics means cues, not spec-complete golden JSON tables.
- RC7/GX3: Oracle solve.sh applies patches then rebuilds; substantive coordination exceeds trivial one-liner.
- CR1: Five fix roots required; decoys stay off oracle path.
- GX9: Do not enumerate per-wave stamp values in instruction.md.
- GX6: Limit causal connective chains that reveal patch order across subsystems.
- Dockerfile: golang bookworm image must expose go/gofmt via symlinks, profile.d, bashrc, and /etc/environment for tmux/login shells.

### Initial Draft Commitments

- task.toml, instruction.md, output_contract.toml, construction_manifest.json
- tests/test.sh, tests/test_outputs.py (opaque test_j* names)
- solution/solve.sh, solution/patches/all-fixes.patch
- environment/Dockerfile, environment/go.mod, environment/run_driver.sh
- environment/cmd/m8_driver/main.go
- environment/internal/driver/pipeline.go, environment/internal/loader/sim.go, environment/internal/manifest/emit.go
- environment/forge/carry_mix.go, environment/forge/index_map.go, environment/forge/index_lane.go, environment/forge/bridge_index.go
- environment/lane/phase_core.go, environment/lane/phase_lane.go, environment/lane/bridge_phase.go
- environment/frame/orchestrator.go, environment/frame/bridge_orchestrator.go
- environment/fixtures/waves/wave_a.json, environment/fixtures/waves/wave_b.json, environment/fixtures/waves/wave_c.json
- environment/fixtures/k6preserve/note_a.txt, environment/fixtures/k6preserve/note_b.txt
- environment/data/scratch_lane/operator_hint.txt
- environment/state/epoch_ledger.json, environment/state/replay_gate.json
- environment/docs/k4_contract.md, environment/docs/verifier_notes.md
- environment/schemas/k4_row.schema.json
- environment/scripts/build_driver.sh, environment/scripts/stamp_helper.py
