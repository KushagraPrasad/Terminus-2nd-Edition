### Decision
GO — Attempt 1. Realized the token-revocation-freshness repair idea as a multi-component TypeScript debugging task: one token validation module, one cache invalidation module, and one SQLite persistence store.

### Metadata
- version: 2
- Task name: token-revocation-freshness
- Title: Token Revocation and Freshness Coordinator
- Category: security
- Task shape: repair_existing_system
- Languages: ["typescript"]
- Difficulty: hard
- Codebase size: minimal
- Subcategories: ["db_interaction"]
- Tags: ["security", "auth", "cache", "sqlite", "jwt"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires repairing three distinct bugs across the security authorization flow. NOP runs score 0/3, and making a localized fix in only one area will fail the verifier.
- The bugs include:
  1. Wildcard scope/principal revocations do not propagate to the LRU Cache unless wildcard matching checks are explicitly validated on cache evictions.
  2. Clock skew between the authorization server and the local database is not compensated because system time is compared directly to token headers.
  3. SQLite DB sync writes do not run within transactional blocks, leaving sequence checkpoints updated but the blacklist table empty on simulated crash events.

### Per-gate Pitfall Inventory
- **Collapse Gate**: Symbols in `construction_manifest.json` are thin and mapped to standard TypeScript class/method names.
- **Predictability Gate**: The folder name does not explicitly reveal the patch implementation details, preventing a purely copy-paste fix.
- **Hidden Invariants**: All requirements are declared in `instruction.md` and `output_contract.toml`.

### Initial Draft Commitments
- Shipped code contains three distinct buggy modules: cache.ts, validator.ts, and store.ts.
- Verifier tests assert:
  - Cache handles wildcard scopes and evictions correctly.
  - Client handles rotated keys fallback correctly.
  - SQLite DB transaction logic functions correctly after crash simulation.

### Public contract
A token gateway fails to immediately reject revoked tokens under high-concurrency requests and epoch updates, leaving a window of stale authority validation. Fix the token gateway logic under `/app/environment` to ensure correctness across dynamic revocations and clock skew adjustments.

### Failure topology
The gateway accepts unauthorized tokens due to improper LRU cache invalidation, ignores clock skew compensation headers, and permits replayed sequence rollbacks after coordinator restarts.

### Environment shape
A TypeScript Node.js runtime environment. Scaffolding loads SQLite and crypto packages under `environment/`.

### Required artifacts
Standard task tree containing task.toml, instruction.md, environment/Dockerfile, tests/test.sh, tests/test_outputs.py, solution/solve.sh.

### Test plan
- `test_token_signature_rotation`
- `test_expired_fallback_keys`
- `test_wildcard_eviction`
- `test_ttl_expiry_sync`
- `test_db_transaction_crash_recovery`
- `test_monotonic_sequence_rollback`

### Drafting guardrails
Keep instruction.md symptom-focused. Describe symptoms and expected invariants, but do not outline the direct code patch locations.

### satisfiability_risk
- rc2_planned_name_risk: low
- gx9_contract_risk: low
- cr1_symbol_frontier_risk: low
- hidden_contract_risk: low

### task_shape
- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: Distributed cache invalidation, key rotation synchronization, and database transaction consistency.
- collapse_risk: Local fixes to cache check loops fail database transaction and fallback security checks.

### platform_files
- path: task.toml
  role: Task metadata
- path: instruction.md
  role: Task instructions
- path: output_contract.toml
  role: Output schemas
- path: tests/test.sh
  role: Verifier script
- path: tests/test_outputs.py
  role: Verifier test cases
- path: solution/solve.sh
  role: Solution patch script
- path: environment/Dockerfile
  role: Container runtime environment
- path: construction_manifest.json
  role: Mapping manifest

### task_files
- path: environment/src/cache.ts
  role: Token cache eviction logic
- path: environment/src/validator.ts
  role: Gateway token validator
- path: environment/src/store.ts
  role: SQLite database sync client
- path: environment/src/jwks.ts
  role: JWKS key retrieval decoy module
- path: environment/src/decoy_logger.ts
  role: Audit logger decoy module

### fix_frontier
- count: 3
- distribution: environment/src/cache.ts, environment/src/validator.ts, environment/src/store.ts
- naming_policy: standard TypeScript gateway architecture
- forbidden_stems: []
- helpers_policy: allowed
- symbol_thin_preferred: true

### contract_surface
- boolean_fields_max: 0
- direct_boolean_assertions_max: 2
- preferred_assertion_styles: ["audit log structure checks", "SQLite state validations"]
- forbidden_assertion_styles: ["plain boolean return assertions"]

### category_profile
- challenge_family: revocation_cache_drift
- profile_name: security_authority_split
- allowed_instruction_disclosures: "assets, principals, allowed/denied actions, audit traces, authority boundary, repro command, and externally tested safety invariants."
- forbidden_instruction_leaks: "vulnerable sink, trust-boundary implementation location, exploit primitive, patch rule, sanitizer name, or exact guard."
- category_specific_hardness_bar: "Reconciliation of token state across changing principals, freshness, and revocation status."
- category_specific_verifier_risks: "None."
- coverage_role: target

### calibration_plan
```yaml
oracle_runs: 3
no_op_runs: 3
target_agent_runs: 20
comparator_agent_runs: 20
human_sanity: Verified that typescript validation and database transaction checks flag intermediate errors.
shortcut_audit: Directly returning true on all validation calls fails signature tests.
ablation_plan: Removing wildcard cache check logic reduces verification complexity.
pass_rate_target:
  hard_max_pct: 20
  too_easy_threshold_pct: 80
  basis: Worst-model pass rate on platform auto-eval.
```

### verifier_scoring_plan
- metrics:
  - metric: functional_correctness
    weight: 0.45
    criterion: "Passes all JWT signature and caching checks."
  - metric: hidden_invariants
    weight: 0.25
    criterion: "Cache handles wildcard scopes and evictions correctly."
  - metric: state_hygiene
    weight: 0.15
    criterion: "SQLite DB transaction logic functions correctly after crash simulation."
  - metric: interface_correctness
    weight: 0.10
    criterion: "Client handles rotated keys fallback correctly."
  - metric: deliverable_completeness
    weight: 0.05
    criterion: "Outputs /logs/verifier/auth_audit_trace.json matches schema."
- overall_threshold: 1.0
- reward_output: reward.txt
- binary_threshold_rule: all tests must pass

### subtype_milestone_plan
- subcategories: ["db_interaction"]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: none

### actionability_plan
- verifier_command_visible: npm test
- source_fix_intent_visible: "Fix the token gateway logic under /app/environment."
- generated_output_rule_visible: "/logs/verifier/auth_audit_trace.json"
- exact_formula_home: instruction
- schema_home: instruction

### waiver_plan
- waivers_expected: false
- waiver_rationale: "No waivers planned."

### reference_pattern
- justification_if_none: "This task implements distributed token revocation and JWT validation cache drift checks."

### realism_source
- source_type: real_bug
- evidence_basis: "Inspired by OAuth 2.0 Token Revocation RFC 7009 / RFC 7519 JWT cache desynchronization vulnerabilities in distributed gateways."
- upstream_or_synthetic_rationale: "Represents standard JWT invalidation caching and key rotation challenges."
- minimization_preserves: "Token validations, database structures, and cache maps."
- synthetic_exception_review: "None."

### difficulty_mechanism_plan
- mechanisms: [false_green_intermediate_states, stateful_multi_step_dependencies, cross_file_cross_format_invariants, rollback_recovery_requirements]
- adversarial_layers_count: 4
- fairness_guardrails: "All invariants and build contracts are documented cleanly."
- mechanism: false_green_intermediate_states
  placement: "Single token cache updates pass basic local validation but fail when multi-step wildcard revocations occur under concurrent requests."
  why_model_misses_it: "Model targets single cache evictions without verifying wildcard pattern support."
  fairness_guardrail: "Instructions specify wildcard claim propagation requirements."
- mechanism: stateful_multi_step_dependencies
  placement: "Verifier runs sequential batches of sync notifications and restarts the client gateway."
  why_model_misses_it: "Model assumes clean database cache state on each call, missing persistent database transaction sync errors."
  fairness_guardrail: "The output contract schema lists sequence histories and database states under verify commands."
- mechanism: cross_file_cross_format_invariants
  placement: "The SQLite blacklist database, the JWT JWKS cache, and the memory cache must remain fully reconciled."
  why_model_misses_it: "Model implements cache updates but fails to sync sequence checkpoints in the database."
  fairness_guardrail: "The instruction documents expected state consistency boundaries across components."
- mechanism: rollback_recovery_requirements
  placement: "The verifier resets the sequence epoch of the auth server (restarting seq=0) to trigger client rollback verification."
  why_model_misses_it: "Model assumes sequence numbers always increase monotonically without handling system restarts."
  fairness_guardrail: "The instructions declare sequence verification and epoch recovery safety rules."
