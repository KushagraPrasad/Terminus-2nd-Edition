### Decision

GO — Attempt 1 (validated). Bank-ready seed `tls-session-cache-divergence` passes idea validation on a local C session cache daemon implementation, framed as a **repair_existing_system** task under the **security** category. Five mandated discoveries, binary session record store + resumption ledger + crash checkpoint journal consistency logic, five-location flipping-point contract, and symptoms-only public obligations without leaking the epoch update order or hash truncation logic.

### Metadata

- version: 2
- Task name: tls-session-cache-divergence
- Title: TLS Session Cache Divergence
- Category: security
- Task shape: repair_existing_system
- Languages: ["c", "bash"]
- Difficulty: hard
- Codebase size: minimal (0–20 files under environment/)
- Subcategories: ["tool_specific"]
- Tags: ["tls", "session-cache", "key-rotation", "cache-invalidation", "state-recovery", "c"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires editing 5 C modules across 5 distinct files (epoch_fence.c, ticket_vault.c, resumption_ledger.c, expiry_janitor.c, journal_writer.c) to solve. A single-file fix fails to reconcile state.
- Inconsistent resumption epoch tracking and journal recovery validity are verified by different tests, ensuring that simple NOP or static outputs cannot pass.

### Per-gate Pitfall Inventory
- **Collapse Gate**: Shipped code symbols map to logical domain boundaries; no keywords overlap with the instruction vocabulary.
- **Predictability Gate (RC2)**: Kept file names generic (ticket_vault, epoch_fence, resumption_ledger) to prevent predicting the fix path, with rc2 waivers applied for the main daemon domain names.
- **Hidden Invariants**: Python verifier assertions query active sessions and ledger entries dynamically rather than hardcoding static values.

### Initial Draft Commitments
- Shipped code contains five buggy files: ticket_vault.c, epoch_fence.c, resumption_ledger.c, expiry_janitor.c, journal_writer.c.
- Verifier tests assert session cache invalidation, ID collision resilience, ledger attribution epoch correctness, TTL sweep sweep cleanup, and state checkpoint recovery fidelity.

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, per-target facet answer tables, or narrative causal chains that name fix coordinates.

### Public contract

A local offline TLS session cache daemon is provided. Developers report inconsistent behavior where:
- Stale sessions survive key rotation (sessions from prior epoch remain active).
- Resumption ledger attributes resumptions to the current system epoch rather than the epoch under which the session was created.
- Checkpoint recovery inflates session count by forcing invalid/swept sessions back to valid status.
- Two sessions sharing the first 16 bytes of their ID but differing in the next 16 bytes are treated as duplicates.

No network access is available.

The agent must determine why the daemon exposes inconsistent session metadata and repair the implementation under `/app/src` so all operations maintain consistent views without breaking session expiry or epoch guarantees.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "security"`
- path: instruction.md
  role: natural public task prompt (symptoms-only public instruction)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation, permutation, and pipeline traps
- path: solution/solve.sh
  role: oracle applying bug patches and locked rebuild
- path: environment/Dockerfile
  role: build definition; pre-install C compiler, python3, pytest, and locked deps
- path: construction_manifest.json
  role: local authoring artifact mirroring Construction manifest below

### task_files

- path: environment/src/main.c
  role: CLI dispatcher parsing store/resume/rotate/sweep/checkpoint/recover/report commands
- path: environment/src/ticket_vault.c
  role: flat-file session record store maintaining session list and duplicate checking
- path: environment/src/epoch_fence.c
  role: tracks key epoch and handles session invalidation on rotation
- path: environment/src/resumption_ledger.c
  role: logs successful session resumptions
- path: environment/src/expiry_janitor.c
  role: cleans up expired sessions using creation time and TTL
- path: environment/src/journal_writer.c
  role: writes checkpoints and recovers session store from journal
- path: environment/src/Makefile
  role: make build script compiling cache_daemon binary
- path: environment/docs/invariants.md
  role: details session validity and epoch attribution rules
- path: environment/docs/data_formats.md
  role: documents binary record structures

### fix_frontier

- count: 5
- distribution: ticket_vault.c, epoch_fence.c, resumption_ledger.c, expiry_janitor.c, journal_writer.c
- naming_policy: explicit nouns banned from function signatures and structures
- forbidden_stems: ["rotation", "key", "fix", "ttl", "revival"]
- helpers_policy: no helper renames or additions
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 8
- preferred_assertion_styles: JSON file output keys, exit codes
- forbidden_assertion_styles: hardcoded database state checks

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: Inconsistent state synchronization between binary file storage, epoch state, ledger, and journal.
- collapse_risk: Disclosing the exact file coordinates or bug mechanisms collapses the task to simple line edits.

### category_profile

- challenge_family: tls_session_cache_divergence
- profile_name: security_authority_split
- allowed_instruction_disclosures: observable CLI behavior (store, resume, report), directory layout, output schema
- forbidden_instruction_leaks: specific bug files, hash truncation details, incorrect rotation epoch parameter
- category_specific_hardness_bar: Key rotation fence, session vault, resumption ledger, and recovery journal must all coordinate
- category_specific_verifier_risks: mock-only checks, single-run tests, static cache fixes
- coverage_role: Adds TLS session caching and epoch state synchronization coverage

### satisfiability_risk

- rc2_planned_name_risk: low — generic file and module names
- gx9_contract_risk: low — verification is based on CLI output and output files
- cr1_symbol_frontier_risk: low — five files with precise fixes
- hidden_contract_risk: low — all rules verified via standard daemon behavior

### actionability_plan

- verifier_command_visible: make -C /app/src
- source_fix_intent_visible: yes
- generated_output_rule_visible: report outputs and storage files
- exact_formula_home: invariants.md
- schema_home: instruction.md

### waiver_plan

- waivers_expected: true
- waiver_rationale: Non-canonical Docker base (golang:bookworm) utilized to provide build-essentials (gcc) without apt runtime install

### reference_pattern

- justification_if_none: This task is a novel C session cache implementation, designed from scratch.

### realism_source

- source_type: synthetic-minimized
- evidence_basis: Based on real-world session resumption invalidation and rotation race conditions seen in OpenSSL/nginx CVEs.
- upstream_or_synthetic_rationale: Replicates real session cache key-rotation race conditions in a minimized flat binary file setup.
- minimization_preserves: Cache invalidation, resumption ledger attribution, and crash recovery validity states.
- synthetic_exception_review: None.

### Failure topology

The local TLS session cache is serving resumption tokens. The vault lookup uses a truncated 16-byte comparison instead of 32-byte matching, leading to collisions for IDs sharing prefixes. Key rotation invalidates the wrong epoch, leaving old sessions valid. Resumption attributes events to the current system epoch instead of the session's negotiation epoch. The sweep janitor ignores per-session TTLs, using a static default. Journal recovery reactivates invalid sessions by overriding their validity status. The solver must coordinate edits across all 5 files to establish consistency.

### Environment shape

A single-container environment running a lightweight C daemon. Code lives under `/app/src`. Data is stored in `/app/data/` using flat binary files.

### Required artifacts

Standard TB3 task tree under `tasks/tls-session-cache-divergence/`: instruction.md, task.toml, output_contract.toml, construction_manifest.json, Dockerfile, tests/test.sh, tests/test_outputs.py (8 tests), solution/solve.sh, and source codebase files.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, cross_file_cross_format_invariants, stateful_multi_step_dependencies, buried_local_constraints
- adversarial_layers_count: 4
- fairness_guardrails: Instructions document the 3-way consistency rule; no timing or latency thresholds.
- mechanism: false_green_intermediate_states
  placement: old-epoch sessions remain valid after rotation, allowing stale resumptions to succeed
  why_model_misses_it: model misses that the rotate command succeeded dynamically but did not invalidate the vault records
  fairness_guardrail: test suite asserts stale sessions are explicitly rejected after rotate
- mechanism: cross_file_cross_format_invariants
  placement: epoch_fence epoch count must match valid session epochs and resumption ledger records
  why_model_misses_it: model fixes key rotation but forgets to propagate session negotiation epoch to ledger logs
  fairness_guardrail: ledger checks assert correct attribution under active rotation
- mechanism: stateful_multi_step_dependencies
  placement: journal recovery restores invalid status; rerun stability check asserts binary layout consistency
  why_model_misses_it: model fixes memory layout but leaks padding bytes or incorrectly overrides invalid flag on reload
  fairness_guardrail: tests inspect binary format outputs and run recovery checkpoints
- mechanism: buried_local_constraints
  placement: per-session TTL values override DEFAULT_TTL in janitor sweeps
  why_model_misses_it: model relies on default TTL matching typical session lifetime instead of record-level TTL
  fairness_guardrail: invariants.md specifies custom TTL lookup rule

### calibration_plan

```yaml
oracle_runs: 3
no_op_runs: 3
target_agent_runs: 20
comparator_agent_runs: 20
human_sanity: Completed to verify C build and test coverage.
shortcut_audit: >
  static JSON output → fails verifier rerun
  patch one file only → other invariant tests fail
ablation_plan: >
  Remove each mechanism one at a time and confirm difficulty drops.
pass_rate_target:
  hard_max_pct: 20
  too_easy_threshold_pct: 80
  basis: Part E worst-model accuracy on platform (GPT-5.5 + Claude Opus 4.8, Jun 12 2026)
```

### verifier_scoring_plan

- metrics: functional_correctness=0.6, hidden_invariants=0.2, state_hygiene=0.1, interface_correctness=0.05, deliverable_completeness=0.05
- overall_threshold: 1.0
- reward_output: reward.txt
- binary_threshold_rule: all functional correctness tests must pass

### subtype_milestone_plan

- subcategories: ["tool_specific"]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: requires C compiler (gcc) and python3/pytest

### Drafting guardrails

Instruction must only mention CLI symptoms and public specifications. It must not reference specific C structures, function names, or internal file formats.

### Triviality Ledger

- Static mock responses fail `test_rerun_determinism` because of binary layout differences.
- Fixing the epoch rotation without fixing ledger attribution fails `test_resume_negotiated_val`.
- Fixing the vault lookup without fixing journal validity override fails `test_checkpoint_validity`.
- Fixing default TTL without custom TTL sweep fails `test_cleanup_custom_ttl`.

### Per-gate Pitfall Inventory

- RC1: Wholesale replace is blocked; changes must distribute across the 5 files.
- RC2: Ensure test names and symbols avoid forbidden tokens.
- RC3: Instruction is symptoms-only.
- CR1: Symbol table maps exactly to the 5 buggy functions.

### Initial Draft Commitments

- tasks/tls-session-cache-divergence/task.toml
- tasks/tls-session-cache-divergence/instruction.md
- tasks/tls-session-cache-divergence/output_contract.toml
- tasks/tls-session-cache-divergence/construction_manifest.json
- tasks/tls-session-cache-divergence/tests/test.sh
- tasks/tls-session-cache-divergence/tests/test_outputs.py
- tasks/tls-session-cache-divergence/solution/solve.sh
- tasks/tls-session-cache-divergence/environment/Dockerfile
- tasks/tls-session-cache-divergence/environment/src/main.c
- tasks/tls-session-cache-divergence/environment/src/ticket_vault.c
- tasks/tls-session-cache-divergence/environment/src/epoch_fence.c
- tasks/tls-session-cache-divergence/environment/src/resumption_ledger.c
- tasks/tls-session-cache-divergence/environment/src/expiry_janitor.c
- tasks/tls-session-cache-divergence/environment/src/journal_writer.c
- tasks/tls-session-cache-divergence/environment/src/Makefile
- tasks/tls-session-cache-divergence/environment/docs/invariants.md
- tasks/tls-session-cache-divergence/environment/docs/data_formats.md
