### Decision
GO — Attempt 2. Attempt 1 failed only on non-canonical evidence IDs; Attempt 2 fixed those schema IDs with no topology regression and reached 0F/0W.

### Metadata
- Task name: snapshot-compaction-race-cpp
- Title: Snapshot Compaction Race
- Category: debugging
- Languages: ["cpp"]
- Difficulty: hard
- Codebase size: small
- Subcategories: ["state-recovery", "consistency"]
- Tags: ["compaction", "restart", "recovery", "race", "consistency"]
- Milestones: 0

### Discovery budget
- Discovery: Visible-ready signal can be emitted before canonical settle truly completes.
  Planned location: environment/core/phase_gate.cpp::phase_latch_q
  Why instruction must not reveal it: Cause naming would collapse diagnosis to one local scheduling tweak.
- Discovery: Health probe can pass on shallow checks while canonical consistency still fails.
  Planned location: environment/checks/surface_probe.cpp::probe_gate_v
  Why instruction must not reveal it: Direct disclosure enables checklist patching without codebase synthesis.
- Discovery: Restart reload can preserve stale alias authority ordering unless remap is recomputed.
  Planned location: environment/store/rebind_table.cpp::ring_bridge_m
  Why instruction must not reveal it: It would disclose fix path and reduce multi-surface reasoning.

### Anti-trivialization verdict
- disclosure_collapse: PASS — Hardness survives only with symptoms-only contract.
- hidden_instance: PASS — Difficulty is coupling, not single-file hunt.
- single_artifact_repair: PASS — Needs runtime + store + probe coordination.
- generalization: PASS — Multiple restart trajectories and collision cases covered.
- prompt_honesty: PASS — Prompt can be honest without naming causes.
- cheating_vs_difficulty: PASS — No anti-cheat-only hardness.
- mechanical_fix_filter: PASS — Core problem is behavior, not harness setup.
- localized_fix: PASS — Flipping-point contract blocks one-locus repair.
- oracle_locality: PASS — Planned oracle frontier spans distinct roots.
- small_declarative_cluster: PASS — Not reducible to tiny table/config edits.
- grep_collapse: PASS — Opaque naming and token ban reduce noun-grep shortcuts.
- pre_factored_helper: PASS — No prompt-mirroring helper names.
- recipe_discount: PASS — Not a standard recipe implementation.
- security_aura_discount: PASS — No reliance on security framing for hardness.
- orthogonal_checklist: PASS — Requirements are coupled and tradeoff-bearing.
- harness_discount: PASS — Hardness independent of infra complexity.
- one_pass_solvability: PASS — One-pass obvious-file edit is unlikely to pass all tests.
- hard_only_gate: PASS — Clearly hard, not medium.
- discovery_budget_test: PASS — 3 non-trivial discoveries planned and hidden.
- instruction_specificity_test: PASS — Symptoms-only instruction target.
- topology_distribution_test: PASS — 3 distinct ≥3-location fix topologies articulated.

### Topology enumeration (3 candidate fix topologies)
- Topology A (gate/remap/probe): `environment/core/phase_gate.cpp::phase_latch_q`, `environment/store/rebind_table.cpp::ring_bridge_m`, `environment/checks/surface_probe.cpp::probe_gate_v`. No single location suffices because visibility timing, persisted remap, and checker depth must align.
- Topology B (trace/merge/scan): `environment/core/epoch_trace.cpp::trace_mux_c`, `environment/store/ledger_mux.cpp::apply_merge_turn`, `environment/checks/history_scan.cpp::scan_anchor_chain`. No single location suffices because anchor correctness depends on producer, persistence, and validator agreement.
- Topology C (fold/reindex/order-check): `environment/core/identity_fold.cpp::fold_pair_stream`, `environment/store/rebind_table.cpp::reindex_alias_ring`, `environment/checks/order_probe.cpp::assert_pair_monotone`. No single location suffices because duplicate-identity arbitration is jointly defined by fold order, storage reindexing, and assertion semantics.

### Rubric axes
- verifiable: PASS — deterministic seeded test contract.
- well_specified: PASS — concise public behavior contract without cause leakage.
- solvable: PASS — expert-feasible in hours with focused debugging.
- difficult: PASS — cross-root coupling and temporal reasoning required.
- interesting: PASS — production-relevant reliability failure mode.
- outcome_verified: PASS — graded on behavior, not implementation process.

