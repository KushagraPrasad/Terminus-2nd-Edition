### Decision

GO — Attempt 3 (validated). Bank-ready seed `go-module-proxy-index-divergence` passes idea validation on a custom Go HTTP/SQL backend implementation, framed as a **repair_existing_system** task under the **build-and-dependency-management** category. Three mandated discoveries, SQLite database + filesystem consistency logic, three-location flipping-point contract, and constraint-complete public obligations without leaking cached metadata or GC transaction internals.

### Metadata

- version: 2
- Task name: go-module-proxy-index-divergence
- Title: Go module proxy index divergence
- Category: build-and-dependency-management
- Task shape: repair_existing_system
- Languages: ["go", "bash"]
- Difficulty: hard
- Codebase size: minimal (0–20 files under environment/)
- Subcategories: ["tool_specific"]
- Tags: ["go-proxy", "sqlite", "caching", "state-sync", "false-green", "build-toolchain"]
- Milestones: 0

## Authoring Brief

### Triviality (Avoidance) Ledger
- The task requires editing 3 Go modules across 3 distinct subdirectories (gc, catalog, goproxy) to solve. A single-file fix fails to reconcile state.
- Inconsistent caching (latest.meta) and index listings are verified by different tests, ensuring that simple NOP or simplistic overrides cannot pass.

### Per-gate Pitfall Inventory
- **Collapse Gate**: Shipped code symbols map to logical domain boundaries; no keywords overlap with the instruction vocabulary.
- **Predictability Gate (RC2)**: Kept package names generic (gc, catalog) to prevent predicting the fix path, with rc2 waivers applied for the main server domain names.
- **Hidden Invariants**: Python verifier assertions query endpoints directly rather than hardcoding DB values, using explicit variables to avoid hidden contracts.

### Initial Draft Commitments
- Shipped code contains three buggy files: gc.go, catalog.go, and handler.go.
- Verifier tests assert GC purging, list endpoint filtering, latest version cache invalidation, and fresh workspace resolution.

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle patch hunks, per-target facet answer tables, or narrative causal chains that name fix coordinates.

### Public contract

A local offline Go module proxy is provided. Developers report inconsistent behavior where:
- `go list -m -versions` reports one set of versions.
- `go get module@latest` resolves a different version.
- Certain historical versions can still be downloaded directly.
- Fresh workspaces fail while existing module caches continue to build.

No network access is available.

The agent must determine why the proxy exposes inconsistent module metadata and repair the proxy implementation under `/app` so every endpoint exposes a consistent view without breaking immutable module guarantees.

### platform_files

- path: task.toml
  role: metadata; must set `[environment] allow_internet = false` and `category = "build-and-dependency-management"`
- path: instruction.md
  role: natural public task prompt (symptoms-only public instruction)
- path: output_contract.toml
  role: local output declaration
- path: tests/test.sh
  role: verifier entrypoint; invoke pre-installed tools only (no apt/pip/curl bootstrap at runtime)
- path: tests/test_outputs.py
  role: domain verifier with ablation, permutation, and pipeline traps
- path: solution/solve.sh
  role: oracle applying oracle.patch and locked rebuild
- path: environment/Dockerfile
  role: build definition; pre-install go compiler, sqlite3, pytest, tmux, asciinema, and locked deps
- path: construction_manifest.json
  role: local authoring artifact mirroring Construction manifest below

### task_files

- path: environment/goproxy/main.go
  role: main proxy entrypoint wiring HTTP endpoints and database setup
- path: environment/goproxy/disk.go
  role: storage layer managing file writing/unlinking in filesystem path
- path: environment/catalog/catalog.go
  role: oracle frontier C — queries index database and verifies filesystem files exist
- path: environment/gc/gc.go
  role: oracle frontier A — garbage collection worker managing version purging and filesystem unlinks
- path: environment/goproxy/handler.go
  role: oracle frontier B — serves the HTTP endpoints and validates cached metadata against DB
- path: environment/goproxy/db.go
  role: SQLite connection helper decoy (non-fix)
- path: environment/goproxy/buffer.go
  role: in-memory cache helper decoy (non-fix)

### fix_frontier

- count: 3
- distribution: gc.go, handler.go, catalog.go
- naming_policy: explicit nouns banned from function signatures and structures
- forbidden_stems: ["proxy", "metadata", "version"]
- helpers_policy: no helper renames or additions
- symbol_thin_preferred: true

### contract_surface

- boolean_fields_max: 0
- direct_boolean_assertions_max: 6
- preferred_assertion_styles: HTTP response codes, JSON content equivalence, CLI exit codes
- forbidden_assertion_styles: hardcoded database state checks, simplistic boolean variables like active_state

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: Inconsistent state synchronization between local file storage, database index, and memory metadata cache.
- collapse_risk: Disclosing the cached latest.meta file location or GC cleanup omissions collapses the task to simple line edits.

### category_profile

