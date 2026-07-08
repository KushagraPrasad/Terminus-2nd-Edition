# Frontier 56 — Phase 1 Candidate Bank (80 concepts)

Generated for anti-template diversity pipeline. Do not implement until Phase 4 lock.

---

## Benchmark category: `build-dependency`

### 1. Offline lockfile rehydration gap
- **id**: `offline-lockfile-rehydration-gap`
- **Status**: `bank-ready`
- **Benchmark category**: `build-dependency`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `offline_lockfile_rehydration`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `offline lockfile rehydration`
- **Framing**: Incremental offline builds succeed on clean tree but fail when lockfile digest disagrees with vendored tarball generation.
- **Discoveries / design insights**:
  - lockfile records hash of generated crate not source manifest
  - vendor dir stale after feature unification reorder
  - cargo metadata vs resolver graph disagree on patch edges
- **Frontier failure modes**:
  - resolver edge misread
  - patch override ordering bug
  - stale vendor tarball hash
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. ABI rebuild drift detector
- **id**: `abi-rebuild-drift-detector`
- **Status**: `bank-ready`
- **Benchmark category**: `build-dependency`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `abi_rebuild_drift`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `ABI rebuild drift`
- **Framing**: Shared library consumers crash after rebuild though soname unchanged and link succeeds.
- **Discoveries / design insights**:
  - struct padding differs under new compiler default
  - generated header not rebuilt when .rs layout changes
  - LTO strips symbol versioning expected by loader
- **Frontier failure modes**:
  - header generation skip
  - LTO symbol visibility drift
  - padding layout mismatch
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Hermetic sandbox build contract
- **id**: `hermetic-sandbox-build-contract`
- **Status**: `bank-ready`
- **Benchmark category**: `build-dependency`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `hermetic_sandbox_build`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `constrained_build`
  - `instruction_framing`: `design-brief`
  - `hardness_source`: `design search`
- **Topology**: `hermetic sandbox build`
- **Framing**: Build must reproduce bit-identical artifacts under strict namespace and offline mirror constraints.
- **Discoveries / design insights**:
  - proc macro reads host /etc during build
  - rustc workspace feature unification order affects metadata hash
  - build script emits nondeterministic timestamp
- **Frontier failure modes**:
  - proc macro host leak
  - feature unification ordering
  - timestamp nondeterminism
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Cross-compile sysroot skew
- **id**: `cross-compile-sysroot-skew`
- **Status**: `bank-ready`
- **Benchmark category**: `build-dependency`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `cross_compile_sysroot_skew`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `cross compile sysroot skew`
- **Framing**: Target binary links on build host but faults on device due to sysroot library generation mismatch.
- **Discoveries / design insights**:
  - linker script path differs host vs target sysroot
  - multilib selection wrong for soft-float ABI
  - pkg-config returns host flags on cross path
- **Frontier failure modes**:
  - sysroot path confusion
  - multilib ABI mismatch
  - pkg-config host leak
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Bazel query graph stale edge
- **id**: `bazel-query-graph-stale-edge`
- **Status**: `bank-ready`
- **Benchmark category**: `build-dependency`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `bazel_query_stale_edge`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `bazel query stale edge`
- **Framing**: Query reports target up-to-date while runtime loads stale .so from previous configuration transition.
- **Discoveries / design insights**:
  - configuration split not invalidated on flag change
  - aspect output cached across incompatible transitions
  - runfiles manifest omits rebuilt data dep
- **Frontier failure modes**:
  - config transition cache
  - aspect stale output
  - runfiles manifest drift
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `build-management`

### 1. Incremental build shadow artifacts
- **id**: `incremental-build-shadow-artifacts`
- **Status**: `bank-ready`
- **Benchmark category**: `build-management`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `incremental_shadow_artifacts`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `incremental shadow artifacts`
- **Framing**: Clean build passes but incremental rebuild serves stale object files after header rename.
- **Discoveries / design insights**:
  - depfile missing generated header edge
  - ccache key ignores compiler define change
  - ninja restat skips compile when mtime alone changes
- **Frontier failure modes**:
  - depfile missing edge
  - ccache key omission
  - restat false negative
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. CI matrix cache poisoning
- **id**: `ci-matrix-cache-poisoning`
- **Status**: `bank-ready`
- **Benchmark category**: `build-management`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `ci_matrix_cache_poison`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `CI matrix cache poison`
- **Framing**: Main branch green but feature branch inherits poisoned cache from orthogonal matrix leg.
- **Discoveries / design insights**:
  - cache key omits compiler major version
  - restore-key fallback pulls wrong OS leg
  - artifact upload includes build tree secrets path
- **Frontier failure modes**:
  - cache key collision
  - restore-key fallback
  - cross-leg artifact bleed
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Pipeline stage ordering trap
- **id**: `pipeline-stage-ordering-trap`
- **Status**: `bank-ready`
- **Benchmark category**: `build-management`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `pipeline_stage_ordering`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `pipeline stage ordering`
- **Framing**: Deploy succeeds while integration tests ran against previous artifact generation.
- **Discoveries / design insights**:
  - needs edge not enforced on manual rerun
  - artifact promotion races with tag push
  - downstream job consumes floating latest tag
- **Frontier failure modes**:
  - needs edge bypass
  - promotion race
  - floating tag consumption
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Distributed compile cache invalidation
- **id**: `distributed-compile-cache-invalidation`
- **Status**: `bank-ready`
- **Benchmark category**: `build-management`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `dist_compile_cache_invalidation`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `dist compile cache invalidation`
- **Framing**: Remote cache hits return objects built with wrong macro set after header-only change.
- **Discoveries / design insights**:
  - content hash excludes preprocessor defines
  - remote executor platform tag too coarse
  - local fallback uploads poisoned entry
- **Frontier failure modes**:
  - define omission in hash
  - platform tag coarse
  - poisoned remote upload
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Release artifact provenance gap
- **id**: `release-artifact-provenance-gap`
- **Status**: `bank-ready`
- **Benchmark category**: `build-management`
- **Portal category**: `build-and-dependency-management`
- **Architecture family**: `release_provenance_gap`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `release provenance gap`
- **Framing**: Signed release verifies but provenance attestation missing witness for one build step.
- **Discoveries / design insights**:
  - in-toto link predicate type hashed wrong
  - rekor index not checked against bundle
  - timestamp authority not cross-signed
- **Frontier failure modes**:
  - predicate hash mismatch
  - rekor index skip
  - timestamp chain gap
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `challenging-games`

