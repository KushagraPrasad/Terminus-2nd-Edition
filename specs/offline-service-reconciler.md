### Decision

GO — Attempt 1. Validated seed from system-administration/5 (Offline Service Reconciler) after hard-only screening, uniqueness check, and full Step 2a validation with 0F/0W. Constrained_build shape with distributed_reconciliation profile. Core hardness derives from discovering the trust-anchor authority ordering among three evidence surfaces (probe cache TOML, signed inventory JSON, operator override YAML) and implementing idempotent merge without algorithm disclosure. Three coordinated fix locations with independent test subsets; pack_digest cross-check provides structural anti-shortcut gate.

### Metadata

- version: 2
- Task name: offline-service-reconciler
- Title: Offline host inventory reconciler
- Category: system-administration
- Task shape: constrained_build
- Languages: ["go", "bash"]
- Difficulty: hard
- Codebase size: small (20–200 files under environment/)
- Subcategories: []
- Tags: ["offline", "airgapped", "fleet", "state", "authority", "idempotency", "go"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, or narrative causal chains that name fix coordinates.

### Public contract

An offline fleet management system must reconcile host state from three sources that can disagree: a cached probe file per host, a signed central inventory, and operator override declarations. After a partial sync, some hosts have contradictory role assignments across these three sources.

Implement a reconciler under `/app` that:
1. Reads probe cache files from `/app/environment/b6/`, signed inventory from `/app/environment/g2/sv_inv.json`, and operator overrides from `/app/environment/f8/op_ov.yaml`
2. Produces `/app/output/host_inventory.json` — the canonical host inventory — and `/app/output/run_report.json`
3. The reconciler must pass all four host profiles (nvme, luks, zfs, legacy) and produce consistent `pack_digest` across both output files
4. Running the reconciler a second time must produce byte-identical output artifacts

The verifier checks:
- All four profile tests pass with correct canonical host role assignment
- `pack_digest` in `host_inventory.json` matches `pack_digest` in `run_report.json`
- Both output artifacts conform to the schema in `output_contract.toml`
- Second run produces identical outputs (idempotency)

Authority and digest rules are documented in `environment/d5/rc_rules.md` and `environment/d5/pk_rules.md`.

Hardcoding output artifacts, copying probe cache directly without reconciliation, or patching the verifier are insufficient.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "system-administration"`
- path: instruction.md
  role: natural public constraint-complete task prompt
- path: output_contract.toml
  role: local output declaration for host_inventory.json and run_report.json
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed pytest only (no runtime apt/pip/curl)
- path: tests/test_outputs.py
  role: domain verifier (7 tests)
- path: solution/solve.sh
  role: oracle coordinating rz_g4, kv_w7, mx_r9 fixes
- path: environment/Dockerfile
  role: build definition; bake Go compiler and Go test runners offline
- path: construction_manifest.json
  role: local authoring artifact mirroring symbol table

### task_files

- path: environment/p4/rz_g4.go
  role: oracle frontier A — authority resolver with intentional defect in rz_g4
- path: environment/p4/rz_sc.go
  role: decoy diagnostics scanner; not on fix path
- path: environment/p4/kv_w7.go
  role: oracle frontier B — signed source verifier and pack_digest computation with intentional defect in kv_w7
- path: environment/p4/kv_au.go
  role: decoy audit reporter; not a fix site
- path: environment/p4/mx_r9.go
  role: oracle frontier C — idempotent merger with intentional defect in mx_r9
- path: environment/p4/main.go
  role: entry point that calls all three modules; not a fix site
- path: environment/p4/go.mod
  role: Go module definition
- path: environment/b6/nx_a.toml
  role: cached probe file for host A with nvme profile
- path: environment/b6/nx_b.toml
  role: cached probe file for host B with luks profile
- path: environment/b6/nx_c.toml
  role: cached probe file for host C with zfs profile
- path: environment/b6/nx_d.toml
  role: cached probe file for host D with legacy profile
- path: environment/g2/sv_inv.json
  role: signed inventory with trust anchors; authority override source
- path: environment/f8/op_ov.yaml
  role: operator-level role overrides
- path: environment/d5/rc_rules.md
  role: trust anchor semantics and authority ordering rules (solver-visible)
- path: environment/d5/pk_rules.md
  role: pack_digest formula specification (solver-visible)

### fix_frontier

- count: 3
- distribution: One substantive function each in environment/p4/rz_g4.go (rz_g4), environment/p4/kv_w7.go (kv_w7), and environment/p4/mx_r9.go (mx_r9).
- naming_policy: Opaque fix-path identifiers using two-char prefix and alphanumeric suffix; instruction nouns must not grep onto frontier symbols.
- forbidden_stems: sync, canonical, authority, trust, anchor, airgapped, fleet, idempotency, merge, resolver, verifier, signer
- helpers_policy: Co-resident decoy modules rz_sc.go and kv_au.go are listed in task_files and excluded from the flipping-point contract.
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 1
- direct_boolean_assertions_max: 1
- preferred_assertion_styles:
  - dict equality on full regenerated host_inventory.json versus profile-expected fixture
  - pack_digest string equality between host_inventory.json and run_report.json
  - rerun stability: run twice, assert byte-identical output artifacts
- forbidden_assertion_styles:
  - scenario-to-key answer grids in instruction text
  - boolean verdict fields per profile in instruction

### task_shape

- type: constrained_build
- instruction_framing: constraint-complete
- hardness_source: design search — agent must design the authority resolution strategy and idempotent merge without a recipe
- collapse_risk: If the trust anchor priority ordering is named in instruction or the pack_digest formula is disclosed in instruction text, the task collapses into transcription of two config rules.

### category_profile

- challenge_family: offline host state reconciliation
- profile_name: distributed_reconciliation
- allowed_instruction_disclosures: Evidence surfaces (probe cache, signed inventory, operator overrides), output artifact names and schema, verifier command, rerun requirement, four profile names.
- forbidden_instruction_leaks: Canonical source discovery algorithm, merge priority ordering, trust anchor location, pack_digest formula, or which artifact wins under conflict.
- category_specific_hardness_bar: Solver reconciles multiple truth surfaces with idempotency and conflict lineage across four profiles.
- category_specific_verifier_risks: Count-only checks, last-write-wins shortcuts, golden merged fixture hardcoding, and static JSON output bypass.
- coverage_role: Adds offline host state reconciliation coverage through constrained_build without duplicating neighboring topology families.

### difficulty_mechanism_plan

- mechanisms: [deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, stateful_multi_step_dependencies, false_green_intermediate_states]
- adversarial_layers_count: 4
- fairness_guardrails: All authority rules documented in environment/d5/rc_rules.md; digest formula in environment/d5/pk_rules.md; rerun requirement stated in instruction
- mechanism: deceptive_but_valid_local_evidence
  placement: One evidence surface remains internally consistent but non-canonical; b6/nx_c.toml shows one role while g2/sv_inv.json overrides it; naive implementations trust the first green surface
  why_model_misses_it: Models default to last-write-wins; the signed-source trust anchor is a non-obvious precedence rule requiring reading rc_rules.md
  fairness_guardrail: rc_rules.md is solver-visible; trust anchor semantics documented without naming the fix function
- mechanism: cross_file_cross_format_invariants
  placement: Three evidence surfaces must agree on role before pack_digest is computed; fixing one format while leaving another inconsistent breaks pack_digest cross-check
  why_model_misses_it: Models fix the most visible conflict but miss that overrides must be applied after signed-source resolution in a specific order
  fairness_guardrail: output_contract.toml declares both artifact paths and pack_digest cross-check requirement; schemas publicly disclosed
- mechanism: stateful_multi_step_dependencies
  placement: reconciler must be run twice to verify idempotency; a non-idempotent merge appends duplicate entries on second run producing different output
  why_model_misses_it: Models stop after first successful run; rerun requirement stated in instruction but the specific failure mode requires probing intermediate state
  fairness_guardrail: rerun stability test visible in test_outputs.py; instruction states rerun must produce identical output
- mechanism: false_green_intermediate_states
  placement: early health check subcommand may report success before full four-profile matrix converges; pack_digest cross-check provides second gate
  why_model_misses_it: Models stop after health subcommand passes; full profile matrix test requires all three modules correctly wired
  fairness_guardrail: verifier command is the full --all-profiles invocation; health subcommand is a known insufficient shortcut documented in instruction

### satisfiability_risk

- rc2_planned_name_risk: low — fix-path filenames and directories use opaque identifiers (p4, b6, g2, f8, d5, rz_g4, kv_w7, mx_r9); no instruction noun appears in any path component
- gx9_contract_risk: low — output contract exposes observations and artifact schemas; no verdict-restating boolean fields per profile
- cr1_symbol_frontier_risk: medium — three fix-path symbols with thin helper surface; oracle-touched helpers must stay symbol-thin and avoid prompt-noun function names
- hidden_contract_risk: low — authority ordering, digest formula, and rerun rules anchored in solver-visible environment/d5/ files before drafting

### actionability_plan

- verifier_command_visible: single local command runs reconciler and validates canonical output from generated artifacts: `go run /app/environment/p4/main.go --all-profiles`
- source_fix_intent_visible: yes at product level — produce canonical output under airgapped sync constraints without revealing algorithm or priority ordering
- generated_output_rule_visible: instruction names generated output artifacts, pack_digest cross-check requirement, and rerun behavior; static hand-authored outputs are insufficient
- exact_formula_home: environment/d5/pk_rules.md; pack_digest formula is solver-visible without being disclosed in instruction
- schema_home: instruction and output_contract.toml; public artifact schema names observations and artifact paths, not verdict booleans

### waiver_plan

- waivers_expected: false
- waiver_rationale: No waiver expected; authority ordering and digest formula anchored in solver-visible docs without naming the solution route. RC2 risk is low with opaque path and frontier naming.

### reference_pattern

- justification_if_none: No promoted reference task matches this offline host inventory reconciliation with three-surface authority quorum topology; this seed introduces distinct distributed_reconciliation coverage in system-administration.

### realism_source

- source_type: real_constraint
- evidence_basis: tool behavior
- upstream_or_synthetic_rationale: Grounded in real offline inventory reconciler behavior for airgapped fleet management systems where probe cache, signed inventory, and operator overrides disagree on host role. Pattern occurs in Ansible offline mode, Salt master-less setups, and Puppet enterprise airgapped deployments.
- minimization_preserves: host role authority coupling across probe cache TOML, signed inventory JSON, and operator override YAML; pack_digest cross-validation; rerun idempotency; four-profile matrix coverage.
- synthetic_exception_review: not required for real_constraint source; reject if Step 2b cannot wire the trust anchor semantics from a real system pattern while preserving the three-surface coupling structure

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: first-look dry run on instruction plus environment listing only; reviewer confirms no patch site named and pack_digest formula not in instruction
- shortcut_audit: agents that only hardcode host_inventory.json or copy probe cache directly without reconciliation must fail pack_digest cross-check; agents that fix one module only must fail majority of profile tests
- ablation_plan: revert each of three fix locations one at a time and confirm the corresponding test subset fails while others pass; confirm no single revert flips majority
- pass_rate_target:
  - hard_max_pct: 20
  - too_easy_threshold_pct: 80
  - basis: Part E worst-model accuracy on platform (GPT-5.5 + Claude Opus 4.8)

### verifier_scoring_plan

- metrics:
  - functional_correctness: weight=0.45; criterion=all four profile tests pass with correct canonical host inventory
  - hidden_invariants: weight=0.20; criterion=pack_digest cross-check passes between host_inventory.json and run_report.json
  - state_hygiene: weight=0.15; criterion=rerun idempotency test passes; second run produces byte-identical output
  - interface_correctness: weight=0.15; criterion=output artifacts conform to declared schema in output_contract.toml
  - deliverable_completeness: weight=0.05; criterion=both required output artifacts present at declared paths
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: single failed pytest assertion fails the suite; reward is 0 if any test fails

### subtype_milestone_plan

- subcategories: [tool_specific]
- milestone_count: 0
- sequential_dependency: conceptually staged but delivered as one task; no milestone gating required
- local_only_data: true
- sidecar_or_protocol_notes: not required beyond local fixtures under environment/b6/, environment/g2/, environment/f8/

### Failure topology

Three evidence surfaces can disagree on host role after a partial airgapped sync. Naive last-write-wins merge produces a canonical output that passes a health subcommand but fails pack_digest cross-check because the signed-source trust anchor is not honored. Fixing authority ordering for one profile without fixing idempotent merge breaks zfs and legacy profiles on rerun. The pack_digest formula ties both output JSON files to a content-addressed hash computed from the reconciled state — hand-authored JSON or static outputs fail this cross-check. A non-idempotent merger appends duplicate entries on second run, producing divergent output artifacts. All three fix locations (rz_g4, kv_w7, mx_r9) must be correct simultaneously; no single fix passes majority of tests.

### Environment shape

- `environment/p4/` — Go reconciler modules (rz_g4.go, rz_sc.go, kv_w7.go, kv_au.go, mx_r9.go, main.go, go.mod)
- `environment/b6/` — per-host cached probe TOML files (nx_a through nx_d)
- `environment/g2/` — signed inventory JSON with trust anchors
- `environment/f8/` — operator-level override YAML
- `environment/d5/` — rc_rules.md (authority ordering) and pk_rules.md (digest formula)

### Required artifacts

Step 2b creates: `task.toml` (`allow_internet = false`, `category = "system-administration"`), `instruction.md`, `output_contract.toml`, `tests/test.sh`, `tests/test_outputs.py` (7 tests), `solution/solve.sh` (Go/bash oracle with substantive multi-module coordination ≥80 LOC or documented GX3 justification), `environment/Dockerfile` (Go and python+pytest baked in offline), all task_files above, and `construction_manifest.json` matching the symbol table. Environment must contain 15+ non-Docker files. Primary agent implementation language is **Go**.

### Test plan

1. `test_gz_nvme_p3` — canonical host_inventory.json nvme role correct; controls fix location A
2. `test_gz_luks_p3` — canonical host_inventory.json luks role correct; controls fix location A
3. `test_wk_xsig_p5` — pack_digest in host_inventory.json matches pack_digest in run_report.json; controls fix location B
4. `test_wk_report_p5` — run_report.json conforms to declared schema; controls fix location B
5. `test_rx_zfs_p7` — canonical host_inventory.json zfs role correct; controls fix location C
6. `test_rx_legacy_p7` — canonical host_inventory.json legacy role correct; controls fix location C
7. `test_rx_rerun_p7` — second reconciler run produces byte-identical output artifacts; controls fix location C

### Drafting guardrails

Do not place instruction nouns on fix-path symbols, directories, or parameters. Do not embed oracle hints in environment comments. Keep pack_digest formula in pk_rules.md, not only in tests. Ensure health subcommand does not name rz_g4, kv_w7, or mx_r9. Avoid boolean verdict fields in host_inventory.json. Agent deliverables must be Go under environment/p4/ (three fixed modules).

### Triviality Ledger

- Hardcoded host_inventory.json from a fixture fails pack_digest cross-check because the hash is computed from reconciled state, not static JSON.
- Copying probe cache directly without resolving signed-source trust anchor produces wrong roles for hosts with inventory overrides.
- Fixing only rz_g4 (frontier A) passes nvme and luks profile tests but fails override idempotency for zfs and legacy.
- Health subcommand can pass while pack_digest cross-check fails; verifier requires full --all-profiles run.
- Non-idempotent merge passes first run but fails test_rx_rerun_p7 idempotency test on second run.

### Per-gate Pitfall Inventory

- RC1: Oracle must perform substantive multi-module Go fixes across three modules, not byte-identical rewrites (GX4).
- RC2: Fix-path filenames and directories use opaque identifiers; instruction nouns must not appear in any path component or symbol name.
- RC6: Instruction stays constraint-complete, not spec-complete with explicit authority ordering or merge algorithm as recipe.
- RC7/GX3: Go/bash oracle solve.sh must exceed 80 LOC substantive coordination or document WARN justification.
- CR1: Three fix roots required; decoys (rz_sc.go, kv_au.go) stay off oracle path.
- GX9: Do not enumerate per-host role values or pack_digest expected values in instruction.md.
- GX10: Avoid naming both pass/fail polarities for one profile field in one sentence.

### Initial Draft Commitments

- task.toml
- instruction.md
- output_contract.toml
- construction_manifest.json
- tests/test.sh
- tests/test_outputs.py
- solution/solve.sh
- environment/Dockerfile
- environment/p4/rz_g4.go
- environment/p4/rz_sc.go
- environment/p4/kv_w7.go
- environment/p4/kv_au.go
- environment/p4/mx_r9.go
- environment/p4/main.go
- environment/p4/go.mod
- environment/b6/nx_a.toml
- environment/b6/nx_b.toml
- environment/b6/nx_c.toml
- environment/b6/nx_d.toml
- environment/g2/sv_inv.json
- environment/f8/op_ov.yaml
- environment/d5/rc_rules.md
- environment/d5/pk_rules.md

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: environment/p4/rz_g4.go
  symbol: rz_g4
  kind: function
  signature: func rz_g4(b6_path string, g2_path string) (map[string]map[string]string, error)
  purpose: Resolve authority among evidence surfaces given signed-source trust anchor; returns canonical role map

- path: environment/p4/kv_w7.go
  symbol: kv_w7
  kind: function
  signature: func kv_w7(g2_path string, resolved_roles map[string]map[string]string) (string, error)
  purpose: Verify signed source and compute pack_digest from reconciled role map and content-addressed headers

- path: environment/p4/mx_r9.go
  symbol: mx_r9
  kind: function
  signature: func mx_r9(f8_path string, resolved_roles map[string]map[string]string) (map[string]map[string]string, error)
  purpose: Merge override YAML idempotently onto resolved role map; returns final canonical output

#### flipping_point_contract

locations:
  - id: A
    path: environment/p4/rz_g4.go
    controls_tests: [test_gz_nvme_p3, test_gz_luks_p3]
  - id: B
    path: environment/p4/kv_w7.go
    controls_tests: [test_wk_xsig_p5, test_wk_report_p5]
  - id: C
    path: environment/p4/mx_r9.go
    controls_tests: [test_rx_zfs_p7, test_rx_legacy_p7, test_rx_rerun_p7]
no_single_location_flips_majority: true
concentration_cap: 0.43

#### decoy_manifest

- path: environment/p4/rz_sc.go
  kind: module
  rhymes_with: rz_g4
  non_fix_purpose: Diagnostics scanner that reads b6/ metadata for reporting; not on authority resolution fix path

- path: environment/p4/kv_au.go
  kind: module
  rhymes_with: kv_w7
  non_fix_purpose: Audit reporter that validates field presence but does not compute pack_digest; not a fix site

#### code_forbidden_tokens

code_forbidden_tokens: [sync, canonical, authority, trust, anchor, airgapped, fleet, idempotency, merge, resolver, verifier, signer]
