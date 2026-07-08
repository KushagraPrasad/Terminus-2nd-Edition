# Phase 4 — Final 56 Roster

Locked concepts with closest-neighbor distinctiveness.

### offline-lockfile-rehydration-gap
- Benchmark category: build-dependency
- Architecture family: offline_lockfile_rehydration
- Closest neighbor: data-lineage-invariant-proof (0%)
- Differences: architecture offline_lockfile_rehydration vs data_lineage_invariant_proof; topology offline lockfile rehydration vs data lineage invariant proof; shape repair_existing_system vs formal_reasoning

### abi-rebuild-drift-detector
- Benchmark category: build-dependency
- Architecture family: abi_rebuild_drift
- Closest neighbor: core-dump-stack-inference (0%)
- Differences: architecture abi_rebuild_drift vs core_dump_stack_inference; topology ABI rebuild drift vs core dump stack inference; shape repair_existing_system vs reverse_engineering

### hermetic-sandbox-build-contract
- Benchmark category: build-dependency
- Architecture family: hermetic_sandbox_build
- Closest neighbor: bazel-query-graph-stale-edge (0%)
- Differences: architecture hermetic_sandbox_build vs bazel_query_stale_edge; topology hermetic sandbox build vs bazel query stale edge; shape constrained_build vs repair_existing_system

### bazel-query-graph-stale-edge
- Benchmark category: build-dependency
- Architecture family: bazel_query_stale_edge
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture bazel_query_stale_edge vs hermetic_sandbox_build; topology bazel query stale edge vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### incremental-build-shadow-artifacts
- Benchmark category: build-management
- Architecture family: incremental_shadow_artifacts
- Closest neighbor: game-logic-invariant-model-check (0%)
- Differences: architecture incremental_shadow_artifacts vs game_logic_model_check; topology incremental shadow artifacts vs game logic model check; shape repair_existing_system vs formal_reasoning

### distributed-compile-cache-invalidation
- Benchmark category: build-management
- Architecture family: dist_compile_cache_invalidation
- Closest neighbor: input-remap-variant-ladder (0%)
- Differences: architecture dist_compile_cache_invalidation vs input_remap_variant_ladder; topology dist compile cache invalidation vs input remap variant ladder; shape repair_existing_system vs adversarial_generalization

### ci-matrix-cache-poisoning
- Benchmark category: build-management
- Architecture family: ci_matrix_cache_poison
- Closest neighbor: move-budget-sokoban-variant-ladder (0%)
- Differences: architecture ci_matrix_cache_poison vs move_budget_sokoban_ladder; topology CI matrix cache poison vs move budget sokoban ladder; shape repair_existing_system vs adversarial_generalization

### pipeline-stage-ordering-trap
- Benchmark category: build-management
- Architecture family: pipeline_stage_ordering
- Closest neighbor: procedural-level-seed-replay (0%)
- Differences: architecture pipeline_stage_ordering vs procedural_level_replay; topology pipeline stage ordering vs procedural level replay; shape repair_existing_system vs repair_existing_system

### move-budget-sokoban-variant-ladder
- Benchmark category: challenging-games
- Architecture family: move_budget_sokoban_ladder
- Closest neighbor: ci-matrix-cache-poisoning (0%)
- Differences: architecture move_budget_sokoban_ladder vs ci_matrix_cache_poison; topology move budget sokoban ladder vs CI matrix cache poison; shape adversarial_generalization vs repair_existing_system

### procedural-level-seed-replay
- Benchmark category: challenging-games
- Architecture family: procedural_level_replay
- Closest neighbor: pipeline-stage-ordering-trap (0%)
- Differences: architecture procedural_level_replay vs pipeline_stage_ordering; topology procedural level replay vs pipeline stage ordering; shape repair_existing_system vs repair_existing_system

### game-logic-invariant-model-check
- Benchmark category: challenging-games
- Architecture family: game_logic_model_check
- Closest neighbor: incremental-build-shadow-artifacts (0%)
- Differences: architecture game_logic_model_check vs incremental_shadow_artifacts; topology game logic model check vs incremental shadow artifacts; shape formal_reasoning vs repair_existing_system

