### Decision
GO — repair_existing_system with inline instruction contract, clean versus incremental rebuild drift, and cross-surface helper invariants across Go buildsys/tools packages.

### Metadata
- version: 2
- Task name: abi-rebuild-drift
- Title: ABI Rebuild Drift
- Category: software-engineering
- Task shape: repair_existing_system
- Languages: ["Go"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["abi", "rebuild", "linking", "integrity", "debugging", "determinism"]
- Milestones: 0

## Authoring Brief

### Public contract

A Go ABI helper workspace under `/app/environment` must rebuild `/app/environment/bin/abictl` and regenerate `/app/environment/out/trace.log` via `emit-trace`. Clean versus incremental tagging disagrees on identities, object ordering, marker decoding, unit projection, mux metadata, and route tracing. Fix source under `/app/environment`; static edits or hand-written trace files are insufficient.

The public instruction states rebuild commands, pytest `--ctrf` verification, behavioral invariants for OpA, DeltaQ, PhaseC, JoinT, MuxH, and trace.log emission, plus fixture literals. Digest formulas and helper surface names live in `/app/environment/data/NOTE.txt` as implementation reference material discoverable while reading the codebase.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt with inline operational contract
- path: output_contract.toml
  role: local output declaration for trace.log and abictl surface
- path: construction_manifest.json
  role: local authoring artifact mirroring symbol table
- path: tests/test.sh
  role: verifier entrypoint; Dockerfile-baked pytest only with rc=$? reward footer
- path: tests/test_outputs.py
  role: domain verifier against abictl CLI helpers
- path: solution/solve.sh
  role: oracle rewriting buildsys and tools helpers
- path: environment/Dockerfile
  role: pinned Go runtime, tmux, asciinema, offline pytest venv

### task_files

- path: environment/buildsys/regen_stage.go
  role: OpA stable identity and header turnover (fix frontier A)
- path: environment/buildsys/link_plan.go
  role: PhaseC object precedence and tail ranking (fix frontier B)
- path: environment/buildsys/target_pick.go
  role: JoinT unit projection (fix frontier C)
- path: environment/buildsys/meta_bus.go
  role: MuxH deep copy and lane digest (fix frontier D)
- path: environment/tools/probe_scan.go
  role: DeltaQ probe parsing and sidecar tolerance (fix frontier E)
- path: environment/buildsys/canon.go
  role: canonical text helpers touched by oracle
- path: environment/buildsys/cache_lane.go
  role: GateB helper used by mux tests
- path: environment/buildsys/header_stamp.go
  role: AxisM stamp helper
- path: environment/buildsys/route_stage.go
  role: TraceRoute emission helper
- path: environment/tools/checksum_lane.go
  role: object constant provider
- path: environment/tools/path_hints.go
  role: blob and seed constant provider
- path: environment/tools/report_emit.go
  role: WriteBlob helper surface
- path: environment/runtime/
  role: correct runtime package; must not be edited
- path: environment/cmd/abictl/main.go
  role: CLI entrypoint and emit-trace pipeline
- path: environment/data/CATALOG.txt
  role: catalog units for JoinT/trace projection
- path: environment/data/NOTE.txt
  role: helper digest formulas and fixture naming reference
- path: environment/docs/verifier_notes.md
  role: pytest ctrf and digest cross-check notes
- path: environment/scripts/digest_ref.py
  role: Python hashlib reference for verifier expectations

### fix_frontier

- count: 5
- distribution: environment/buildsys (4 helpers) and environment/tools (DeltaQ)
- naming_policy: Published helper names in NOTE.txt only; instruction avoids fix-path tokens
- forbidden_stems: [broken, buggy, fix_me, golden, expected, drift]
- helpers_policy: runtime package stays correct; decoys limited to constant providers
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [JSON field equality, tuple probe pairs, ordered object lists, trace line sequences, digest recomputation]
- forbidden_assertion_styles: [hand-written trace.log only checks, existence-only CLI smoke]

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only about implementation patch
- hardness_source: cross-helper invariant repair under clean versus incremental tagging
- collapse_risk: patching one helper while leaving probe parsing or mux deep-copy broken

### category_profile

- challenge_family: deterministic build helper repair
- profile_name: software_engineering_debugging
- allowed_instruction_disclosures: rebuild commands, pytest --ctrf, behavioral invariants, fixture literals, mux field semantics
- forbidden_instruction_leaks: exact patch hunks, oracle transcripts, helper function names on fix path in instruction.md
- category_specific_hardness_bar: Five helper surfaces must agree across clean/incremental modes and regenerated trace output
- category_specific_verifier_risks: Static trace edits, runtime-only fixes, single-helper patches that pass one CLI subcommand
- coverage_role: Exercises cross-file Go helper repair with probe fixtures and catalog projection

### difficulty_mechanism_plan

- mechanisms: [false_green_intermediate_states, cross_file_cross_format_invariants, deceptive_but_valid_local_evidence, environment_specific_cli_semantics]
- adversarial_layers_count: 4
- fairness_guardrails: Every layer is discoverable from NOTE.txt, CATALOG.txt, probe fixtures, and regenerated CLI helper output
- mechanism: false_green_intermediate_states
  placement: incremental OpA calls return different stable_id than clean calls for the same canonical unit/seed pair
  why_model_misses_it: Models patch only the clean path or only normalize casing on one mode tag and assume incremental tagging is equivalent
  fairness_guardrail: Instruction states clean and incremental must share one rebuild identity
- mechanism: cross_file_cross_format_invariants
  placement: buildsys link_plan.PhaseC ordering must agree with tools probe_scan.DeltaQ parsing and meta_bus.MuxH deep-copy semantics
  why_model_misses_it: Models fix one helper package while leaving cross-file object precedence or sidecar parsing inconsistent across buildsys and tools
  fairness_guardrail: NOTE.txt documents each helper surface and the cross-check rules for multi-component interaction
- mechanism: deceptive_but_valid_local_evidence
  placement: malformed ABI markers and comment-tolerant sidecar key-value fields tempt models to trust the wrong left/right pair
  why_model_misses_it: Models read sidecar metadata before the first valid blob marker or mishandle comment-tolerant left/right fields
  fairness_guardrail: NOTE.txt states first valid ABI marker wins and documents sidecar tolerance rules
- mechanism: environment_specific_cli_semantics
  placement: join_t projection, trace_route emission, and mux lane digest depend on canonical text rules and deep-copied nested object lists
  why_model_misses_it: Models apply naive sorting or shallow-copy metadata and miss stale nested objects after caller mutation
  fairness_guardrail: Instruction documents mux deep-copy and JoinT projection behavior inline

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: Build engineer reproduces identity drift and probe ordering failures using NOTE.txt and fixture blobs only
- shortcut_audit: Block hand-written trace.log, static binary swaps without go build, and runtime package edits
- ablation_plan: Remove canonical identity layer, then probe parsing layer, then object ranking layer; expect monotonic verifier drop
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=Part E Hard threshold on worst-model accuracy

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt=1 only when all pytest checks pass

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: Single repair task across buildsys and tools helper packages
- local_only_data: true
- sidecar_or_protocol_notes: Single-container local verifier; Go helpers and pytest baked in Dockerfile with offline runtime

### satisfiability_risk

- rc2_planned_name_risk: low — helper package names live in NOTE.txt, not instruction nouns on fix symbols
- gx9_contract_risk: low — instruction lists fixture literals without per-test numeric answer tables
- cr1_symbol_frontier_risk: medium — five helper files across two package roots
- hidden_contract_risk: low — operational contract inline in instruction.md; digest formulas in NOTE.txt

### actionability_plan

- verifier_command_visible: go build, emit-trace, and pytest with --ctrf documented in instruction.md
- source_fix_intent_visible: yes — fix Go sources under /app/environment; static output writes insufficient
- generated_output_rule_visible: trace.log must be pipeline-regenerated after helper fixes
- exact_formula_home: /app/environment/docs/helper_contract.rst for digest and ranking formulas
- schema_home: instruction.md for operational contract; helper_contract.rst for digest reference

### waiver_plan

- waivers_expected: no
- waiver_rationale: Hardness from coupled helper behavior, not harness brittleness

### reference_pattern

- reference_task_id:
- justification_if_none: No promoted reference task matches Go ABI helper rebuild drift with clean versus incremental identity disagreement and probe sidecar traps

### realism_source

- source_type: real_system
- evidence_basis: build-system debugging pattern
- upstream_or_synthetic_rationale: Incremental rebuild tagging drift across canonicalization, probe parsing, link ordering, and trace emission mirrors real ABI helper integration failures
- minimization_preserves: Cross-helper clean/incremental invariants and regenerated trace grading
- synthetic_exception_review: not required

### Triviality Ledger

- Patching only OpA clean mode passes one identity test but incremental casing drift still fails the matrix.
- Trusting sidecar left/right pairs before the first valid blob marker passes malformed captures locally but fails DeltaQ ordering tests.
- Hand-writing `/app/environment/out/trace.log` without emit-trace fails trace projection even when individual CLI subcommands look correct.
- Shallow-copy mux metadata passes immediate packet shape but fails post-mutation deep-copy checks.

### Per-gate Pitfall Inventory

- RC1: Oracle must rewrite helper logic across buildsys and tools, not revert a single flag.
- RC2: Instruction avoids buildsys/tools path tokens and helper symbol names; NOTE.txt carries published helper names only.
- RC6: Instruction stays symptoms-only; digest recipes remain in NOTE.txt not instruction.md.
- RC7: Oracle solve.sh substantive heredoc writes exceed trivial LOC floor.
- GX9: Do not enumerate per-test stable_id values in instruction.md.
- spec_gap_detector: mux field semantics need definition cues inline in instruction.md.
- post_disclosure_collapse: keep digest formulas in NOTE.txt; operational contract inline in instruction.md.
- sandbox_risk_gate: Dockerfile must pre-install tmux and asciinema to avoid AgentSetupTimeoutError.

### Initial Draft Commitments

- task.toml, instruction.md, output_contract.toml, construction_manifest.json
- tests/test.sh with rc=$? reward footer, tests/test_outputs.py (test_h01–test_h10)
- solution/solve.sh, solution/oracle/ reference copies
- environment/Dockerfile with tmux, asciinema, offline pytest venv
- environment/buildsys/*.go, environment/tools/*.go, environment/runtime/*.go
- environment/cmd/abictl/main.go, environment/data/CATALOG.txt, environment/data/NOTE.txt
- environment/docs/verifier_notes.md, environment/scripts/digest_ref.py

### collapse_notes

Cross-file helper repair after incremental build failure recovery; cache invalidation semantics across clean versus incremental tagging; multi-component interaction between buildsys and tools packages.

### Test plan

1. test_h01 — clean and incremental OpA identity agreement
2. test_h02 — OpA mode and casing matrix
3. test_h03 — first valid blob marker wins over sidecar
4. test_h04 — comment-tolerant sidecar metadata
5. test_h05 — seeded fallback when marker and sidecar missing
6. test_h06 — object precedence with hash-ranked tail
7. test_h07 — rank seed changes tail only
8. test_h08 — JoinT suffix canonicalization and sort
9. test_h09 — mux deep copy and lane digest
10. test_h10 — trace.log catalog projection