### 1. Move budget Sokoban variant ladder
- **id**: `move-budget-sokoban-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `challenging-games`
- **Portal category**: `games`
- **Architecture family**: `move_budget_sokoban_ladder`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `move budget sokoban ladder`
- **Framing**: Solver must complete puzzle family under strict move budget across variant ladder of rule tweaks.
- **Discoveries / design insights**:
  - push priority interacts with ice tiles differently per arm
  - undo stack depth limited on one variant
  - goal detection differs corner vs edge goals
- **Frontier failure modes**:
  - push priority misread
  - undo depth miscount
  - goal predicate variant
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Procedural level seed replay
- **id**: `procedural-level-seed-replay`
- **Status**: `bank-ready`
- **Benchmark category**: `challenging-games`
- **Portal category**: `games`
- **Architecture family**: `procedural_level_replay`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `procedural level replay`
- **Framing**: Generated levels diverge from reference when seed replay omits one initialization phase.
- **Discoveries / design insights**:
  - RNG stream split per subsystem order-sensitive
  - biome table cached across hot reload
  - entity spawn queue processed before terrain finalize
- **Frontier failure modes**:
  - RNG stream split error
  - biome cache stale
  - spawn order inversion
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. AI search transposition table bug
- **id**: `ai-search-transposition-table-bug`
- **Status**: `bank-ready`
- **Benchmark category**: `challenging-games`
- **Portal category**: `games`
- **Architecture family**: `transposition_table_bug`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `transposition table bug`
- **Framing**: Engine mis-evaluates position after transposition store retrieves wrong bound type.
- **Discoveries / design insights**:
  - Zobrist key collision on pawn structure
  - bound type not updated on deeper search
  - table entry generation stale after null move
- **Frontier failure modes**:
  - Zobrist collision
  - bound type stale
  - generation counter miss
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Game logic invariant model check
- **id**: `game-logic-invariant-model-check`
- **Status**: `bank-ready`
- **Benchmark category**: `challenging-games`
- **Portal category**: `games`
- **Architecture family**: `game_logic_model_check`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `game logic model check`
- **Framing**: Prove turn-based rules cannot reach illegal state under documented action set.
- **Discoveries / design insights**:
  - simultaneous resolution order affects legality
  - pass action skipped in compound turn
  - undo restores wrong phase counter
- **Frontier failure modes**:
  - resolution order gap
  - phase counter drift
  - undo state incomplete
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Input remap variant ladder
- **id**: `input-remap-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `challenging-games`
- **Portal category**: `games`
- **Architecture family**: `input_remap_variant_ladder`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `input remap variant ladder`
- **Framing**: Control remap must survive ladder of deadzone, repeat rate, and chord bindings.
- **Discoveries / design insights**:
  - chord timeout differs gamepad vs keyboard
  - analog deadzone applied before axis merge
  - focus loss drops buffered edge events
- **Frontier failure modes**:
  - chord timeout drift
  - deadzone order bug
  - focus buffer loss
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `cryptography`

### 1. AEAD nonce reuse recovery
- **id**: `aead-nonce-reuse-recovery`
- **Status**: `bank-ready`
- **Benchmark category**: `cryptography`
- **Portal category**: `security`
- **Architecture family**: `aead_nonce_reuse_recovery`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `AEAD nonce reuse recovery`
- **Framing**: Decryptor reports auth failure intermittently when nonce counter rewinds after crash.
- **Discoveries / design insights**:
  - persistent counter not fsynced before ack
  - backup restore replays old counter window
  - parallel writers share counter file without lock
- **Frontier failure modes**:
  - counter rewind
  - fsync ordering
  - parallel counter race
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Threshold signature shard mismatch
- **id**: `threshold-signature-shard-mismatch`
- **Status**: `bank-ready`
- **Benchmark category**: `cryptography`
- **Portal category**: `security`
- **Architecture family**: `threshold_sig_shard_mismatch`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `threshold sig shard mismatch`
- **Framing**: Sharded recovery reconstructs key locally but verify fails under rotated metadata.
- **Discoveries / design insights**:
  - shard index permutation not authenticated
  - threshold includes retired custodian
  - HKDF info string differs between arms
- **Frontier failure modes**:
  - shard index swap
  - retired custodian count
  - HKDF info mismatch
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. TLS extension order inference
- **id**: `tls-extension-order-inference`
- **Status**: `bank-ready`
- **Benchmark category**: `cryptography`
- **Portal category**: `security`
- **Architecture family**: `tls_extension_order_inference`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `reverse_engineering`
  - `instruction_framing`: `behavioral-target`
  - `hardness_source`: `semantic inference`
- **Topology**: `TLS extension order inference`
- **Framing**: Infer required extension ordering from traces to build compatible terminator.
- **Discoveries / design insights**:
  - key_share group preference differs by arm
  - supported_versions encoding ambiguous
  - post-handshake auth optional path
- **Frontier failure modes**:
  - extension order drift
  - version encoding ambiguity
  - post-handshake path
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Crypto agility variant ladder
- **id**: `crypto-agility-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `cryptography`
- **Portal category**: `security`
- **Architecture family**: `crypto_agility_ladder`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `crypto agility ladder`
- **Framing**: Verify signatures across algorithm agility ladder without unsafe fallback ordering.
- **Discoveries / design insights**:
  - RSA-PSS salt length differs by provider
  - EdDSA context string optional per arm
  - hybrid KEM combines classical and PQC wrong
- **Frontier failure modes**:
  - PSS salt mismatch
  - EdDSA context omission
  - hybrid KEM composition
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Encrypted backup header parse
- **id**: `encrypted-backup-header-parse`
- **Status**: `bank-ready`
- **Benchmark category**: `cryptography`
- **Portal category**: `security`
- **Architecture family**: `encrypted_backup_header`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `encrypted backup header`
- **Framing**: Backup decrypts first chunk but manifest hash mismatches due to header endianness.
- **Discoveries / design insights**:
  - salt iteration count conflicting widths
  - AEAD AAD excludes version field
  - compression flag affects MAC input
- **Frontier failure modes**:
  - endianness drift
  - AAD scope error
  - compression MAC scope
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Passkey challenge replay
- **id**: `passkey-challenge-replay`
- **Status**: `bank-ready`
- **Benchmark category**: `cryptography`
- **Portal category**: `security`
- **Architecture family**: `passkey_challenge_replay`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `passkey challenge replay`
- **Framing**: WebAuthn ceremony verifies once but accepts replayed challenge on concurrent session.
- **Discoveries / design insights**:
  - challenge store not bound to origin
  - signCount not checked on backup path
  - UV flag optional on fallback authenticator
- **Frontier failure modes**:
  - origin binding miss
  - signCount skip
  - UV optional bypass
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `data-processing`

### 1. Stream window aggregate drift
- **id**: `stream-window-aggregate-drift`
- **Status**: `bank-ready`
- **Benchmark category**: `data-processing`
- **Portal category**: `data-processing`
- **Architecture family**: `stream_window_aggregate_drift`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `stream window aggregate drift`
- **Framing**: Rolling aggregates match batch on sample data but drift on production event order.
- **Discoveries / design insights**:
  - watermark lateness treated as drop not side output
  - session gap closure uses processing time
  - retraction not applied to incremental state
- **Frontier failure modes**:
  - watermark semantics
  - processing time gap
  - retraction omission
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Schema inference variant ladder
- **id**: `schema-inference-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `data-processing`
- **Portal category**: `data-processing`
- **Architecture family**: `schema_inference_ladder`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `schema inference ladder`
- **Framing**: Inferred schema must survive variant ladder of malformed and nested edge cases.
- **Discoveries / design insights**:
  - union widening order changes nullability
  - numeric string coercion differs arms
  - array tuple vs list ambiguity