### input-remap-variant-ladder
- Benchmark category: challenging-games
- Architecture family: input_remap_variant_ladder
- Closest neighbor: distributed-compile-cache-invalidation (0%)
- Differences: architecture input_remap_variant_ladder vs dist_compile_cache_invalidation; topology input remap variant ladder vs dist compile cache invalidation; shape adversarial_generalization vs repair_existing_system

### aead-nonce-reuse-recovery
- Benchmark category: cryptography
- Architecture family: aead_nonce_reuse_recovery
- Closest neighbor: move-budget-sokoban-variant-ladder (0%)
- Differences: architecture aead_nonce_reuse_recovery vs move_budget_sokoban_ladder; topology AEAD nonce reuse recovery vs move budget sokoban ladder; shape repair_existing_system vs adversarial_generalization

### crypto-agility-variant-ladder
- Benchmark category: cryptography
- Architecture family: crypto_agility_ladder
- Closest neighbor: shell-task-env-inheritance-trap (0%)
- Differences: architecture crypto_agility_ladder vs shell_env_inheritance; topology crypto agility ladder vs shell env inheritance; shape adversarial_generalization vs repair_existing_system

### threshold-signature-shard-mismatch
- Benchmark category: cryptography
- Architecture family: threshold_sig_shard_mismatch
- Closest neighbor: distributed-compile-cache-invalidation (0%)
- Differences: architecture threshold_sig_shard_mismatch vs dist_compile_cache_invalidation; topology threshold sig shard mismatch vs dist compile cache invalidation; shape repair_existing_system vs repair_existing_system

### encrypted-backup-header-parse
- Benchmark category: cryptography
- Architecture family: encrypted_backup_header
- Closest neighbor: pipeline-stage-ordering-trap (0%)
- Differences: architecture encrypted_backup_header vs pipeline_stage_ordering; topology encrypted backup header vs pipeline stage ordering; shape repair_existing_system vs repair_existing_system

### data-lineage-invariant-proof
- Benchmark category: data-processing
- Architecture family: data_lineage_invariant_proof
- Closest neighbor: offline-lockfile-rehydration-gap (0%)
- Differences: architecture data_lineage_invariant_proof vs offline_lockfile_rehydration; topology data lineage invariant proof vs offline lockfile rehydration; shape formal_reasoning vs repair_existing_system

### stream-window-aggregate-drift
- Benchmark category: data-processing
- Architecture family: stream_window_aggregate_drift
- Closest neighbor: move-budget-sokoban-variant-ladder (0%)
- Differences: architecture stream_window_aggregate_drift vs move_budget_sokoban_ladder; topology stream window aggregate drift vs move budget sokoban ladder; shape repair_existing_system vs adversarial_generalization

### pii-redaction-variant-ladder
- Benchmark category: data-processing
- Architecture family: pii_redaction_ladder
- Closest neighbor: incremental-build-shadow-artifacts (0%)
- Differences: architecture pii_redaction_ladder vs incremental_shadow_artifacts; topology PII redaction ladder vs incremental shadow artifacts; shape adversarial_generalization vs repair_existing_system

### regex-extraction-trace-inference
- Benchmark category: data-processing
- Architecture family: regex_extraction_inference
- Closest neighbor: distributed-compile-cache-invalidation (0%)
- Differences: architecture regex_extraction_inference vs dist_compile_cache_invalidation; topology regex extraction inference vs dist compile cache invalidation; shape reverse_engineering vs repair_existing_system

### data-contract-validator-builder
- Benchmark category: data-scripting
- Architecture family: data_contract_validator_build
- Closest neighbor: distributed-compile-cache-invalidation (0%)
- Differences: architecture data_contract_validator_build vs dist_compile_cache_invalidation; topology data contract validator build vs dist compile cache invalidation; shape constrained_build vs repair_existing_system