- challenge_family: go_module_proxy_index_divergence
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: observable CLI behavior (go list, go get), HTTP endpoint specifications, local environment setup
- forbidden_instruction_leaks: caching mechanisms, SQLite DB schemas, garbage collection workflow details
- category_specific_hardness_bar: Go module resolution, HTTP server proxy, stateful SQLite DB database, and filesystem zip storage must all coordinate
- category_specific_verifier_risks: clean-build-only pass, mock-only HTTP checks, static caching fixes
- coverage_role: Adds Go module toolchain and proxy state synchronization coverage

### satisfiability_risk

- rc2_planned_name_risk: low — generic file and module names
- gx9_contract_risk: low — verification is based on CLI output and toolchain responses
- cr1_symbol_frontier_risk: low — three files with precise fixes
- hidden_contract_risk: low — all rules verified via standard Go toolchain behavior

### actionability_plan

- verifier_command_visible: go test /app/tests
- source_fix_intent_visible: yes
- generated_output_rule_visible: proxy responses and storage files
- exact_formula_home: module header comments in main.go
- schema_home: environment/goproxy/handler.go

### waiver_plan

- waivers_expected: false
- waiver_rationale: No special waivers needed for standard Go/SQLite task

### reference_pattern

- justification_if_none: This task is a novel reverse_engineering and repair task for Go toolchain module proxy behavior, designed from scratch without using any existing template.

### realism_source

- source_type: real_system
- evidence_basis: Based on real-world Go proxy synchronization problems seen in large organizations running Athens or custom module proxies.
- upstream_or_synthetic_rationale: Replicates real toolchain proxy misbehavior (divergent list vs fetch endpoints) in a minimized SQLite/filesystem layout.
- minimization_preserves: Metadata storage divergence, immutable zip storage on disk, and false-green states for local cached clients.
- synthetic_exception_review: Not applicable for real system source.

### Failure topology

The local Go module proxy is serving packages from local storage. The index version listing (`@v/list`) reads from a database table that got out of sync with the actual storage directory due to transaction failures in the garbage collection worker (`gc.go`). The GC worker deletes version records from the SQLite database but does not delete the corresponding `.zip` and `.info` files from the filesystem. Furthermore, the `@latest` endpoint reads version metadata from a cached file `latest.meta` managed by `handler.go`, which is not invalidated by the GC run. This leaves the proxy serving inconsistent version metadata, where cached Go environments can still download missing versions directly while fresh checkouts fail. The solver must coordinate fixes across the GC worker, database queries, and cached handlers to restore consistency.

### Environment shape

A single-container environment running a lightweight Go HTTP proxy server. The Go project lives under `environment/goproxy`. Database storage is backed by SQLite (`/app/data/proxy.db`), and zip/info blobs are stored in `/app/data/storage/`.

### Required artifacts

Standard TB3 task tree under `tasks/go-module-proxy-index-divergence/`: instruction.md, task.toml (`allow_internet = false`), output_contract.toml, construction_manifest.json, Dockerfile (pinned Go compiler and pytest), tests/test.sh, tests/test_outputs.py (≥6 tests), solution/solve.sh + oracle.patch, and the Go codebase files.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, cross_file_cross_format_invariants, environment_specific_cli_semantics, partial_observability_experiment_design
- adversarial_layers_count: 4
- fairness_guardrails: Instructions warn about cached vs clean build states; all endpoints checked dynamically; sqlite3 CLI available; no timing or latency thresholds.
- mechanism: false_green_intermediate_states
  placement: immutable zip files on disk stay valid, allowing cached builds to pass while clean runs fail
  why_model_misses_it: the agent will see successful builds in its initial state and assume the system is correct, missing that the index is actually broken
  fairness_guardrail: instructions explicitly warn that fresh builds behave differently from cached builds
- mechanism: cross_file_cross_format_invariants
  placement: SQL database index, latest.meta cache file, and directory zip files must be kept consistent
  why_model_misses_it: the agent will fix one storage format (e.g. database) but forget to update or invalidate the others
  fairness_guardrail: all endpoints must be consistently correct for verifier tests to pass
- mechanism: environment_specific_cli_semantics
  placement: go list and go get behaviors query different HTTP endpoints
  why_model_misses_it: the model might not know that go list -m -versions queries @v/list, while go get module@latest queries @latest
  fairness_guardrail: the instructions describe which command yields which symptom
- mechanism: partial_observability_experiment_design
  placement: the proxy runs as a daemon/server; state must be observed via proxy logs and CLI queries
  why_model_misses_it: the model cannot step-debug and must run curl queries or inspect sqlite files to diagnose the state
  fairness_guardrail: sqlite3 CLI tool and proxy logs are available inside the sandbox

### calibration_plan

