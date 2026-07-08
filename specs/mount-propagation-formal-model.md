### Decision
GO — Attempt 1. Four-root fix frontier with fan/axis coupling, cross-format witness digests, opaque test naming, and RC2-neutral path tokens after satisfiability gate fix.

### Metadata
- version: 2
- Task name: mount-propagation-formal-model
- Title: Mount Propagation Proof
- Category: system-administration
- Task shape: formal_reasoning
- Languages: ["C", "Python"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["mount", "propagation", "formal-verification", "namespace", "concurrency"]
- Milestones: 0

## Authoring Brief

### Public contract

Fix the bundled mount propagation model under `/app/environment` so it satisfies the formal **invariants** exercised by the public checker:

```bash
/app/environment/tools/mp_verify --matrix all --profiles strict,relaxed --witness-out /app/output/witness.json
```

Rebuild the simulator and tools before running the checker. Success requires:

1. Every bundled **scenario** **sequence** maintains the documented **propagation** **invariants** for shared/private/slave flag relationships under the small-state model checker.
2. **Bind** mount event delivery matches canonical binary payload bytes; witness `trace_digest` must agree with the recomputation rule in `environment/docs/verify_contract.md`.
3. **Pivot** operations reset only the relationships documented in the contract—not all edges survive **pivot** unchanged.
4. Terminal `witness.json` from the full `--matrix all` run is graded; partial stage reports may look green while cross-scenario obligations still fail.

**Partial observability:** Textual log excerpts under `/app/output/logs` are sampled; not every **propagation** violation appears there. Use binary payload fixtures under `/app/environment/fixtures/sample_bytes` and checker diagnostics.

**False-green trap:** Stage reports under `/app/output/stage` may show locally acyclic graphs while terminal witness rows still fail. The verifier grades only the terminal `witness.json` from the full command above.

**Migration / recovery:** A destructive **migration** step ships at `environment/migrations/v2_store.sh`. Repeat it only via the idempotent **recovery** command documented in `verify_contract.md` before re-running **verification**.

**CLI semantics:** Use the exact checker flags above; wrapper scripts under `environment/scripts/` may differ from generic GNU behavior.

Domain status tokens (`MS_SHARED`, `MS_PRIVATE`, `MS_SLAVE`) appear in public fixtures and `environment/docs/flag_glossary.md`.

Static witness writes, checker-only edits, transition-table transcription without runtime fixes, or test modifications are insufficient.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public task prompt derived from Public contract above
- path: output_contract.toml
  role: local output declaration for witness.json
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed pytest only (no runtime apt/pip/curl)
- path: tests/test_outputs.py
  role: domain verifier (10 tests)
- path: solution/solve.sh
  role: oracle coordinating four fix-path symbols
- path: environment/Dockerfile
  role: build definition; pre-install cmake, gcc, pytest, pinned deps
- path: construction_manifest.json
  role: local authoring artifact mirroring symbol table below

### task_files

- path: environment/core/mp/transition.c
  role: propagation flag transition engine (fix frontier A)
- path: environment/core/mp/transition.h
  role: transition engine headers
- path: environment/core/mp/legacy_transition.c
  role: decoy deprecated transition implementation
- path: environment/core/mp/tree.c
  role: simulated mount tree mutations
- path: environment/core/mp/bundle_runner.c
  role: scripted sequence replay driver
- path: environment/fan/lane/delivery.c
  role: fan-in event delivery lane (fix frontier B)
- path: environment/fan/lane/delivery.h
  role: delivery lane headers
- path: environment/fan/lane/stub_delivery.c
  role: decoy no-op delivery stubs
- path: environment/coord/axis/reset.c
  role: axis swap relationship reset (fix frontier C)
- path: environment/coord/axis/reset.h
  role: axis reset headers
- path: environment/coord/axis/fan_matrix.c
  role: axis/fan interaction helper
- path: environment/tools/mp_verify/main.c
  role: checker CLI entrypoint
- path: environment/tools/mp_verify/engine.c
  role: matrix runner and invariant validation
- path: environment/tools/mp_verify/journal.c
  role: terminal journal packer (fix frontier D)
- path: environment/tools/mp_verify/journal.h
  role: journal blob headers
- path: environment/tools/evt_extract/collector.c
  role: binary payload collector/decoding
- path: environment/tools/evt_extract/collector.h
  role: payload collector headers
- path: environment/profiles/strict.toml
  role: strict propagation profile constants (CLI name strict)
- path: environment/profiles/relaxed.toml
  role: relaxed propagation profile constants (CLI name relaxed)
- path: environment/bundles/fan_in.json
  role: fan-in duplicate delivery bundle
- path: environment/bundles/axis_fan.json
  role: axis swap plus fan retention bundle
- path: environment/bundles/flag_chain.json
  role: private/shared/slave composition bundle
- path: environment/bundles/replay_matrix.json
  role: full matrix bundle index
- path: environment/docs/api.md
  role: public simulator API behavioral contract
- path: environment/docs/verify_contract.md
  role: witness schema, digest rule, recovery command
- path: environment/docs/flag_glossary.md
  role: MS_* status token glossary with fixture examples
- path: environment/migrations/v2_store.sh
  role: destructive migration with documented idempotent recovery
- path: environment/scripts/build_all.sh
  role: build orchestration wrapper with task-specific semantics
- path: environment/fixtures/sample_bytes/
  role: binary payload exemplars for observability drills
- path: environment/CMakeLists.txt
  role: top-level build definition

### fix_frontier

- count: 4
- distribution: core/mp, fan/lane, coord/axis, tools/mp_verify module roots
- naming_policy: Opaque symbols from construction manifest symbol_table only
- forbidden_stems: [propagation, invariant, sequence, scenario, shared, private, slave, bind, pivot, witness, digest, migration, recovery, verification, mount]
- helpers_policy: Decoys may rhyme structurally; oracle must not touch decoy bodies
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [witness digests, checker exit codes, payload-derived counts, schema field equality, cross-run invariants]
- forbidden_assertion_styles: [boolean answer keys, scenario->field->expected tables, fields ending in _ok/_valid/_passes]

### task_shape

- type: formal_reasoning
- instruction_framing: constraint-complete
- hardness_source: formal correctness
- collapse_risk: transcribing provided algorithm without proof obligations

### category_profile

- challenge_family: mount propagation semantics
- profile_name: concurrency_ordering
- allowed_instruction_disclosures: Concurrent mount sequences, public ordering invariants, mp_verify command, scenario/profile matrix, witness schema, sampled logs, recovery command, MS_* glossary
- forbidden_instruction_leaks: Race window location, transition table recipe, bind dedup key, pivot edge retention set, oracle transcript, fix-path symbol names
- category_specific_hardness_bar: Transition engine, fan delivery, axis reset, payload collector, and checker must coordinate across two profiles and six bundles
- category_specific_verifier_risks: False greens from acyclic-only checks, single-payload assertions, golden witness fixtures, global serialization shortcuts
- coverage_role: Strengthens concurrency_ordering via mount propagation formal proof with cross-artifact witnesses

### difficulty_mechanism_plan

- mechanisms: [rollback_recovery_requirements, partial_observability_experiment_design, environment_specific_cli_semantics, rare_local_vocabulary, false_green_intermediate_states, cross_file_cross_format_invariants]
- adversarial_layers_count: 6
- fairness_guardrails: Every layer is discoverable from local docs, payload fixtures, and the public checker command
- mechanism: rollback_recovery_requirements
  placement: environment/migrations/v2_store.sh payload store
  why_model_misses_it: Agents rerun destructive migration and corrupt stored payloads needed for replay bundles
  fairness_guardrail: Idempotent recovery command documented in verify_contract.md
- mechanism: partial_observability_experiment_design
  placement: sampled textual logs vs full binary payloads under fixtures/sample_bytes
  why_model_misses_it: Agents infer propagation violations from incomplete log excerpts rather than required bundle experiments
  fairness_guardrail: Instruction lists required bundle/profile pairs and binary payload directory
- mechanism: environment_specific_cli_semantics
  placement: environment/scripts/build_all.sh and mp_verify wrapper flags
  why_model_misses_it: Agents assume generic GNU make/cmake behavior and skip profile matrix flags
  fairness_guardrail: Instruction names exact mp_verify command and rebuild prerequisite
- mechanism: rare_local_vocabulary
  placement: MS_SHARED/MS_PRIVATE/MS_SLAVE status tokens in fixtures and checker output
  why_model_misses_it: Agents misread domain-specific flag tokens as generic mount success markers
  fairness_guardrail: flag_glossary.md defines tokens with public fixture examples
- mechanism: false_green_intermediate_states
  placement: /app/output/stage partial mp_verify reports
  why_model_misses_it: Local acyclic propagation graphs pass early while terminal witness rows still fail cross-bundle obligations
  fairness_guardrail: Instruction states terminal witness.json from full --matrix all run is graded
- mechanism: cross_file_cross_format_invariants
  placement: witness JSON vs canonical binary payload bytes
  why_model_misses_it: Agents patch JSON summaries without rebuilding canonical payloads checked by digest tests
  fairness_guardrail: verify_contract.md documents sha256 trace_digest over canonical binary bytes

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: Namespace engineer reproduces failing mp_verify locally using seeded bundles only
- shortcut_audit: Block hardcoded witness JSON, checker-only patch, transition-table transcription without fan/axis fixes, test edits
- ablation_plan: Remove partial-log layer, then cross-format digest layer, then profile matrix; expect monotonic difficulty drop
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=Part E Hard threshold on worst-model accuracy; verifier-offline via Dockerfile-baked pytest; post-upload difficulty classification after platform agent runs

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward.txt=1 only when all weighted metrics pass

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: Single-container local verifier with seeded replay scheduler only

### satisfiability_risk

- rc2_planned_name_risk: low — opaque fix-path symbols and neutral path tokens precommitted in symbol_table
- gx9_contract_risk: low — contract uses digests and structured rows, not boolean verdict tables
- cr1_symbol_frontier_risk: low — frontier spans four module roots with decoys
- hidden_contract_risk: medium — binary payload digest rules and axis edge retention live in cross-artifact behavior and verify_contract.md

### actionability_plan

- verifier_command_visible: mp_verify --matrix all --profiles strict,relaxed documented in instruction.md
- source_fix_intent_visible: yes — fix sources under /app/environment so rebuilt checker passes; no patch recipe
- generated_output_rule_visible: witness.json path and schema public; terminal matrix output is graded
- exact_formula_home: environment/docs/verify_contract.md for trace_digest sha256 and witness field rules
- schema_home: instruction.md plus environment/docs/verify_contract.md and flag_glossary.md

### waiver_plan

- waivers_expected: no
- waiver_rationale: Hardness from coupled mount propagation behavior, not harness brittleness

### reference_pattern

- reference_task_id:
- justification_if_none: No promoted reference task covers mount propagation formal proof with cross-profile witnesses and axis/fan coupling

### realism_source

- source_type: real_system
- evidence_basis: open-source issue
- upstream_or_synthetic_rationale: Production system-administration pattern for mount propagation semantics: shared/private/slave composition, bind duplicate events, pivot partial reset
- minimization_preserves: Causal coupling in mount propagation formal proof across transition, delivery, reset, and witness surfaces
- synthetic_exception_review: not required

### Failure topology

The bundled propagation simulator fails formal verification for different root causes depending on bundle and profile. Flag transition updates can satisfy local acyclic checks while fan-in duplicate delivery still emits extra events that invalidate witness rows. Axis swap operations reset some propagation edges but retain fan-slave relationships on pre-axis subtrees; treating axis swap as a full tree wipe passes smoke paths and fails replay bundles. Journal packing ties JSON summaries to canonical binary payload digests, so checker-only or static JSON edits fail cross-format tests. Sampled textual logs omit violations that appear only in binary payloads under the bundled fixtures. No single subsystem edit satisfies all six bundles under both strict and relaxed profiles.

### Environment shape

- `environment/core/mp/` — simulated mount tree, transition engine, bundle replay driver
- `environment/fan/lane/` — fan-in event delivery lane and decoy stubs
- `environment/coord/axis/` — axis swap relationship reset and fan interaction matrix
- `environment/tools/mp_verify/` — formal checker CLI, matrix engine, journal packer
- `environment/tools/evt_extract/` — binary payload collection/decoding
- `environment/profiles/` — strict and relaxed propagation parameter files
- `environment/bundles/` — seeded scripted sequence JSON consumed by mp_verify
- `environment/docs/` — API, verification contract, and flag glossary (solver-visible)
- `environment/migrations/` — destructive payload migration plus documented recovery
- `environment/scripts/` — build wrapper with task-specific CLI semantics
- `environment/fixtures/` — binary payload exemplars and replay anchor material

### Required artifacts

Step 2b creates: `task.toml` (`allow_internet = false`), `instruction.md`, `output_contract.toml`, `tests/test.sh`, `tests/test_outputs.py` (10 tests), `solution/solve.sh`, `environment/Dockerfile` (C toolchain + pytest baked in), all task_files above, and `construction_manifest.json` matching the symbol table. Environment must contain 20+ non-Docker files.

### Test plan

1. `test_m01` — terminal matrix witness rows, digests, and invariant counts for strict profile
2. `test_m02` — same for relaxed profile with cross-profile divergence checks
3. `test_m03` — flag_chain bundle flag composition matches witness rows
4. `test_m04` — fan_in duplicate event counts match canonical payload bytes
5. `test_m05` — fan delivery replay is idempotent across two matrix runs
6. `test_m06` — axis_fan bundle retains documented fan-slave edges after axis swap
7. `test_m07` — axis reset does not wipe unrelated shared subtrees
8. `test_m08` — v2_store recovery restores fixtures across repeated destructive steps
9. `test_m09` — stage JSON omits fields present in terminal witness journals
10. `test_m10` — metamorphic tags differ when trace digests diverge

### Drafting guardrails

Do not place instruction nouns on fix-path symbols or directories. Do not embed oracle hints in environment comments. Keep witness contract in verify_contract.md, not only in tests. Ensure checker diagnostics never name apply_flag_n, fold_event_r, reset_edge_q, or pack_journal_u. Avoid boolean verdict fields in witness.json. Do not publish full transition composition tables or fan dedup keys in instruction.md.

### Triviality Ledger

- Naive transition-table transcription passes single-bundle smoke but fails `test_m04` because fan-in duplicate delivery still emits extra canonical payload events.
- Checker-only patches can make stage reports look acyclic while `test_m09` fails because terminal witness journals require fields omitted from stage JSON.
- Axis-as-full-wipe passes `test_m03` locally but `test_m06` fails because fan-slave edges on pre-axis subtrees must be retained per contract.
- Hand-written witness.json fails digest cross-check even when sampled logs look green.

### Per-gate Pitfall Inventory

- RC1: Oracle must perform substantive cross-file edits, not byte-identical rewrites (GX4).
- RC2: Fix-path symbols stay opaque; instruction nouns banned via code_forbidden_tokens; path components use fan/axis/bundles/evt_extract/journal not bind/pivot/scenario/witness/trace.
- RC6: Instruction stays constraint-complete, not spec-complete with full transition matrix recipe.
- RC7/GX3: Oracle solve.sh must exceed 80 LOC substantive coordination logic or document WARN justification.
- CR1: Four fix roots required; decoys stay off oracle path.
- GX9: Do not enumerate witness field values per bundle in instruction.md.
- GX10: Avoid naming both pass/fail polarities for one bundle field in one sentence.
- GX6: Limit causal connective chains that reveal patch order across subsystems.

### Initial Draft Commitments

- task.toml, instruction.md, output_contract.toml, construction_manifest.json
- tests/test.sh, tests/test_outputs.py (opaque test_m01–test_m10)
- solution/solve.sh, solution/apply_fixes.sh
- environment/Dockerfile, environment/CMakeLists.txt
- environment/core/mp/transition.c, environment/core/mp/transition.h, environment/core/mp/legacy_transition.c, environment/core/mp/tree.c, environment/core/mp/bundle_runner.c
- environment/fan/lane/delivery.c, environment/fan/lane/delivery.h, environment/fan/lane/stub_delivery.c
- environment/coord/axis/reset.c, environment/coord/axis/reset.h, environment/coord/axis/fan_matrix.c
- environment/tools/mp_verify/main.c, environment/tools/mp_verify/engine.c, environment/tools/mp_verify/journal.c, environment/tools/mp_verify/journal.h
- environment/tools/evt_extract/collector.c, environment/tools/evt_extract/collector.h
- environment/profiles/strict.toml, environment/profiles/relaxed.toml
- environment/bundles/fan_in.json, environment/bundles/axis_fan.json, environment/bundles/flag_chain.json, environment/bundles/replay_matrix.json
- environment/docs/api.md, environment/docs/verify_contract.md, environment/docs/flag_glossary.md
- environment/migrations/v2_store.sh, environment/scripts/build_all.sh
- environment/fixtures/sample_bytes/

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/core/mp/transition.c
  symbol: apply_flag_n
  kind: function
  signature: int apply_flag_n(struct mp_ctx *ctx, uint32_t mnt_id, enum flag_action act, uint8_t target_flag)
  purpose: Applies propagation flag transitions for a mount node in the simulated tree.
- path: environment/fan/lane/delivery.c
  symbol: fold_event_r
  kind: function
  signature: int fold_event_r(struct mp_ctx *ctx, const struct fan_event *ev, uint32_t parent_id, uint16_t submount_gen)
  purpose: Merges fan-in propagation events into the active delivery lane.
- path: environment/coord/axis/reset.c
  symbol: reset_edge_q
  kind: function
  signature: void reset_edge_q(struct mp_ctx *ctx, uint32_t root_id, enum axis_scope scope)
  purpose: Rewrites propagation edges after an axis swap for the given scope.
- path: environment/tools/mp_verify/journal.c
  symbol: pack_journal_u
  kind: function
  signature: int pack_journal_u(const struct run_matrix *mx, struct journal_blob *out)
  purpose: Serializes terminal witness rows and canonical payload digests for grading.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: environment/core/mp/transition.c
    controls_tests: [test_m01, test_m02, test_m03]
  - id: B
    path: environment/fan/lane/delivery.c
    controls_tests: [test_m04, test_m05]
  - id: C
    path: environment/coord/axis/reset.c
    controls_tests: [test_m06, test_m07, test_m08]
  - id: D
    path: environment/tools/mp_verify/journal.c
    controls_tests: [test_m09, test_m10]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: environment/core/mp/legacy_transition.c
  kind: module
  rhymes_with: apply_flag_n
  non_fix_purpose: Deprecated transition path used only by offline benchmarks.
- path: environment/fan/lane/stub_delivery.c
  kind: helper
  rhymes_with: fold_event_r
  non_fix_purpose: No-op delivery stubs for simulator builds.
- path: environment/tools/evt_extract/collector.c
  kind: helper
  rhymes_with: pack_journal_u
  non_fix_purpose: Collects payload metadata without mutating propagation state.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [propagation, invariant, sequence, scenario, shared, private, slave, bind, pivot, witness, digest, migration, recovery, verification, mount]
```