### notebook-cell-reorder-provenance
- Benchmark category: data-scripting
- Architecture family: notebook_cell_provenance
- Closest neighbor: data-contract-validator-builder (0%)
- Differences: architecture notebook_cell_provenance vs data_contract_validator_build; topology notebook cell provenance vs data contract validator build; shape repair_existing_system vs constrained_build

### pipeline-dag-checkpoint-resume
- Benchmark category: data-scripting
- Architecture family: pipeline_dag_checkpoint
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture pipeline_dag_checkpoint vs hermetic_sandbox_build; topology pipeline DAG checkpoint vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### shell-task-env-inheritance-trap
- Benchmark category: data-scripting
- Architecture family: shell_env_inheritance
- Closest neighbor: bazel-query-graph-stale-edge (0%)
- Differences: architecture shell_env_inheritance vs bazel_query_stale_edge; topology shell env inheritance vs bazel query stale edge; shape repair_existing_system vs repair_existing_system

### core-dump-stack-inference
- Benchmark category: debugging
- Architecture family: core_dump_stack_inference
- Closest neighbor: abi-rebuild-drift-detector (0%)
- Differences: architecture core_dump_stack_inference vs abi_rebuild_drift; topology core dump stack inference vs ABI rebuild drift; shape reverse_engineering vs repair_existing_system

### happens-before-model-check
- Benchmark category: debugging
- Architecture family: happens_before_model_check
- Closest neighbor: distributed-compile-cache-invalidation (0%)
- Differences: architecture happens_before_model_check vs dist_compile_cache_invalidation; topology happens before model check vs dist compile cache invalidation; shape formal_reasoning vs repair_existing_system

### journal-replay-generation-skew
- Benchmark category: debugging
- Architecture family: journal_replay_generation_skew
- Closest neighbor: ci-matrix-cache-poisoning (0%)
- Differences: architecture journal_replay_generation_skew vs ci_matrix_cache_poison; topology journal replay generation skew vs CI matrix cache poison; shape repair_existing_system vs repair_existing_system

### heisenbug-variant-ladder
- Benchmark category: debugging
- Architecture family: heisenbug_variant_ladder
- Closest neighbor: offline-lockfile-rehydration-gap (0%)
- Differences: architecture heisenbug_variant_ladder vs offline_lockfile_rehydration; topology heisenbug variant ladder vs offline lockfile rehydration; shape adversarial_generalization vs repair_existing_system

### plugin-registry-authority-split
- Benchmark category: large-codebase
- Architecture family: plugin_registry_authority_split
- Closest neighbor: move-budget-sokoban-variant-ladder (0%)
- Differences: architecture plugin_registry_authority_split vs move_budget_sokoban_ladder; topology plugin registry authority split vs move budget sokoban ladder; shape repair_existing_system vs adversarial_generalization

### cross-module-float-policy-drift
- Benchmark category: large-codebase
- Architecture family: cross_module_float_policy
- Closest neighbor: aead-nonce-reuse-recovery (0%)
- Differences: architecture cross_module_float_policy vs aead_nonce_reuse_recovery; topology cross module float policy vs AEAD nonce reuse recovery; shape repair_existing_system vs repair_existing_system

### service-mesh-config-precedence
- Benchmark category: large-codebase
- Architecture family: service_mesh_config_precedence
- Closest neighbor: encrypted-backup-header-parse (0%)
- Differences: architecture service_mesh_config_precedence vs encrypted_backup_header; topology service mesh config precedence vs encrypted backup header; shape repair_existing_system vs repair_existing_system

### monorepo-import-cycle-repair
- Benchmark category: large-codebase
- Architecture family: monorepo_import_cycle_repair
- Closest neighbor: abi-rebuild-drift-detector (0%)
- Differences: architecture monorepo_import_cycle_repair vs abi_rebuild_drift; topology monorepo import cycle repair vs ABI rebuild drift; shape repair_existing_system vs repair_existing_system

