### Decision

GO — repair_existing_system task for cgroup-style metric persistence desync. Hardness from multi-component replay semantics, journal reconstruction, cross-tag state isolation, and corruption recovery across persist/runtime/rollup/janitor packages.

### Metadata

- Task name: cgroup-pressure-metric-desync
- Category: debugging
- Task shape: repair_existing_system
- Languages: ["go", "bash"]
- Difficulty: hard

### difficulty_mechanism_plan

- mechanisms: rollback_recovery_requirements, cross_file_cross_format_invariants, stateful_multi_step_dependencies, deceptive_but_valid_local_evidence, journal_reconstruction, replay_system
- adversarial_layers_count: 6
- mechanism: journal_reconstruction
  placement: corrupt run_journal.json mid-chain with cold/warm recovery expectations
  why_model_misses_it: agents delete corrupt journals instead of rewriting valid empty segments before export continues
  fairness_guardrail: check_contract.md documents cold repair shape without naming fix functions
- mechanism: replay_system
  placement: inverted generation window and foreign-tag ghost replay into blend_ratio
  why_model_misses_it: models patch obvious tag equality checks but miss generation-scoped replay semantics
  fairness_guardrail: epoch generation bumps are observable in epoch.json during tests
- mechanism: cross_file_cross_format_invariants
  placement: retention, deferred compact, overlay merge, and rollup ordering interact on shared mem_a
  why_model_misses_it: fixing one janitor helper leaves warm-path compaction before retention reintroducing foreign ghost
  fairness_guardrail: mixed-tag chains in verifier exercise ordering invariants
- mechanism: stateful_multi_step_dependencies
  placement: checkpoint seq, validated bit, and warm-on-empty-store through reconcile helpers
  why_model_misses_it: driver-only warm checkpoint requirement passes some runs but fails fresh-store warm and seq monotonicity
  fairness_guardrail: cold leaves validated false; warm sets validated true with same blend
- mechanism: deceptive_but_valid_local_evidence
  placement: overlay and journal rows look structurally valid while attributing foreign-tag mass
  why_model_misses_it: local per-tag exports appear healthy until unrelated tags pollute the shared store
  fairness_guardrail: band assertions derive from visible calib constants only
- mechanism: rollback_recovery_requirements
  placement: corrupt checkpoint, epoch, and overlay sidecars during cold preparation
  why_model_misses_it: agents treat parse errors as fatal instead of recovering into the next generation export
  fairness_guardrail: corruption tests write invalid bytes then expect successful cold export

### calibration_plan

- pass_rate_target: hard_max_pct=20
- ablation_plan: partial fixes on journal, epoch, reconcile, compact, and rollup should fail disjoint verifier subsets