- **Frontier failure modes**:
  - union widen order
  - coercion path drift
  - array tuple ambiguity
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. PII redaction variant ladder
- **id**: `pii-redaction-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `data-processing`
- **Portal category**: `data-processing`
- **Architecture family**: `pii_redaction_ladder`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `PII redaction ladder`
- **Framing**: Redaction must not leak substrings under regex collision and encoding ladder.
- **Discoveries / design insights**:
  - overlapping patterns hide partial secrets
  - structured field redaction breaks JSON
  - hash salt must stay stable for correlation
- **Frontier failure modes**:
  - regex overlap leak
  - JSON validity break
  - salt instability
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Data lineage invariant proof
- **id**: `data-lineage-invariant-proof`
- **Status**: `bank-ready`
- **Benchmark category**: `data-processing`
- **Portal category**: `data-processing`
- **Architecture family**: `data_lineage_invariant_proof`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `data lineage invariant proof`
- **Framing**: Prove pipeline cannot emit row without required provenance fields under rewrite rules.
- **Discoveries / design insights**:
  - view definition hides intermediate filter
  - late arriving dimension changes grain
  - surrogate key reused across reload
- **Frontier failure modes**:
  - view grain hide
  - late dimension skew
  - surrogate key reuse
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Regex extraction trace inference
- **id**: `regex-extraction-trace-inference`
- **Status**: `bank-ready`
- **Benchmark category**: `data-processing`
- **Portal category**: `data-processing`
- **Architecture family**: `regex_extraction_inference`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `reverse_engineering`
  - `instruction_framing`: `behavioral-target`
  - `hardness_source`: `semantic inference`
- **Topology**: `regex extraction inference`
- **Framing**: Infer extraction rules from sample traces; must generalize to held-out arms.
- **Discoveries / design insights**:
  - capture group optional in subset of arms
  - multiline mode changes anchor behavior
  - unicode property escapes differ engine
- **Frontier failure modes**:
  - capture optional drift
  - multiline anchor
  - unicode property gap
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Metamorphic ETL checksum chain
- **id**: `metamorphic-etl-checksum-chain`
- **Status**: `bank-ready`
- **Benchmark category**: `data-processing`
- **Portal category**: `data-processing`
- **Architecture family**: `metamorphic_etl_checksum`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `metamorphic ETL checksum`
- **Framing**: ETL checksum chain breaks when intermediate sort order differs from documented stable sort.
- **Discoveries / design insights**:
  - tie-break key omitted from hash input
  - null ordering differs arms
  - parallel merge changes equal-key order
- **Frontier failure modes**:
  - tie-break omission
  - null order drift
  - parallel merge order
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `data-scripting`

### 1. Pipeline DAG checkpoint resume
- **id**: `pipeline-dag-checkpoint-resume`
- **Status**: `bank-ready`
- **Benchmark category**: `data-scripting`
- **Portal category**: `data-processing`
- **Architecture family**: `pipeline_dag_checkpoint`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `pipeline DAG checkpoint`
- **Framing**: Orchestrator resumes mid-DAG but replays completed stage causing duplicate side effects.
- **Discoveries / design insights**:
  - checkpoint stores stage name not attempt id
  - idempotent token not scoped to partition
  - dynamic fan-out not captured in checkpoint
- **Frontier failure modes**:
  - checkpoint identity weak
  - idempotency scope
  - fan-out omission
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Shell task env inheritance trap
- **id**: `shell-task-env-inheritance-trap`
- **Status**: `bank-ready`
- **Benchmark category**: `data-scripting`
- **Portal category**: `data-processing`
- **Architecture family**: `shell_env_inheritance`
- **Implementation language**: `bash`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `shell env inheritance`
- **Framing**: Script succeeds interactively but fails in CI due to inherited env changing precedence.
- **Discoveries / design insights**:
  - exported function shadows POSIX builtin
  - BASH_ENV mutates non-interactive path
  - set -e masked by subshell ERR trap
- **Frontier failure modes**:
  - function shadow builtin
  - BASH_ENV side effect
  - ERR trap scope
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Notebook cell reorder provenance
- **id**: `notebook-cell-reorder-provenance`
- **Status**: `bank-ready`
- **Benchmark category**: `data-scripting`
- **Portal category**: `data-processing`
- **Architecture family**: `notebook_cell_provenance`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `notebook cell provenance`
- **Framing**: Reordered notebook cells produce same output but wrong lineage metadata for audit.
- **Discoveries / design insights**:
  - cell id not stable across save
  - execution count reused after kernel restart
  - widget state serialized out of order
- **Frontier failure modes**:
  - cell id instability
  - execution count reuse
  - widget serialize order
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Cron overlap guard failure
- **id**: `cron-overlap-guard-failure`
- **Status**: `bank-ready`
- **Benchmark category**: `data-scripting`
- **Portal category**: `data-processing`
- **Architecture family**: `cron_overlap_guard`
- **Implementation language**: `bash`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `cron overlap guard`
- **Framing**: Scheduled job overlaps itself causing double write despite flock guard.
- **Discoveries / design insights**:
  - flock released before async child completes
  - timezone DST shifts schedule twice
  - missed run policy catches up burst
- **Frontier failure modes**:
  - flock lifetime short
  - DST double fire
  - catch-up burst
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Data contract validator builder
- **id**: `data-contract-validator-builder`
- **Status**: `bank-ready`
- **Benchmark category**: `data-scripting`
- **Portal category**: `data-processing`
- **Architecture family**: `data_contract_validator_build`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `constrained_build`
  - `instruction_framing`: `design-brief`
  - `hardness_source`: `design search`
- **Topology**: `data contract validator build`
- **Framing**: Build validator enforcing evolving JSON contract under version ladder without network.
- **Discoveries / design insights**:
  - optional field default differs version arms
  - enum extension must reject unknown on old consumer
  - numeric bound uses inclusive vs exclusive edge
- **Frontier failure modes**:
  - default version drift
  - enum extension rule
  - bound inclusivity
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `debugging`

### 1. Journal replay generation skew
- **id**: `journal-replay-generation-skew`
- **Status**: `bank-ready`
- **Benchmark category**: `debugging`
- **Portal category**: `debugging`
- **Architecture family**: `journal_replay_generation_skew`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `journal replay generation skew`
- **Framing**: After partial rollback, lanes disagree on closure counters despite aggregate looking fine.
- **Discoveries / design insights**:
  - stale checkpoint ancestry revives retired generation
  - combine invalidates before rollback completes
  - echo lane reads pre-rollback facet material
- **Frontier failure modes**:
  - generation skew
  - combine order bug
  - echo lane stale read
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Scheduler persistence reconciliation
- **id**: `scheduler-persistence-reconciliation`
- **Status**: `bank-ready`
- **Benchmark category**: `debugging`
- **Portal category**: `debugging`
- **Architecture family**: `scheduler_persistence_reconciliation`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `scheduler persistence reconciliation`
- **Framing**: Tasks survive restart but runqueue order violates documented fairness after replay.
- **Discoveries / design insights**:
  - WAL replay skips cancelled generation
  - priority inversion on persistence fsync path
  - lease renewal double-applies on recovery
- **Frontier failure modes**:
  - WAL skip cancelled
  - priority inversion
  - lease double apply
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Core dump stack inference
- **id**: `core-dump-stack-inference`
- **Status**: `bank-ready`
- **Benchmark category**: `debugging`
- **Portal category**: `debugging`
- **Architecture family**: `core_dump_stack_inference`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `reverse_engineering`
  - `instruction_framing`: `behavioral-target`
  - `hardness_source`: `semantic inference`
- **Topology**: `core dump stack inference`
- **Framing**: Infer corruption site from multi-thread cores with divergent unwinding across libc versions.
- **Discoveries / design insights**:
  - unwinder stops at signal trampoline differently
  - DWARF CFI missing for hand-written asm
  - alt signal stack confuses frame chain
- **Frontier failure modes**:
  - unwind trampoline gap
  - CFI missing
  - alt stack confusion
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Distributed trace context break
- **id**: `distributed-trace-context-break`
- **Status**: `bank-ready`
- **Benchmark category**: `debugging`
- **Portal category**: `debugging`
- **Architecture family**: `trace_context_propagation_break`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `trace context propagation break`
- **Framing**: Spans disconnected across services though requests succeed end-to-end.
- **Discoveries / design insights**:
  - baggage header stripped at gateway
  - trace id regenerated on async boundary
  - parent span id reused after pool recycle
- **Frontier failure modes**:
  - baggage strip
  - trace id regen
  - span id reuse
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Heisenbug variant ladder
- **id**: `heisenbug-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `debugging`
- **Portal category**: `debugging`
- **Architecture family**: `heisenbug_variant_ladder`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `heisenbug variant ladder`
- **Framing**: Fix must survive ASAN on/off, jemalloc/glibc, single vs multi thread without masking.
- **Discoveries / design insights**:
  - sanitizer changes timing hiding race
  - allocator padding alters layout
  - signal mask differs under harness