```yaml
oracle_runs: 3
no_op_runs: 3
target_agent_runs: 20
comparator_agent_runs: 20
human_sanity: Completed by author to confirm solvability.
shortcut_audit: >
  read test helpers and transcribe → all algorithm helpers removed
  load env file via exec and transcribe → exec pattern removed
  static JSON output → fails verifier rerun
  patch one file only → cross-file invariant fails
ablation_plan: >
  Remove each mechanism one at a time and confirm difficulty drops.
pass_rate_target:
  hard_max_pct: 20
  too_easy_threshold_pct: 80
  basis: Part E worst-model accuracy on platform (GPT-5.5 + Claude Opus 4.8, Jun 12 2026)
```

### verifier_scoring_plan

- metrics: functional_correctness=0.5, hidden_invariants=0.25, state_hygiene=0.1, interface_correctness=0.1, deliverable_completeness=0.05
- overall_threshold: 1.0
- reward_output: reward.json
- binary_threshold_rule: functional_correctness and hidden_invariants must pass perfectly

### subtype_milestone_plan

- subcategories: ["tool_specific"]
- milestone_count: 0
- sequential_dependency: none
- local_only_data: true
- sidecar_or_protocol_notes: requires Go compiler to run the verifier locally

### Drafting guardrails

Instruction must only mention CLI symptoms and proxy specifications. It must not reference `latest.meta`, the SQLite database table schemas, the `PurgeVersion` function, or the filesystem directory location under `/app/data/storage`. Test names and symbol table variables must not contain `proxy`, `metadata`, or `version`.

### Triviality Ledger

- Static mock responses fail `test_latest_meta_invalidation` because the verifier updates versions dynamically.
- Fixing the GC worker without invalidating `latest.meta` fails `test_latest_resolves_correctly`.
- Fixing HTTP handler cache reads without cleaning up files from disk fails `test_gc_deletes_zips`.
- Keeping `/@latest` tied only to the newest database row fails `test_latest_skips_incomplete_newest_release` when the newest row's files are missing and an older complete release exists.
- Serving direct downloads from disk without rechecking the live index fails `test_download_rejects_index_stale_file` when a stale artifact remains after its index row disappears.

### Per-gate Pitfall Inventory

- RC1/GX2: Forbid single-file wholesale replace. Semantic changes must touch `gc.go`, `handler.go`, and `catalog.go`.
- RC2: Ensure test names (`test_list_endpoints`) and symbols avoid forbidden tokens (`proxy`, `metadata`, `version`).
- RC3: Instruction is symptoms-only and does not name the caching file or GC details.
- CR1/CR2: Verify symbol table matches the flipping-point locations exactly.

### Initial Draft Commitments

- tasks/go-module-proxy-index-divergence/task.toml
- tasks/go-module-proxy-index-divergence/instruction.md
- tasks/go-module-proxy-index-divergence/output_contract.toml
- tasks/go-module-proxy-index-divergence/construction_manifest.json
- tasks/go-module-proxy-index-divergence/tests/test.sh
- tasks/go-module-proxy-index-divergence/tests/test_outputs.py
- tasks/go-module-proxy-index-divergence/solution/solve.sh
- tasks/go-module-proxy-index-divergence/solution/oracle.patch
- tasks/go-module-proxy-index-divergence/environment/Dockerfile
- tasks/go-module-proxy-index-divergence/environment/goproxy/main.go
- tasks/go-module-proxy-index-divergence/environment/goproxy/disk.go
- tasks/go-module-proxy-index-divergence/environment/goproxy/catalog.go
- tasks/go-module-proxy-index-divergence/environment/goproxy/gc.go
- tasks/go-module-proxy-index-divergence/environment/goproxy/handler.go
- tasks/go-module-proxy-index-divergence/environment/goproxy/db.go
- tasks/go-module-proxy-index-divergence/environment/goproxy/buffer.go

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: environment/goproxy/gc.go
  symbol: PurgeVersion
  kind: function
  signature: func PurgeVersion(db *sql.DB, version string) error
  purpose: Removes index entries and cleans corresponding filesystem zips.
- path: environment/goproxy/handler.go
  symbol: ServeLatest
  kind: function
  signature: func ServeLatest(w http.ResponseWriter, r *http.Request)
  purpose: Serves the latest metadata cache and validates it against current index state.
- path: environment/goproxy/catalog.go
  symbol: QueryVersions
  kind: function
  signature: func QueryVersions(db *sql.DB, module string) ([]string, error)
  purpose: Queries index database and verifies existence of matching zip files.
```

#### flipping_point_contract

```
- location_id: gc_unlink
  path: environment/goproxy/gc.go
  controls_tests:
    - test_gc_purges_storage_files
    - test_gc_invalidates_latest_cache
- location_id: handler_latest
  path: environment/goproxy/handler.go
  controls_tests:
    - test_latest_resolves_active_release
    - test_latest_skips_incomplete_newest_release
    - test_latest_meta_cache_invalidation
    - test_download_rejects_index_stale_file
- location_id: index_query
  path: environment/goproxy/catalog.go
  controls_tests:
    - test_list_endpoint_filtering
    - test_fresh_workspace_resolution
```

- no_single_location_flips_majority: true
- concentration_cap: 0.5
