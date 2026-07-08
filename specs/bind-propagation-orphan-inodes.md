### Decision
GO — Attempt 1. Rust bind-propagation debugging task with coupled gate cache, relay flush ordering, and split barrier invariants across a small multi-module driver.

### Metadata
- version: 2
- Task name: bind-propagation-orphan-inodes
- Title: Bind propagation orphan inode reconciliation
- Category: debugging
- Languages: ["rust", "bash"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "debugging", "bind-mount", "state-reconciliation", "inode"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites, or an exhaustive file tree here.

### Public contract
Operators repair `/app/environment` Rust sources so `bash /app/environment/scripts/build_driver.sh` and `bash /app/environment/scripts/run_driver.sh` regenerate aligned manifest, journal, and consumer trace artifacts with zero drift. Contract prose lives in `/app/environment/docs/mount_contract.md` and `/app/environment/schemas/p9_row.schema.json`.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, stateful_multi_step_dependencies, buried_local_constraints, cross_file_cross_format_invariants, rollback_recovery_requirements
- adversarial_layers_count: 5
- fairness_guardrails: published mount contract invariants, wave fixture digests, and deterministic checkpoint replay.
- mechanism: false_green_intermediate_states
  placement: orphan generation floors and observer cache reuse
  why_model_misses_it: agents patch stale-cache detection but still serve superseded observer tuples without evicting rows below the generation floor.
  fairness_guardrail: mount contract documents supersede floors and stale cache eviction.
- mechanism: stateful_multi_step_dependencies
  placement: relay holdback and queue flush ordering
  why_model_misses_it: agents fix manifest drift while leaving flush events out of ascending `(mode_rank, wave_seq, gen_b)` order or with swapped bind-rank values.
  fairness_guardrail: mount contract documents flush triple ordering and rank table consistency.
- mechanism: buried_local_constraints
  placement: checkpoint warm replay and gate epoch alignment
  why_model_misses_it: models advance replay domain or gate epoch without purging incompatible cache rows, leaving warm reruns misaligned.
  fairness_guardrail: mount contract documents replay domain and gate epoch purge rules.
- mechanism: cross_file_cross_format_invariants
  placement: split barrier commits versus path operation generations
  why_model_misses_it: agents observe `split_commit` journal rows but record `committed_gen` below `barrier_gen` instead of the era generation from the path operation tag.
  fairness_guardrail: mount contract states `committed_gen >= barrier_gen` and era-tag parsing semantics.
- mechanism: rollback_recovery_requirements
  placement: writable-pool checkpoint idempotency and manifest digest stability
  why_model_misses_it: models align one output surface while checkpoint `run_seq`, `manifest_sha256`, and anchor bytes diverge across delete-and-rerun recovery.
  fairness_guardrail: instruction and mount contract require idempotent reruns and preservation rules.

### calibration_plan

- oracle_runs: 3/3 stress plus 10/10 repeat for flake detection.
- no_op_runs: 3/3 mean 0.0 baseline.
- pass_rate_target: worst-model pass rate ≤ 20% with legitimate multi-subsystem Rust debugging failures.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt derived from Public contract above
- path: output_contract.toml
  role: local output declaration for identity_manifest, event_journal, consumer_trace
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed pytest only
- path: tests/test_outputs.py
  role: domain verifier
- path: solution/solve.sh
  role: oracle applying patch bundle and rebuilding driver
- path: environment/Dockerfile
  role: build definition; pre-install rust toolchain, pytest, tmux, asciinema
- path: construction_manifest.json
  role: local authoring artifact mirroring symbol table

### task_files

- path: environment/src/gate/cache.rs
  role: oracle frontier A — orphan generation floors and observer cache reuse
- path: environment/src/relay/queue.rs
  role: oracle frontier B — relay holdback and flush ordering
- path: environment/src/split/barrier.rs
  role: oracle frontier C — split barrier commits versus path operation generations
- path: environment/src/pipeline/flush_bridge.rs
  role: oracle frontier D — checkpoint warm replay and gate epoch alignment
- path: environment/tools/stamp_digest.py
  role: co-resident digest helper for stamp cross-checks (non-fix)
- path: environment/docs/mount_contract.md
  role: mount contract invariants and schema references
- path: environment/scripts/build_driver.sh
  role: release build entrypoint
- path: environment/scripts/run_driver.sh
  role: driver wrapper entrypoint

### fix_frontier

- count: 4
- distribution: gate/, relay/, split/, pipeline/ module roots
- naming_policy: Opaque Rust module paths only; no instruction nouns on fix paths
- forbidden_stems: [bind, propagation, orphan, inode, manifest, journal, trace, drift]
- helpers_policy: Decoys and co-resident helpers including stamp_digest.py perform adjacent work; frontier stays at four Rust modules
- symbol_thin_preferred: true

### category_profile

- challenge_family: bind_mount_state_reconciliation
- profile_name: debugging
- allowed_instruction_disclosures: mount_contract.md schemas, build_driver/run_driver commands, pytest verifier pipeline, preservation rules for fixtures and writable pool
- forbidden_instruction_leaks: exact patch hunks, oracle symbol names, per-row golden stamps
- category_specific_hardness_bar: Cache invalidation, journal ordering, replay domain alignment, and split barrier invariants must coordinate across manifest/journal/trace surfaces
- category_specific_verifier_risks: False greens from one aligned surface while checkpoint or flush ordering still diverges
- coverage_role: Bind propagation orphan inode reconciliation under debugging category

### reference_pattern

- reference_task_id:
- justification_if_none: Promoted reference async-pipeline-premature-completion targets state_recovery_crash_consistency only. No promoted reference matches bind mount propagation orphan inode combination.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: first-look dry run on instruction plus environment listing only
- shortcut_audit: block hand-written JSON under /app/output and fixture tampering
- ablation_plan: revert cache, relay, split, and pipeline modules separately; expect monotonic verifier drop
- pass_rate_target: hard_max_pct=20

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt=1 only when all pytest checks pass

### actionability_plan

- verifier_command_visible: build_driver.sh, run_driver.sh, and pytest via /tests/test.sh documented in instruction.md
- source_fix_intent_visible: yes — fix Rust sources under /app/environment; static output writes insufficient
- generated_output_rule_visible: identity_manifest, event_journal, and consumer_trace under /app/output must be pipeline-regenerated
- exact_formula_home: environment/docs/mount_contract.md
- schema_home: environment/schemas/p9_row.schema.json plus mount_contract.md