### Hardness axes
- discover: PASS — hidden race and stale-remap coupling must be uncovered in code/runtime.
- synthesize: PASS — complete fix requires combining findings from multiple subsystems.
- diagnose: PASS — symptom-first prompt with no cause disclosure.
- navigate_coupling: PASS — local edits can break distant invariants.
- reason_beyond_training: PASS — bespoke state semantics exceed pattern-match recipes.

### Instruction completeness test
Can the agent solve this by reading only instruction.md? No. Instruction will not name defect sites or causal mechanism, so deep code engagement is required.

## Reviewer Appendix

### Implementation plan
Construct a C++ environment where readiness visibility, replay progression, and reload authority rebind logic can drift after restart boundaries even when shallow health appears green. The realization should force diagnosis of temporal sequencing and state authority reconstruction rather than surface-value transcription.

Seed defects across three roots and ensure test coverage forces coordination: readiness-order checks, canonical remap checks, and long-horizon identity/replay checks. Include decoy modules that rhyme structurally with fix modules to discourage path-by-name shortcutting.

### Proposed file inventory
Plan a 20+ file `environment/` with distinct `core`, `store`, and `checks` trees plus headers, configs, and seeded data fixtures. Keep build/test scaffolding straightforward and deterministic.

### Oracle notes
Oracle should edit at least three distinct fix-path locations and include substantive logic (not no-op rewrites). It should establish ordering guarantees, canonical remap correction, and probe-depth alignment sufficient to satisfy all test subsets under flipping-point constraints.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
Delay one visible-ready emission path in a gate function.

Likely editable frontier:
- environment/core/phase_gate.cpp
- environment/store/rebind_table.cpp
- environment/checks/surface_probe.cpp

Requirement-to-file map:
- readiness aligns with true settle -> environment/core/phase_gate.cpp
- restart remap remains canonical -> environment/store/rebind_table.cpp
- shallow/deep health agreement -> environment/checks/surface_probe.cpp

Oracle estimated complexity: 110 lines of non-boilerplate logic

Red flags:
- Attempt 1 had schema-ID mismatch in evidence arrays; fixed in Attempt 2.

Residual hardness:
Even with full file visibility, the solver must infer cross-generation causality and repair coupled invariants across asynchronous and persisted boundaries.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
restart, resume, system, recovery, generations, state, operators, replay, compaction, completion, reconciliation, mappings, identities

**Renames during drafting:**
- `emit_replay_ready` -> `phase_latch_q`: removed forbidden token `replay`
- `test_generation_resume_divergence` -> `test_lane_window_consistency`: removed forbidden tokens `generations`, `resume`
- `test_replay_compaction_health` -> `test_commit_latch_visibility`: removed forbidden tokens `replay`, `compaction`

**Test names audited:**
- test_lane_window_consistency
- test_commit_latch_visibility
- test_map_epoch_roundtrip
- test_alias_sort_stability
- test_horizon_anchor_trace

**Concentration math:**
- Total tests across `flipping_point_contract`: 5
- Per location:
  - A (`environment/core/phase_gate.cpp`): 2/5 = 0.4
  - B (`environment/store/rebind_table.cpp`): 1/5 = 0.2
  - C (`environment/checks/surface_probe.cpp`): 2/5 = 0.4
- Cap: 0.5. Max ratio observed: 0.4. Status: PASS

### Per-test feasibility pre-check
- Test: test_lane_window_consistency
- Checks: visible-ready cannot precede canonical lane settle.
- Valid approaches: 2+
- Chain-dependent: yes (gate + probe)
- Feasibility risk: MEDIUM

- Test: test_commit_latch_visibility
- Checks: commit visibility appears only after settle-latch threshold.
- Valid approaches: 2+
- Chain-dependent: yes (gate + trace)
- Feasibility risk: MEDIUM

- Test: test_map_epoch_roundtrip
- Checks: restarted map reconstruction remains deterministic.
- Valid approaches: 2+
- Chain-dependent: yes (store + core)
- Feasibility risk: MEDIUM

- Test: test_alias_sort_stability
- Checks: duplicate identity ordering remains stable.
- Valid approaches: 2+
- Chain-dependent: yes (fold + store + checks)
- Feasibility risk: MEDIUM

- Test: test_horizon_anchor_trace
- Checks: long-horizon anchor chain remains consistent after restart boundaries.
- Valid approaches: 2+
- Chain-dependent: yes (trace + store + scan)
- Feasibility risk: MEDIUM

- Test: test_probe_depth_agreement
- Checks: shallow pass cannot mask canonical inconsistency.
- Valid approaches: 2+
- Chain-dependent: yes (probe + data path)
- Feasibility risk: MEDIUM