### checkpoint-resume-optimizer-state
- Benchmark category: machine-learning
- Architecture family: checkpoint_optimizer_resume
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture checkpoint_optimizer_resume vs hermetic_sandbox_build; topology checkpoint optimizer resume vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### ood-detection-variant-ladder
- Benchmark category: machine-learning
- Architecture family: ood_detection_ladder
- Closest neighbor: incremental-build-shadow-artifacts (0%)
- Differences: architecture ood_detection_ladder vs incremental_shadow_artifacts; topology OOD detection ladder vs incremental shadow artifacts; shape adversarial_generalization vs repair_existing_system

### mixed-precision-replay-ladder
- Benchmark category: machine-learning
- Architecture family: mixed_precision_replay_ladder
- Closest neighbor: abi-rebuild-drift-detector (0%)
- Differences: architecture mixed_precision_replay_ladder vs abi_rebuild_drift; topology mixed precision replay ladder vs ABI rebuild drift; shape adversarial_generalization vs repair_existing_system

### sampler-shard-divergence-repair
- Benchmark category: machine-learning
- Architecture family: sampler_shard_divergence
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture sampler_shard_divergence vs hermetic_sandbox_build; topology sampler shard divergence vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### fft-resume-corruption
- Benchmark category: scientific-computing-analysis
- Architecture family: fft_resume_corruption
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture fft_resume_corruption vs hermetic_sandbox_build; topology FFT resume corruption vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### symplectic-integrator-energy-drift
- Benchmark category: scientific-computing-analysis
- Architecture family: symplectic_energy_drift
- Closest neighbor: pipeline-stage-ordering-trap (0%)
- Differences: architecture symplectic_energy_drift vs pipeline_stage_ordering; topology symplectic energy drift vs pipeline stage ordering; shape repair_existing_system vs repair_existing_system

### interval-arithmetic-proof-contract
- Benchmark category: scientific-computing-analysis
- Architecture family: interval_arithmetic_proof
- Closest neighbor: incremental-build-shadow-artifacts (0%)
- Differences: architecture interval_arithmetic_proof vs incremental_shadow_artifacts; topology interval arithmetic proof vs incremental shadow artifacts; shape formal_reasoning vs repair_existing_system

### monte-carlo-stratified-overlap
- Benchmark category: scientific-computing-analysis
- Architecture family: monte_carlo_stratified
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture monte_carlo_stratified vs hermetic_sandbox_build; topology monte carlo stratified vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### mac-policy-boolean-precedence
- Benchmark category: security
- Architecture family: mac_boolean_precedence
- Closest neighbor: ood-detection-variant-ladder (0%)
- Differences: architecture mac_boolean_precedence vs ood_detection_ladder; topology MAC boolean precedence vs OOD detection ladder; shape repair_existing_system vs adversarial_generalization

### supply-chain-sig-chain-gap
- Benchmark category: security
- Architecture family: supply_chain_sig_gap
- Closest neighbor: procedural-level-seed-replay (0%)
- Differences: architecture supply_chain_sig_gap vs procedural_level_replay; topology supply chain sig gap vs procedural level replay; shape repair_existing_system vs repair_existing_system

### privilege-graph-acyclic-proof
- Benchmark category: security
- Architecture family: privilege_graph_proof
- Closest neighbor: incremental-build-shadow-artifacts (0%)
- Differences: architecture privilege_graph_proof vs incremental_shadow_artifacts; topology privilege graph proof vs incremental shadow artifacts; shape formal_reasoning vs repair_existing_system

### revocation-cache-authority-split
- Benchmark category: security
- Architecture family: revocation_cache_split
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture revocation_cache_split vs hermetic_sandbox_build; topology revocation cache split vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### minimal-http-router-under-size-cap
- Benchmark category: software-engineering
- Architecture family: minimal_http_router_cap
- Closest neighbor: incremental-build-shadow-artifacts (0%)
- Differences: architecture minimal_http_router_cap vs incremental_shadow_artifacts; topology minimal HTTP router cap vs incremental shadow artifacts; shape constrained_build vs repair_existing_system