- **Frontier failure modes**:
  - timing mask
  - layout drift
  - signal mask diff
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Happens-before model check
- **id**: `happens-before-model-check`
- **Status**: `bank-ready`
- **Benchmark category**: `debugging`
- **Portal category**: `debugging`
- **Architecture family**: `happens_before_model_check`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `happens before model check`
- **Framing**: Verify queue API linearizability under documented memory ordering for custom runtime.
- **Discoveries / design insights**:
  - relaxed atomics create cycle not in logs
  - fence placement differs ARM vs x86
  - publication safety missing on lazy init
- **Frontier failure modes**:
  - relaxed atomic cycle
  - fence portability
  - lazy init publish
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `large-codebase`

### 1. Monorepo import cycle repair
- **id**: `monorepo-import-cycle-repair`
- **Status**: `bank-ready`
- **Benchmark category**: `large-codebase`
- **Portal category**: `software-engineering`
- **Architecture family**: `monorepo_import_cycle_repair`
- **Implementation language**: `python`
- **Subcategories**: `['long_context']`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `monorepo import cycle repair`
- **Framing**: Large Python monorepo fails typecheck only on full graph due to lazy import cycle.
- **Discoveries / design insights**:
  - TYPE_CHECKING guard hides runtime cycle
  - namespace package shadowed by local stub
  - editable install resolves wrong package root
- **Frontier failure modes**:
  - TYPE_CHECKING mask
  - namespace shadow
  - editable path wrong
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Legacy bytecode VM inference
- **id**: `legacy-bytecode-vm-inference`
- **Status**: `bank-ready`
- **Benchmark category**: `large-codebase`
- **Portal category**: `software-engineering`
- **Architecture family**: `legacy_bytecode_vm_inference`
- **Implementation language**: `java`
- **Subcategories**: `['long_context']`
- **task_shape**:
  - `type`: `reverse_engineering`
  - `instruction_framing`: `behavioral-target`
  - `hardness_source`: `semantic inference`
- **Topology**: `legacy bytecode VM inference`
- **Framing**: Infer opcode semantics from traces; implement decoder passing metamorphic harness.
- **Discoveries / design insights**:
  - wide instruction overlaps narrow prefix
  - stack depth implicit on call pattern
  - endian switch mid-image on arm ladder
- **Frontier failure modes**:
  - opcode prefix overlap
  - stack depth infer
  - endian arm switch
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Cross-module float policy drift
- **id**: `cross-module-float-policy-drift`
- **Status**: `bank-ready`
- **Benchmark category**: `large-codebase`
- **Portal category**: `software-engineering`
- **Architecture family**: `cross_module_float_policy`
- **Implementation language**: `python`
- **Subcategories**: `['long_context']`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `cross module float policy`
- **Framing**: Aggregated metrics disagree across modules though each passes local unit tests.
- **Discoveries / design insights**:
  - Kahan sum only on master path
  - decimal context differs import order
  - json serializer rounding per module
- **Frontier failure modes**:
  - Kahan path split
  - decimal context order
  - json round per module
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Plugin registry authority split
- **id**: `plugin-registry-authority-split`
- **Status**: `bank-ready`
- **Benchmark category**: `large-codebase`
- **Portal category**: `software-engineering`
- **Architecture family**: `plugin_registry_authority_split`
- **Implementation language**: `java`
- **Subcategories**: `['long_context']`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `plugin registry authority split`
- **Framing**: Plugin load succeeds but sandbox escape via stale capability grant after hot reload.
- **Discoveries / design insights**:
  - capability token not revoked on unload
  - registry index reused for new plugin id
  - signature check skipped on cached descriptor
- **Frontier failure modes**:
  - capability revoke miss
  - index reuse
  - signature cache skip
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Query plan cost model optimize
- **id**: `query-plan-cost-model-optimize`
- **Status**: `bank-ready`
- **Benchmark category**: `large-codebase`
- **Portal category**: `software-engineering`
- **Architecture family**: `query_plan_cost_model_optimize`
- **Implementation language**: `cpp`
- **Subcategories**: `['long_context']`
- **task_shape**:
  - `type`: `optimization_under_constraints`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `constrained optimization`
- **Topology**: `query plan cost model optimize`
- **Framing**: Optimize join order under cardinality cap using public cost formulas only.
- **Discoveries / design insights**:
  - correlated subquery cardinality underestimated
  - histogram bucket boundary inclusive wrong
  - parallel worker skew not in cost model
