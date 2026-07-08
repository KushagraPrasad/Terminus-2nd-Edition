### Decision
GO — Attempt 1. Committed bash-only three-module offline rescue packaging frontier with pivot/bind topology coupling, ld.so cache invalidation cross-format invariants, and four-profile verifier matrix.

### Metadata
- version: 2
- Task name: offline-rescue-chroot-contract
- Title: Offline Rescue Chroot Contract
- Category: software-engineering
- Task shape: constrained_build
- Languages: ["bash"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["system-administration", "offline-build", "chroot", "rescue", "toolchain", "packaging"]
- Milestones: 0

## Authoring Brief

### Public contract

Build a **bash-only** offline rescue packaging toolchain under `/app/environment/w2` that produces a profile-aware pack rebinding the active root under strict capability and size limits, **without modifying** the read-only host fixture at `/app/environment/h0/fixture`.

Public checker:

```bash
/app/environment/v5/rc_verify --all-profiles --pack-out /app/output/pack_out.json --report-out /app/output/run_report.json
```

Run `/app/environment/w2/run_entry.sh` (or equivalent wiring you create) before `rc_verify`. Success requires:

1. **Four-profile matrix** — `nvme`, `luks`, `zfs`, and `legacy` profiles from `environment/p1/` each pass the checker with reference rows matching `environment/w6/*_row.json`.
2. **Rebinding outcomes** — active-root rebinding follows externally tested outcomes in `environment/c4/k4_rules.md` and size limits in `environment/c4/k4_limits.md` (pivot vs bind rescue paths are not interchangeable across profiles).
3. **Linker cache invalidation** — generated cache bytes target the rescue root prefix declared in pack metadata, not the host fixture prefix; local cache probes alone are insufficient.
4. **Pack digest binding** — `pack_out.json` `pack_digest` matches `run_report.json` per the public formula in `environment/c4/k4_pack.md` (JSON metadata cross-checks binary cache headers and bind manifest hashes).
5. **Size and capability hygiene** — emitted pack stays within published offline limits and does not require disallowed capabilities.

**Deceptive local evidence:** `rc_verify health` and `rc_verify status` subcommands may report success before the terminal `--all-profiles` matrix converges.

**False-green trap:** `/app/output/stage` and `environment/v5/stage_only.sh` may show passing rows while `pack_digest` cross-check fails.

**Recovery:** Repeat `environment/m7/mig7.sh` only via the idempotent recovery command in `k4_pack.md` before re-running verification.

Hardcoding deliverables, mutating `environment/h0/fixture`, host-prefix cache reuse, or test edits are insufficient.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false`
- path: instruction.md
  role: natural public design-brief prompt derived from Public contract above
- path: output_contract.toml
  role: local output declaration for pack_out.json and run_report.json
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed pytest only (no runtime apt/pip/curl)
- path: tests/test_outputs.py
  role: domain verifier (8 tests)
- path: solution/solve.sh
  role: bash oracle coordinating op_a, phase_b, reconcile_c
- path: environment/Dockerfile
  role: build definition; bake bash, fakeroot helpers, pytest offline
- path: construction_manifest.json
  role: local authoring artifact mirroring symbol table below

### task_files

- path: environment/h0/fixture/etc/os-release
  role: read-only host root identity fixture
- path: environment/h0/fixture/exec/sh
  role: minimal host shell stub
- path: environment/h0/fixture/lib/ld-linux-x86-64.so.2
  role: host dynamic linker stub for prefix contrast
- path: environment/p1/nvme.json
  role: nvme profile descriptor for rc_verify
- path: environment/p1/luks.json
  role: luks profile descriptor
- path: environment/p1/zfs.json
  role: zfs profile descriptor
- path: environment/p1/legacy.json
  role: legacy profile descriptor
- path: environment/t2/h0_link.bin
  role: host-prefix linker cache bytes
- path: environment/t2/r0_link.bin
  role: rescue-prefix reference cache bytes
- path: environment/d3/floor.json
  role: baseline devnode schema
- path: environment/d3/p1_overrides.json
  role: per-profile devnode cardinality and majors
- path: environment/c4/k4_rules.md
  role: public pivot vs bind rules and rebinding outcome matrix
- path: environment/c4/k4_limits.md
  role: size and capability limits for offline pack
- path: environment/c4/k4_pack.md
  role: pack_out.json / run_report.json schemas and pack_digest formula
- path: environment/c4/shortcut.sh
  role: decoy host-bind-only helper
- path: environment/v5/rc_verify
  role: checker CLI with health/status subcommands
- path: environment/v5/grid_engine.sh
  role: pack_digest and witness validation
- path: environment/v5/stage_only.sh
  role: decoy stage reporter without digest cross-check
- path: environment/v5/apply_ctl.sh
  role: offline replay driver applying pack to fixtures
- path: environment/w6/nvme_row.json
  role: nvme reference rows
- path: environment/w6/luks_row.json
  role: luks reference rows
- path: environment/w6/zfs_row.json
  role: zfs reference rows
- path: environment/w6/legacy_row.json
  role: legacy reference rows
- path: environment/m7/mig7.sh
  role: destructive migration with documented idempotent recovery
- path: environment/c4/k2/ctl_k.sh
  role: build-path module A (agent implements op_a)
- path: environment/w2/m2/m_phase.sh
  role: build-path module B (agent implements phase_b)
- path: environment/v5/p2/assemble_p.sh
  role: build-path module C (agent implements reconcile_c)
- path: environment/w2/run_entry.sh
  role: wires three modules into pipeline entrypoint

### fix_frontier

- count: 3
- distribution: environment/c4/k2, environment/w2/m2, and environment/v5/p2 across three bash module roots plus run_entry entry
- naming_policy: Opaque symbols from construction manifest symbol_table only
- forbidden_stems: [rescue, chroot, rebind, pivot, bind, ldso, cache, device, nodes, storage, backend, capability, offline, active, migration, recovery, rollback, health, status, intermediate, digest, verification, profiles, witness]
- helpers_policy: Decoys may rhyme structurally; oracle must not modify decoy bodies to pass
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 0
- preferred_assertion_styles: [pack_digest equality, checker exit codes, witness numeric fields, schema keys, cross-run invariants, binary header bytes]
- forbidden_assertion_styles: [boolean answer keys, scenario->field->expected tables, fields ending in _ok/_valid/_passes]

### task_shape

- type: constrained_build
- instruction_framing: design-brief
- hardness_source: design search
- collapse_risk: blank-canvas build with no binding cross-component constraints

### category_profile

- challenge_family: rescue environment packaging
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: Observable packaging requirements, public rc_verify command, four offline profiles, capability/size limits, output schemas, recovery command, witness outcomes
- forbidden_instruction_leaks: Per-backend pivot/bind choice table as recipe, exact ld.so prefix rewrite steps, per-backend devnode major/minor lists, oracle transcript
- category_specific_hardness_bar: Fixtures, generated ld.so cache bytes, rebinding graph, and cache invalidation coordinate across four offline profiles
- category_specific_verifier_risks: False greens from local health/status subcommands, golden pack fixtures, clean-host-only checks
- coverage_role: Strengthens build_dependency_toolchain via offline rescue chroot packaging with multi-backend matrix

### difficulty_mechanism_plan

- mechanisms: [deceptive_but_valid_local_evidence, false_green_intermediate_states, cross_file_cross_format_invariants, rollback_recovery_requirements, environment_specific_cli_semantics]
- adversarial_layers_count: 5
- fairness_guardrails: Every layer is discoverable from local docs, fixtures, and the public rc_verify command
- mechanism: deceptive_but_valid_local_evidence
  placement: environment/v5/rc_verify health and status subcommands
  why_model_misses_it: Models trust misleading local success from health probes that skip pack_digest and full profile matrix
  fairness_guardrail: Instruction requires terminal --all-profiles run; grid_engine cross-checks durable pack_out.json against run_report.json
- mechanism: false_green_intermediate_states
  placement: /app/output/stage summaries via environment/v5/stage_only.sh
  why_model_misses_it: Models declare done when intermediate report files show passing rows before terminal convergence
  fairness_guardrail: Verifier requires full profile matrix pack_digest match documented in k4_pack.md
- mechanism: cross_file_cross_format_invariants
  placement: pack_out.json metadata vs environment/t2 link byte headers in grid_engine
  why_model_misses_it: Models fix single JSON file without aligning binary ld.so cache bytes to rescue prefix; cache invalidation for non-host prefix is required
  fairness_guardrail: pack_digest formula and witness numeric fields are public in k4_pack.md
- mechanism: rollback_recovery_requirements
  placement: environment/m7/mig7.sh destructive migration of fixture store
  why_model_misses_it: Models repeat destructive migration and corrupt backend fixtures needed for luks/zfs witnesses; build failure recovery path must be followed
  fairness_guardrail: Idempotent recovery path documented publicly in k4_pack.md before re-verification
- mechanism: environment_specific_cli_semantics
  placement: environment/v5/rc_verify flags and environment/c4/k4_rules.md profile matrix
  why_model_misses_it: Models assume generic mount --bind semantics apply uniformly across all four profiles
  fairness_guardrail: Instruction names exact rc_verify command and references k4_rules.md for externally tested rebinding outcomes

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: Expert sysadmin reproduces four-profile pack locally using bash toolchain and rc_verify only offline
- shortcut_audit: Block hardcoded pack_out.json, host fixture mutation, stage-only shortcuts, health-subcommand-only success, test edits
- ablation_plan: Remove deceptive health layer, then pack_digest cross-format layer, then rollback recovery; expect monotonic difficulty drop
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
- sidecar_or_protocol_notes: Single-container local verifier only; offline fixtures pre-bundled

### satisfiability_risk

- rc2_planned_name_risk: low — opaque build-path symbols precommitted in symbol_table
- gx9_contract_risk: low — contract uses pack_digest rows and numeric witnesses, not boolean verdict tables
- cr1_symbol_frontier_risk: low — frontier spans three bash module roots with decoys
- hidden_contract_risk: medium — pack_digest binds JSON metadata to binary cache headers and bind manifest hashes in grid_engine behavior

### actionability_plan

- verifier_command_visible: rc_verify --all-profiles with pack-out and report-out paths in instruction.md
- source_fix_intent_visible: yes — build bash under environment/w2; do not mutate environment/h0/fixture
- generated_output_rule_visible: pack_out.json and run_report.json schemas and pack_digest rule public in k4_pack.md
- exact_formula_home: environment/c4/k4_pack.md for pack_digest and witness tolerance rules
- schema_home: environment/c4/k4_pack.md plus instruction.md output paths

### waiver_plan

- waivers_expected: no
- waiver_rationale: Hardness from coupled offline packaging behavior and cache invalidation, not harness brittleness

### reference_pattern

- reference_task_id:
- justification_if_none: No promoted reference tasks in docs/reference_tasks/index.json; offline rescue chroot packaging with pivot/bind and ld.so retargeting is a distinct build_dependency_toolchain pattern without a promoted clone source.

### realism_source

- source_type: real_system
- evidence_basis: open-source issue
- upstream_or_synthetic_rationale: Production system-administration pattern for initramfs/rescue image packaging — pivot_root vs bind rescue paths, ld.so cache targeting non-host root, storage-backend-specific minimal devnodes
- minimization_preserves: Causal coupling in offline rescue packaging across rebinding topology, linker cache invalidation, and backend device minimality
- synthetic_exception_review: not required

### Failure topology

The read-only host fixture defines the active-root baseline, but agents must emit an offline rescue pack that rebinds safely per profile without mutating host bytes. Pivot-style rebinding works for some storage backends while others require recursive bind rescue paths; choosing the wrong topology passes local health probes yet fails witness rows on replay. Linker cache generation must retarget the rescue root prefix — host-prefix caches validate locally via deceptive probes but break pack_digest once binary headers are cross-checked. Device node minimality varies by backend overrides, so a single generic devnode table cannot satisfy all four profiles. The checker ties JSON pack metadata to binary cache and bind manifest bytes through a public pack_digest rule, so hand-authored JSON or stage-only success paths still fail cross-format checks. Destructive migration can corrupt stored fixtures unless the documented idempotent recovery runs first. Multi-component interaction across rebinding, cache invalidation, and assembly modules is required; no single bash file satisfies the full matrix.

### Environment shape

- `environment/h0/` — read-only host root fixture tree
- `environment/p1/` — four profile descriptors consumed by rc_verify
- `environment/t2/` — host vs rescue linker cache template bytes
- `environment/d3/` — devnode schema and per-profile overrides
- `environment/c4/` — rebinding and limit contracts, k4_pack schemas, decoy shortcut helper; `k2/` agent module root
- `environment/v5/` — rc_verify CLI, grid_engine validation, apply_ctl replay, decoy stage reporter; `p2/` agent module root
- `environment/w6/` — per-profile reference JSON rows
- `environment/m7/` — destructive migration step plus recovery contract
- `environment/w2/` — agent-built bash modules and run_entry wiring

### Required artifacts

Step 2b creates: `task.toml` (`allow_internet = false`), `instruction.md`, `output_contract.toml`, `tests/test.sh`, `tests/test_outputs.py` (8 tests), `solution/solve.sh` (bash oracle with substantive multi-module coordination ≥80 LOC or documented GX3 justification), `environment/Dockerfile` (bash, fakeroot helpers, pytest baked in), all task_files above, and `construction_manifest.json` matching the symbol table. Environment must contain 20+ non-Docker files. Primary agent implementation language is **bash**.

### Test plan

1. `test_t01_terminal` — rc_verify exit 0 for all four profiles; chain-dependent on full pipeline
2. `test_t02_artifact_align` — pack_out pack_digest matches run_report per k4_pack.md
3. `test_t03_p9_deep` — zfs/legacy fail if rebinding uses pivot where bind rescue path is required
4. `test_t04_smoke_guard` — nvme remains passing after luks-oriented cache retarget fixes
5. `test_t05_visibility` — luks profile requires full devnode override table before first pack emission
6. `test_t06_w3_idem` — documented recovery after mig7.sh preserves fixture integrity
7. `test_t07_b0_touch` — modifying environment/h0/fixture fails all profiles
8. `test_t08_cross_fmt` — JSON pack row counts align with binary cache header fields post-fix

### Drafting guardrails

Do not place instruction nouns on build-path symbols, directories, or parameters. Do not embed oracle hints in environment comments. Keep pack_digest and witness rules in k4_pack.md, not only in tests. Ensure rc_verify diagnostics never name op_a, phase_b, or reconcile_c. Avoid boolean verdict fields in pack_out.json. Agent deliverables must be bash under environment/w2 and cooperating modules.

### Triviality Ledger

- Hardcoded pack_out.json from a fixture passes digest check only for one profile; t01 fails on luks/zfs/legacy witnesses.
- Host-prefix cache reuse via t2/h0_link.bin rhymes with correct output but fails t02 pack_digest cross-check against rescue-prefix bytes.
- shortcut.sh host-only binds pass health subcommand while t03 fails on zfs/legacy bind-path requirements.
- stage_only.sh can look green while pack_digest cross-check fails in t02.
- Mutating environment/h0/fixture fails t07 even if one profile appears locally healthy.

### Per-gate Pitfall Inventory

- RC1: Oracle must perform substantive cross-file bash edits across three lib modules, not byte-identical rewrites (GX4).
- RC2: Build-path symbols stay opaque; instruction nouns banned via code_forbidden_tokens; test names must not contain forbidden nouns.
- RC6: Instruction stays design-brief, not spec-complete with per-backend pivot/bind enumeration as a recipe.
- RC7/GX3: Bash oracle solve.sh must exceed 80 LOC substantive coordination or document WARN justification.
- CR1: Three build roots required; decoys stay off oracle path.
- GX9: Do not enumerate per-profile pack field values or witness numerics in instruction.md.
- GX10: Avoid naming both pass/fail polarities for one witness field in one sentence.
- GX8: Tests may import bash-invoked helpers only if implemented in environment/ or named in instruction.

### Initial Draft Commitments

- task.toml
- instruction.md
- output_contract.toml
- construction_manifest.json
- tests/test.sh
- tests/test_outputs.py
- solution/solve.sh
- environment/Dockerfile
- environment/h0/fixture/etc/os-release
- environment/h0/fixture/exec/sh
- environment/h0/fixture/lib/ld-linux-x86-64.so.2
- environment/p1/nvme.json
- environment/p1/luks.json
- environment/p1/zfs.json
- environment/p1/legacy.json
- environment/t2/h0_link.bin
- environment/t2/r0_link.bin
- environment/d3/floor.json
- environment/d3/p1_overrides.json
- environment/c4/k4_rules.md
- environment/c4/k4_limits.md
- environment/c4/k4_pack.md
- environment/c4/shortcut.sh
- environment/v5/rc_verify
- environment/v5/grid_engine.sh
- environment/v5/stage_only.sh
- environment/v5/apply_ctl.sh
- environment/w6/nvme_row.json
- environment/w6/luks_row.json
- environment/w6/zfs_row.json
- environment/w6/legacy_row.json
- environment/m7/mig7.sh
- environment/c4/k2/ctl_k.sh
- environment/w2/m2/m_phase.sh
- environment/v5/p2/assemble_p.sh
- environment/w2/run_entry.sh

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: environment/c4/k2/ctl_k.sh
  symbol: op_a
  kind: function
  signature: op_a()
  purpose: Emits bind/pivot manifest rows consumed by pack assembly per active profile

- path: environment/w2/m2/m_phase.sh
  symbol: phase_b
  kind: function
  signature: phase_b()
  purpose: Writes rescue-prefix ld.so cache bytes referenced by pack metadata

- path: environment/v5/p2/assemble_p.sh
  symbol: reconcile_c
  kind: function
  signature: reconcile_c()
  purpose: Materializes backend-specific minimal devnode records and invokes apply_ctl

#### flipping_point_contract

locations:
  - id: A
    path: environment/c4/k2/ctl_k.sh
    controls_tests: [test_t01_terminal, test_t07_b0_touch, test_t08_cross_fmt]
  - id: B
    path: environment/w2/m2/m_phase.sh
    controls_tests: [test_t03_p9_deep, test_t04_smoke_guard]
  - id: C
    path: environment/v5/p2/assemble_p.sh
    controls_tests: [test_t02_artifact_align, test_t05_visibility, test_t06_w3_idem]
no_single_location_flips_majority: true
concentration_cap: 0.5

#### decoy_manifest

- path: environment/c4/shortcut.sh
  kind: helper
  rhymes_with: op_a
  non_fix_purpose: Host-only recursive bind shortcuts for simulator builds

- path: environment/v5/stage_only.sh
  kind: module
  rhymes_with: reconcile_c
  non_fix_purpose: Writes stage summaries without pack_digest cross-check

#### code_forbidden_tokens

code_forbidden_tokens: [rescue, chroot, rebind, pivot, bind, ldso, cache, device, nodes, storage, backend, capability, offline, active, migration, recovery, rollback, health, status, intermediate, digest, verification, profiles, witness]