### typestate-protocol-proof
- Benchmark category: software-engineering
- Architecture family: typestate_protocol_proof
- Closest neighbor: pipeline-stage-ordering-trap (0%)
- Differences: architecture typestate_protocol_proof vs pipeline_stage_ordering; topology typestate protocol proof vs pipeline stage ordering; shape formal_reasoning vs repair_existing_system

### wire-protocol-from-pcap-inference
- Benchmark category: software-engineering
- Architecture family: wire_protocol_pcap_inference
- Closest neighbor: offline-lockfile-rehydration-gap (0%)
- Differences: architecture wire_protocol_pcap_inference vs offline_lockfile_rehydration; topology wire protocol pcap inference vs offline lockfile rehydration; shape reverse_engineering vs repair_existing_system

### async-fault-injection-ladder
- Benchmark category: software-engineering
- Architecture family: async_fault_injection_ladder
- Closest neighbor: incremental-build-shadow-artifacts (0%)
- Differences: architecture async_fault_injection_ladder vs incremental_shadow_artifacts; topology async fault injection ladder vs incremental shadow artifacts; shape adversarial_generalization vs repair_existing_system

### mount-propagation-formal-model
- Benchmark category: system-configuration
- Architecture family: mount_propagation_formal
- Closest neighbor: offline-lockfile-rehydration-gap (0%)
- Differences: architecture mount_propagation_formal vs offline_lockfile_rehydration; topology mount propagation formal vs offline lockfile rehydration; shape formal_reasoning vs repair_existing_system

### fstab-variant-remount-ladder
- Benchmark category: system-configuration
- Architecture family: fstab_remount_ladder
- Closest neighbor: ci-matrix-cache-poisoning (0%)
- Differences: architecture fstab_remount_ladder vs ci_matrix_cache_poison; topology fstab remount ladder vs CI matrix cache poison; shape adversarial_generalization vs repair_existing_system

### namespace-restore-replay-loop
- Benchmark category: system-configuration
- Architecture family: namespace_restore_replay
- Closest neighbor: game-logic-invariant-model-check (0%)
- Differences: architecture namespace_restore_replay vs game_logic_model_check; topology namespace restore replay vs game logic model check; shape repair_existing_system vs formal_reasoning

### cgroup-pressure-metric-desync
- Benchmark category: system-configuration
- Architecture family: cgroup_pressure_desync
- Closest neighbor: hermetic-sandbox-build-contract (0%)
- Differences: architecture cgroup_pressure_desync vs hermetic_sandbox_build; topology cgroup pressure desync vs hermetic sandbox build; shape repair_existing_system vs constrained_build

### device-node-lineage-mismatch
- Benchmark category: troubleshooting
- Architecture family: device_node_lineage
- Closest neighbor: encrypted-backup-header-parse (0%)
- Differences: architecture device_node_lineage vs encrypted_backup_header; topology device node lineage vs encrypted backup header; shape repair_existing_system vs repair_existing_system

### overlay-lowerdir-stale-bind
- Benchmark category: troubleshooting
- Architecture family: overlay_lowerdir_stale_bind
- Closest neighbor: move-budget-sokoban-variant-ladder (0%)
- Differences: architecture overlay_lowerdir_stale_bind vs move_budget_sokoban_ladder; topology overlay lowerdir stale bind vs move budget sokoban ladder; shape repair_existing_system vs adversarial_generalization

### watchdog-restart-boundary-debug
- Benchmark category: troubleshooting
- Architecture family: watchdog_restart_boundary
- Closest neighbor: offline-lockfile-rehydration-gap (0%)
- Differences: architecture watchdog_restart_boundary vs offline_lockfile_rehydration; topology watchdog restart boundary vs offline lockfile rehydration; shape repair_existing_system vs repair_existing_system

### quota-rollback-skew-variant
- Benchmark category: troubleshooting
- Architecture family: quota_rollback_skew
- Closest neighbor: pipeline-stage-ordering-trap (0%)
- Differences: architecture quota_rollback_skew vs pipeline_stage_ordering; topology quota rollback skew vs pipeline stage ordering; shape repair_existing_system vs repair_existing_system