- **Frontier failure modes**:
  - cardinality underestimate
  - histogram boundary
  - skew omission
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Service mesh config precedence
- **id**: `service-mesh-config-precedence`
- **Status**: `bank-ready`
- **Benchmark category**: `large-codebase`
- **Portal category**: `software-engineering`
- **Architecture family**: `service_mesh_config_precedence`
- **Implementation language**: `go`
- **Subcategories**: `['long_context']`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `service mesh config precedence`
- **Framing**: Effective routing policy wrong after layered CRD, annotation, and file overrides.
- **Discoveries / design insights**:
  - precedence table differs control plane vs data plane
  - namespace-scoped policy not invalidated on move
  - default upstream timeout inherited wrong
- **Frontier failure modes**:
  - precedence table split
  - namespace move stale
  - timeout inherit wrong
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `machine-learning`

### 1. Checkpoint resume optimizer state
- **id**: `checkpoint-resume-optimizer-state`
- **Status**: `bank-ready`
- **Benchmark category**: `machine-learning`
- **Portal category**: `machine-learning`
- **Architecture family**: `checkpoint_optimizer_resume`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `checkpoint optimizer resume`
- **Framing**: Training resumes but optimizer moments wrong causing loss spike though weights match.
- **Discoveries / design insights**:
  - Adam bias correction uses step from wrong run
  - fp16 master weights not restored
  - learning rate schedule tied to wall clock
- **Frontier failure modes**:
  - bias correction step
  - fp16 master miss
  - LR wall clock
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Sampler shard divergence repair
- **id**: `sampler-shard-divergence-repair`
- **Status**: `bank-ready`
- **Benchmark category**: `machine-learning`
- **Portal category**: `machine-learning`
- **Architecture family**: `sampler_shard_divergence`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `sampler shard divergence`
- **Framing**: Distributed sampler assigns overlapping indices after worker failure recovery.
- **Discoveries / design insights**:
  - shard offset not advanced on resume
  - drop_last differs eval vs train path
  - seed split includes rank in wrong position
- **Frontier failure modes**:
  - shard offset stall
  - drop_last mismatch
  - seed split error
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. OOD detection variant ladder
- **id**: `ood-detection-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `machine-learning`
- **Portal category**: `machine-learning`
- **Architecture family**: `ood_detection_ladder`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `OOD detection ladder`
- **Framing**: Detector must flag held-out arms without threshold tuning on visible set only.
- **Discoveries / design insights**:
  - feature scaling fit on full batch leaks
  - temperature scaling uses val in train
  - ensemble disagreement ignored on borderline
- **Frontier failure modes**:
  - scaling leak
  - temperature val leak
  - ensemble ignore
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Mixed precision replay ladder
- **id**: `mixed-precision-replay-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `machine-learning`
- **Portal category**: `machine-learning`
- **Architecture family**: `mixed_precision_replay_ladder`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `mixed precision replay ladder`
- **Framing**: Forward pass matches fp32 on small batch but diverges on large with same seed.
- **Discoveries / design insights**:
  - loss scaler update before unscale
  - TF32 enabled only rank zero
  - allreduce order non-deterministic
- **Frontier failure modes**:
  - scaler order
  - TF32 rank split
  - allreduce order
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Prompt injection eval ladder
- **id**: `prompt-injection-eval-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `machine-learning`
- **Portal category**: `machine-learning`
- **Architecture family**: `prompt_injection_eval_ladder`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `prompt injection eval ladder`
- **Framing**: Eval harness must resist injection strings in tool outputs without blocklist hacks.
- **Discoveries / design insights**:
  - system prompt concatenation order matters
  - tool result delimiter escapable
  - jailbreak via nested markup in citation
- **Frontier failure modes**:
  - concat order inject
  - delimiter escape
  - nested markup
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Calibration isotonic monotonic proof
- **id**: `calibration-isotonic-monotonic-proof`
- **Status**: `bank-ready`
- **Benchmark category**: `machine-learning`
- **Portal category**: `machine-learning`
- **Architecture family**: `isotonic_calibration_proof`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `isotonic calibration proof`
- **Framing**: Prove isotonic mapping preserves monotonicity under documented tie-breaking.
- **Discoveries / design insights**:
  - tie pool merges wrong adjacent blocks
  - out-of-sample extrapolation flat wrong
  - weight normalization differs arms
- **Frontier failure modes**:
  - tie pool merge
  - extrapolation flat
  - weight norm drift
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `scientific-computing-analysis`

### 1. FFT resume corruption
- **id**: `fft-resume-corruption`
- **Status**: `bank-ready`
- **Benchmark category**: `scientific-computing-analysis`
- **Portal category**: `scientific-computing`
- **Architecture family**: `fft_resume_corruption`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `FFT resume corruption`
- **Framing**: Spectral pipeline resumes mid-transform with wrong normalization constant.
- **Discoveries / design insights**:
  - wisdom file tied to old grid topology
  - real-to-complex plan reused incorrectly
  - padding factor ignored in plan search
- **Frontier failure modes**:
  - wisdom stale
  - plan reuse wrong
  - padding ignore
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Cross-runtime float policy drift
- **id**: `cross-runtime-float-policy-drift`
- **Status**: `bank-ready`
- **Benchmark category**: `scientific-computing-analysis`
- **Portal category**: `scientific-computing`
- **Architecture family**: `cross_runtime_float_drift`
- **Implementation language**: `fortran`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `cross runtime float drift`
- **Framing**: Simulation binary agrees on one OS but diverges on second with same inputs.
- **Discoveries / design insights**:
  - FMA availability differs
  - denormal flush changes branch
  - reduction tree depth changes ULP
- **Frontier failure modes**:
  - FMA availability
  - denormal flush
  - reduction tree
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Unit conversion pipeline drift
- **id**: `unit-conversion-pipeline-drift`
- **Status**: `bank-ready`
- **Benchmark category**: `scientific-computing-analysis`
- **Portal category**: `scientific-computing`
- **Architecture family**: `unit_conversion_drift`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `unit conversion drift`
- **Framing**: Derived quantities disagree after unit string refactor in analysis notebook.
- **Discoveries / design insights**:
  - offset temperature handled inconsistently
  - compound unit drops dimension
  - locale decimal comma breaks parser
- **Frontier failure modes**:
  - offset temp unit
  - dimension drop
  - locale comma
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Monte Carlo stratified overlap
- **id**: `monte-carlo-stratified-overlap`
- **Status**: `bank-ready`
- **Benchmark category**: `scientific-computing-analysis`
- **Portal category**: `scientific-computing`
- **Architecture family**: `monte_carlo_stratified`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `monte carlo stratified`
- **Framing**: Coverage drops below nominal despite correct formula on visible strata.
- **Discoveries / design insights**:
  - strata boundaries overlap after transform
  - antithetic pairs correlated
  - RNG split per stratum reuses stream
- **Frontier failure modes**:
  - strata overlap
  - antithetic correlation
  - RNG reuse
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Symplectic integrator energy drift
- **id**: `symplectic-integrator-energy-drift`
- **Status**: `bank-ready`
- **Benchmark category**: `scientific-computing-analysis`
- **Portal category**: `scientific-computing`
- **Architecture family**: `symplectic_energy_drift`
- **Implementation language**: `fortran`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `symplectic energy drift`
- **Framing**: Energy drifts past threshold on long orbit though short run acceptable.
- **Discoveries / design insights**:
  - splitting order odd even differs
  - potential gradient uses stale coords
  - warm start reuses wrong momentum phase
- **Frontier failure modes**:
  - splitting order
  - stale gradient
  - momentum phase
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Interval arithmetic proof contract
- **id**: `interval-arithmetic-proof-contract`
- **Status**: `bank-ready`
- **Benchmark category**: `scientific-computing-analysis`
- **Portal category**: `scientific-computing`
- **Architecture family**: `interval_arithmetic_proof`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `interval arithmetic proof`
- **Framing**: Prove enclosure holds for deployed expression graph on all test intervals.
- **Discoveries / design insights**:
  - dependency problem overestimation uncaught
  - monotonicity not exploited
  - rounding mode mix invalidates step
- **Frontier failure modes**:
  - dependency blowup
  - monotonicity miss
  - rounding mix
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `security`

### 1. Revocation cache authority split
- **id**: `revocation-cache-authority-split`
- **Status**: `bank-ready`
- **Benchmark category**: `security`
- **Portal category**: `security`
- **Architecture family**: `revocation_cache_split`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `revocation cache split`
- **Framing**: Token validation accepts revoked credentials when cache partitions disagree.
- **Discoveries / design insights**:
  - positive TTL exceeds revocation propagation
  - negative cache not invalidated on rotation
  - replica serves stale CRL fragment
- **Frontier failure modes**:
  - TTL propagation gap
  - negative cache stale
  - CRL fragment stale
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. MAC policy boolean precedence
- **id**: `mac-policy-boolean-precedence`
- **Status**: `bank-ready`
- **Benchmark category**: `security`
- **Portal category**: `security`
- **Architecture family**: `mac_boolean_precedence`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `MAC boolean precedence`
- **Framing**: Confined service gains capability after boolean toggle order differs from docs.
- **Discoveries / design insights**:
  - conditional boolean stack not atomic
  - dontaudit hides first failing allow
  - module version changes boolean default
- **Frontier failure modes**:
  - boolean stack order
  - dontaudit mask
  - default version drift
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Confused deputy RPC guard
- **id**: `confused-deputy-rpc-guard`
- **Status**: `bank-ready`
- **Benchmark category**: `security`
- **Portal category**: `security`
- **Architecture family**: `confused_deputy_rpc_guard`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `constrained_build`
  - `instruction_framing`: `design-brief`
  - `hardness_source`: `design search`
- **Topology**: `confused deputy RPC guard`
- **Framing**: Service A invokes privileged B method using delegated client credentials.
- **Discoveries / design insights**:
  - capability not scoped to method
  - request metadata trusted from client
  - async callback reuses stale delegation
- **Frontier failure modes**:
  - capability scope
  - metadata trust
  - stale delegation
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. WAF bypass variant ladder
- **id**: `waf-bypass-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `security`
- **Portal category**: `security`
- **Architecture family**: `waf_bypass_ladder`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `WAF bypass ladder`
- **Framing**: Harden normalization so encoding ladder cannot reach same backend sink.
- **Discoveries / design insights**:
  - double decode differs by content type
  - chunked reassembly boundary
  - path normalization proxy vs app
