# Validation Log: offline-lockfile-rehydration-017

## Attempt 1
- Derived score: 9 FAILs, 0 WARNs
- Evidence: specs/.runs/offline-lockfile-rehydration-017/attempt-1-evidence.json
- Evidence errors:
  - test name 'test_h3_matrix_layout' contains forbidden instruction noun 'matrix'.
  - test name 'test_h6_sync_label' contains forbidden instruction noun 'sync'.
  - test name 'test_h6_sync_label' contains forbidden instruction noun 'sync_label'.
  - test name 'test_h7_band_span' contains forbidden instruction noun 'band_span'.
  - test name 'test_h11_rows_total' contains forbidden instruction noun 'rows_total'.
  - test name 'test_h14_bind_mutate' contains forbidden instruction noun 'bind'.
  - test name 'test_h18_perm_generalization' contains forbidden instruction noun 'generalization'.
  - test name 'test_h20_cli_replay_surface' contains forbidden instruction noun 'replay'.
  - naming_pass.concentration_math disagrees with computed values: total_tests supplied=18 computed=17; location 'A' ratio supplied=0.2777777777777778 computed=0.294118; location 'B' ratio supplied=0.1111111111111111 computed=0.117647; location 'C' ratio supplied=0.2777777777777778 computed=0.294118; location 'D' ratio supplied=0.2777777777777778 computed=0.294118
- Blocking evidence failures:
  - test name 'test_h3_matrix_layout' contains forbidden instruction noun 'matrix'.
  - test name 'test_h6_sync_label' contains forbidden instruction noun 'sync'.
  - test name 'test_h6_sync_label' contains forbidden instruction noun 'sync_label'.
  - test name 'test_h7_band_span' contains forbidden instruction noun 'band_span'.
  - test name 'test_h11_rows_total' contains forbidden instruction noun 'rows_total'.
  - test name 'test_h14_bind_mutate' contains forbidden instruction noun 'bind'.
  - test name 'test_h18_perm_generalization' contains forbidden instruction noun 'generalization'.
  - test name 'test_h20_cli_replay_surface' contains forbidden instruction noun 'replay'.
  - naming_pass.concentration_math disagrees with computed values: total_tests supplied=18 computed=17; location 'A' ratio supplied=0.2777777777777778 computed=0.294118; location 'B' ratio supplied=0.1111111111111111 computed=0.117647; location 'C' ratio supplied=0.2777777777777778 computed=0.294118; location 'D' ratio supplied=0.2777777777777778 computed=0.294118

## Attempt 2
- Derived score: 2 FAILs, 0 WARNs
- Evidence: specs/.runs/offline-lockfile-rehydration-017/attempt-2-evidence.json
- Evidence errors:
  - test name 'test_h18_extra_orderings' contains forbidden instruction noun 'ordering'.
  - test name 'test_h20_argv_surface' contains forbidden instruction noun 'argv'.
- Blocking evidence failures:
  - test name 'test_h18_extra_orderings' contains forbidden instruction noun 'ordering'.
  - test name 'test_h20_argv_surface' contains forbidden instruction noun 'argv'.

## Attempt 3
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/offline-lockfile-rehydration-017/attempt-3-evidence.json

## Attempt 4
- Derived score: 1 FAILs, 0 WARNs
- Evidence: specs/.runs/offline-lockfile-rehydration-017/attempt-4-evidence.json
- Evidence errors:
  - test name 'test_h13_repeat_stable' contains forbidden instruction noun 'table'.
- Blocking evidence failures:
  - test name 'test_h13_repeat_stable' contains forbidden instruction noun 'table'.