- **Frontier failure modes**:
  - double decode
  - chunk boundary
  - path norm split
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Supply chain sig chain gap
- **id**: `supply-chain-sig-chain-gap`
- **Status**: `bank-ready`
- **Benchmark category**: `security`
- **Portal category**: `security`
- **Architecture family**: `supply_chain_sig_gap`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `supply chain sig gap`
- **Framing**: Package verifies with publisher sig but provenance chain missing witness.
- **Discoveries / design insights**:
  - in-toto link hashed wrong predicate
  - rekor index unchecked
  - timestamp authority not cross-signed
- **Frontier failure modes**:
  - predicate hash
  - rekor skip
  - timestamp gap
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Privilege graph acyclic proof
- **id**: `privilege-graph-acyclic-proof`
- **Status**: `bank-ready`
- **Benchmark category**: `security`
- **Portal category**: `security`
- **Architecture family**: `privilege_graph_proof`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `privilege graph proof`
- **Framing**: Verify delegation graph acyclic under dynamic grant and revoke script.
- **Discoveries / design insights**:
  - temporary grants expire out of order
  - group inheritance cyclic
  - revoke not propagated to derived tokens
- **Frontier failure modes**:
  - grant expiry order
  - inheritance cycle
  - revoke propagation
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `software-engineering`

### 1. Typestate protocol proof
- **id**: `typestate-protocol-proof`
- **Status**: `bank-ready`
- **Benchmark category**: `software-engineering`
- **Portal category**: `software-engineering`
- **Architecture family**: `typestate_protocol_proof`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `typestate protocol proof`
- **Framing**: Prove API usage state machine cannot reach illegal state at compile-checked subset.
- **Discoveries / design insights**:
  - transition table incomplete on error path
  - refinement type erasure loses phase
  - macro-generated impl skips guard
- **Frontier failure modes**:
  - error path gap
  - erasure loss
  - macro guard skip
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Async fault injection ladder
- **id**: `async-fault-injection-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `software-engineering`
- **Portal category**: `software-engineering`
- **Architecture family**: `async_fault_injection_ladder`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `async fault injection ladder`
- **Framing**: Runtime must survive injected fault ladder without deadlock or lost cancellation.
- **Discoveries / design insights**:
  - cancellation not propagated to IO driver
  - select bias drops wakeup
  - timeout race with drop order
- **Frontier failure modes**:
  - cancel propagation
  - select bias
  - timeout drop race
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Minimal HTTP router under size cap
- **id**: `minimal-http-router-under-size-cap`
- **Status**: `bank-ready`
- **Benchmark category**: `software-engineering`
- **Portal category**: `software-engineering`
- **Architecture family**: `minimal_http_router_cap`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `constrained_build`
  - `instruction_framing`: `design-brief`
  - `hardness_source`: `design search`
- **Topology**: `minimal HTTP router cap`
- **Framing**: Implement router under byte budget serving method/path matrix and error codes.
- **Discoveries / design insights**:
  - trie vs table tradeoff for prefix routes
  - percent decode must not allocate per segment
  - keep-alive parsing shares buffer with body
- **Frontier failure modes**:
  - route table tradeoff
  - decode alloc
  - buffer sharing
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Wire protocol from pcap inference
- **id**: `wire-protocol-from-pcap-inference`
- **Status**: `bank-ready`
- **Benchmark category**: `software-engineering`
- **Portal category**: `software-engineering`
- **Architecture family**: `wire_protocol_pcap_inference`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `reverse_engineering`
  - `instruction_framing`: `behavioral-target`
  - `hardness_source`: `semantic inference`
- **Topology**: `wire protocol pcap inference`
- **Framing**: Infer framing from pcaps; produce parser passing metamorphic replay harness.
- **Discoveries / design insights**:
  - length-prefix vs delimiter ambiguous
  - optional fields encoded per version
  - checksum algorithm unlabeled
- **Frontier failure modes**:
  - framing ambiguity
  - optional encoding
  - checksum unknown
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Codec framing variant ladder
- **id**: `codec-framing-variant-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `software-engineering`
- **Portal category**: `software-engineering`
- **Architecture family**: `codec_framing_ladder`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `codec framing ladder`
- **Framing**: Codec must decode variant ladder including split packets and partial headers.
- **Discoveries / design insights**:
  - reassembly buffer retains tail
  - MAC verified before length field
  - nested TLV MAC covers wrong range
- **Frontier failure modes**:
  - reassembly tail
  - MAC before length
  - TLV MAC range
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Allocator pool size optimize
- **id**: `allocator-pool-size-optimize`
- **Status**: `bank-ready`
- **Benchmark category**: `software-engineering`
- **Portal category**: `software-engineering`
- **Architecture family**: `allocator_pool_optimize`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `optimization_under_constraints`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `constrained optimization`
- **Topology**: `allocator pool optimize`
- **Framing**: Optimize pool allocator under memory cap for fixed allocation size distribution.
- **Discoveries / design insights**:
  - alignment padding vs cache line tradeoff
  - thread cache flush policy affects peak
  - madvise behavior on return to OS
- **Frontier failure modes**:
  - alignment tradeoff
  - tcache flush
  - madvise policy
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `system-configuration`

### 1. Namespace restore replay loop
- **id**: `namespace-restore-replay-loop`
- **Status**: `bank-ready`
- **Benchmark category**: `system-configuration`
- **Portal category**: `system-administration`
- **Architecture family**: `namespace_restore_replay`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `namespace restore replay`
- **Framing**: Automated namespace restore leaves stale mount entries failing health checks.
- **Discoveries / design insights**:
  - pivot_root leaves bind-mounted dev nodes
  - propagation events after consumer cache stat
  - PrivateDevices interacts with mknod cache
- **Frontier failure modes**:
  - dev node stale
  - propagation cache
  - PrivateDevices interact
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Cgroup pressure metric desync
- **id**: `cgroup-pressure-metric-desync`
- **Status**: `bank-ready`
- **Benchmark category**: `system-configuration`
- **Portal category**: `system-administration`
- **Architecture family**: `cgroup_pressure_desync`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `cgroup pressure desync`
- **Framing**: Pressure metrics report low while workloads OOM due to accounting generation skew.
- **Discoveries / design insights**:
  - memory.pressure uses stale window
  - psi avg10 vs avg60 precedence wrong
  - hierarchy walk skips delegated subtree
- **Frontier failure modes**:
  - pressure window stale
  - psi precedence
  - hierarchy skip
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Fstab variant remount ladder
- **id**: `fstab-variant-remount-ladder`
- **Status**: `bank-ready`
- **Benchmark category**: `system-configuration`
- **Portal category**: `system-administration`
- **Architecture family**: `fstab_remount_ladder`
- **Implementation language**: `bash`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `adversarial_generalization`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `adversarial generalization`
- **Topology**: `fstab remount ladder`
- **Framing**: Mount workflow must survive ro-rw toggles and bind moves without stale consumers.
- **Discoveries / design insights**:
  - systemd mount vs fstab generator disagree
  - nofail masks ordering bugs
  - remote fs options differ per arm
- **Frontier failure modes**:
  - generator disagree
  - nofail mask
  - remote option drift
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. SELinux restorecon generation
- **id**: `selinux-restorecon-generation`
- **Status**: `bank-ready`
- **Benchmark category**: `system-configuration`
- **Portal category**: `system-administration`
- **Architecture family**: `selinux_restorecon_generation`
- **Implementation language**: `python`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `selinux restorecon generation`
- **Framing**: Relabeled tree passes check but domain transitions fail on upgraded policy gen.
- **Discoveries / design insights**:
  - restorecon uses old spec generation
  - contexts.d drop-in order differs
  - tmpfs contexts not recomputed on reload
- **Frontier failure modes**:
  - spec generation stale
  - drop-in order
  - tmpfs context
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Systemd timer persistent skew
- **id**: `systemd-timer-persistent-skew`
- **Status**: `bank-ready`
- **Benchmark category**: `system-configuration`
- **Portal category**: `system-administration`
- **Architecture family**: `systemd_timer_skew`
- **Implementation language**: `bash`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `systemd timer skew`
- **Framing**: Persistent timer fires early after DST jump overlapping maintenance window.
- **Discoveries / design insights**:
  - Persistent uses different reference clock
  - RandomizedDelaySec interacts DST
  - OnCalendar vs OnUnitActiveSec precedence
- **Frontier failure modes**:
  - clock reference
  - DST interaction
  - calendar precedence
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Mount propagation formal model
- **id**: `mount-propagation-formal-model`
- **Status**: `bank-ready`
- **Benchmark category**: `system-configuration`
- **Portal category**: `system-administration`
- **Architecture family**: `mount_propagation_formal`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `formal_reasoning`
  - `instruction_framing`: `constraint-complete`
  - `hardness_source`: `formal correctness`
- **Topology**: `mount propagation formal`
- **Framing**: Prove propagation invariants for scripted sequence using small-state model checker.
- **Discoveries / design insights**:
  - MS_SHARED PRIVATE SLAVE compose non-obviously
  - bind mount duplicates event paths
  - pivot_root resets some relationships
- **Frontier failure modes**:
  - flag composition
  - bind duplicate events
  - pivot partial reset
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---

## Benchmark category: `troubleshooting`

### 1. Overlay lowerdir stale bind
- **id**: `overlay-lowerdir-stale-bind`
- **Status**: `bank-ready`
- **Benchmark category**: `troubleshooting`
- **Portal category**: `debugging`
- **Architecture family**: `overlay_lowerdir_stale_bind`
- **Implementation language**: `rust`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `overlay lowerdir stale bind`
- **Framing**: Merged tree shows resurrected files after partial umount during rolling deploy.
- **Discoveries / design insights**:
  - whiteout not propagated to new generation
  - index off changes whiteout semantics
  - workdir cleanup races copy_up
- **Frontier failure modes**:
  - whiteout propagation
  - index semantics
  - workdir race
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 2. Device node lineage mismatch
- **id**: `device-node-lineage-mismatch`
- **Status**: `bank-ready`
- **Benchmark category**: `troubleshooting`
- **Portal category**: `debugging`
- **Architecture family**: `device_node_lineage`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `device node lineage`
- **Framing**: Services open wrong major/minor after automated device node refresh cycle.
- **Discoveries / design insights**:
  - mknod cache from pre-pivot generation
  - udev rule order differs cold vs hot
  - health probe caches stat before rule apply
- **Frontier failure modes**:
  - mknod cache stale
  - udev order
  - stat cache race
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 3. Watchdog restart boundary debug
- **id**: `watchdog-restart-boundary-debug`
- **Status**: `bank-ready`
- **Benchmark category**: `troubleshooting`
- **Portal category**: `debugging`
- **Architecture family**: `watchdog_restart_boundary`
- **Implementation language**: `go`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `watchdog restart boundary`
- **Framing**: Watchdog reports recovery while subsystem violates liveness on alternate probe.
- **Discoveries / design insights**:
  - heartbeat touched before work completes
  - dependent check disabled degraded path
  - grace period resets without clearing latch
- **Frontier failure modes**:
  - heartbeat early
  - dependent mask
  - grace latch
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 4. Health check dependency mask
- **id**: `health-check-dependency-mask`
- **Status**: `bank-ready`
- **Benchmark category**: `troubleshooting`
- **Portal category**: `debugging`
- **Architecture family**: `health_dependency_mask`
- **Implementation language**: `java`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `health dependency mask`
- **Framing**: Aggregate health green while critical dependency failing due to weighting.
- **Discoveries / design insights**:
  - weighted score hides hard fail
  - degraded not propagated parent
  - parallel probe timeout short
- **Frontier failure modes**:
  - weight hides fail
  - degraded propagation
  - probe timeout
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 5. Offline rescue chroot contract
- **id**: `offline-rescue-chroot-contract`
- **Status**: `bank-ready`
- **Benchmark category**: `troubleshooting`
- **Portal category**: `debugging`
- **Architecture family**: `offline_rescue_chroot`
- **Implementation language**: `bash`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `constrained_build`
  - `instruction_framing`: `design-brief`
  - `hardness_source`: `design search`
- **Topology**: `offline rescue chroot`
- **Framing**: Build rescue chroot rebinding active root under capability and size constraints.
- **Discoveries / design insights**:
  - pivot vs bind rescue paths differ
  - ld.so cache must target rescue root
  - device node minimal set varies backend
- **Frontier failure modes**:
  - pivot bind diff
  - ld.so cache
  - device minimal set
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`

### 6. Quota rollback skew variant
- **id**: `quota-rollback-skew-variant`
- **Status**: `bank-ready`
- **Benchmark category**: `troubleshooting`
- **Portal category**: `debugging`
- **Architecture family**: `quota_rollback_skew`
- **Implementation language**: `cpp`
- **Subcategories**: `[]`
- **task_shape**:
  - `type`: `repair_existing_system`
  - `instruction_framing`: `symptoms-only`
  - `hardness_source`: `diagnosis`
- **Topology**: `quota rollback skew`
- **Framing**: Project quotas double-count after directory reparent and rollback sequence.
- **Discoveries / design insights**:
  - project inheritance differs xfs ext4
  - quota check uses stale projid cache
  - reparent without remount skips hook
- **Frontier failure modes**:
  - inheritance diff
  - projid cache
  - reparent hook skip
- **realism_source**:
  - `source_type`: `real_system`
  - `evidence_basis`: `open-source issue`


---
## Coverage summary

- Total candidates: `80`
- Per benchmark category: `{'build-dependency': 5, 'build-management': 5, 'challenging-games': 5, 'cryptography': 6, 'data-processing': 6, 'data-scripting': 5, 'debugging': 6, 'large-codebase': 6, 'machine-learning': 6, 'scientific-computing-analysis': 6, 'security': 6, 'software-engineering': 6, 'system-configuration': 6, 'troubleshooting': 6}`
- Architecture family counts (pre-dedup): `{'offline_lockfile_rehydration': 1, 'abi_rebuild_drift': 1, 'hermetic_sandbox_build': 1, 'cross_compile_sysroot_skew': 1, 'bazel_query_stale_edge': 1, 'incremental_shadow_artifacts': 1, 'ci_matrix_cache_poison': 1, 'pipeline_stage_ordering': 1, 'dist_compile_cache_invalidation': 1, 'release_provenance_gap': 1, 'move_budget_sokoban_ladder': 1, 'procedural_level_replay': 1, 'transposition_table_bug': 1, 'game_logic_model_check': 1, 'input_remap_variant_ladder': 1, 'aead_nonce_reuse_recovery': 1, 'threshold_sig_shard_mismatch': 1, 'tls_extension_order_inference': 1, 'crypto_agility_ladder': 1, 'encrypted_backup_header': 1, 'passkey_challenge_replay': 1, 'stream_window_aggregate_drift': 1, 'schema_inference_ladder': 1, 'pii_redaction_ladder': 1, 'data_lineage_invariant_proof': 1, 'regex_extraction_inference': 1, 'metamorphic_etl_checksum': 1, 'pipeline_dag_checkpoint': 1, 'shell_env_inheritance': 1, 'notebook_cell_provenance': 1, 'cron_overlap_guard': 1, 'data_contract_validator_build': 1, 'journal_replay_generation_skew': 1, 'scheduler_persistence_reconciliation': 1, 'core_dump_stack_inference': 1, 'trace_context_propagation_break': 1, 'heisenbug_variant_ladder': 1, 'happens_before_model_check': 1, 'monorepo_import_cycle_repair': 1, 'legacy_bytecode_vm_inference': 1, 'cross_module_float_policy': 1, 'plugin_registry_authority_split': 1, 'query_plan_cost_model_optimize': 1, 'service_mesh_config_precedence': 1, 'checkpoint_optimizer_resume': 1, 'sampler_shard_divergence': 1, 'ood_detection_ladder': 1, 'mixed_precision_replay_ladder': 1, 'prompt_injection_eval_ladder': 1, 'isotonic_calibration_proof': 1, 'fft_resume_corruption': 1, 'cross_runtime_float_drift': 1, 'unit_conversion_drift': 1, 'monte_carlo_stratified': 1, 'symplectic_energy_drift': 1, 'interval_arithmetic_proof': 1, 'revocation_cache_split': 1, 'mac_boolean_precedence': 1, 'confused_deputy_rpc_guard': 1, 'waf_bypass_ladder': 1, 'supply_chain_sig_gap': 1, 'privilege_graph_proof': 1, 'typestate_protocol_proof': 1, 'async_fault_injection_ladder': 1, 'minimal_http_router_cap': 1, 'wire_protocol_pcap_inference': 1, 'codec_framing_ladder': 1, 'allocator_pool_optimize': 1, 'namespace_restore_replay': 1, 'cgroup_pressure_desync': 1, 'fstab_remount_ladder': 1, 'selinux_restorecon_generation': 1, 'systemd_timer_skew': 1, 'mount_propagation_formal': 1, 'overlay_lowerdir_stale_bind': 1, 'device_node_lineage': 1, 'watchdog_restart_boundary': 1, 'health_dependency_mask': 1, 'offline_rescue_chroot': 1, 'quota_rollback_skew': 1}`
- Note: families with count >2 require Phase 3 demotion before final 56.

