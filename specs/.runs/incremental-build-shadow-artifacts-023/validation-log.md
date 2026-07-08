# Validation Log: incremental-build-shadow-artifacts-023

## Attempt 1
- Derived score: 1 FAILs, 0 WARNs
- Evidence: specs/.runs/incremental-build-shadow-artifacts-023/attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.naming_pass: Additional properties are not allowed ('recomputed_concentration' was unexpected)
- Blocking evidence failures:
  - Schema validation failed at $.naming_pass: Additional properties are not allowed ('recomputed_concentration' was unexpected)

## Attempt 2
- Derived score: 5 FAILs, 0 WARNs
- Evidence: specs/.runs/incremental-build-shadow-artifacts-023/attempt-2-evidence.json
- Evidence errors:
  - test name 'test_r10_rerun_pipe' contains forbidden instruction noun 'rerun'.
  - test name 'test_r18_index_first' contains forbidden instruction noun 'index'.
  - test name 'test_r20_cli_hooks' contains forbidden instruction noun 'hook'.
  - test name 'test_r20_cli_hooks' contains forbidden instruction noun 'hooks'.
  - naming_pass.concentration_math disagrees with computed values: total_tests supplied=20 computed=18; location 'A' ratio supplied=0.25 computed=0.277778; location 'B' ratio supplied=0.1 computed=0.111111; location 'C' ratio supplied=0.3 computed=0.333333; location 'D' ratio supplied=0.25 computed=0.277778
- Blocking evidence failures:
  - test name 'test_r10_rerun_pipe' contains forbidden instruction noun 'rerun'.
  - test name 'test_r18_index_first' contains forbidden instruction noun 'index'.
  - test name 'test_r20_cli_hooks' contains forbidden instruction noun 'hook'.
  - test name 'test_r20_cli_hooks' contains forbidden instruction noun 'hooks'.
  - naming_pass.concentration_math disagrees with computed values: total_tests supplied=20 computed=18; location 'A' ratio supplied=0.25 computed=0.277778; location 'B' ratio supplied=0.1 computed=0.111111; location 'C' ratio supplied=0.3 computed=0.333333; location 'D' ratio supplied=0.25 computed=0.277778

## Attempt 3
- Derived score: 3 FAILs, 0 WARNs
- Evidence: specs/.runs/incremental-build-shadow-artifacts-023/attempt-3-evidence.json
- Evidence errors:
  - test name 'test_r10_pipe_trap' contains forbidden instruction noun 'trap'.
  - test name 'test_r20_argv_surface' contains forbidden instruction noun 'argv'.
  - test name 'test_r20_argv_surface' contains forbidden instruction noun 'surface'.
- Blocking evidence failures:
  - test name 'test_r10_pipe_trap' contains forbidden instruction noun 'trap'.
  - test name 'test_r20_argv_surface' contains forbidden instruction noun 'argv'.
  - test name 'test_r20_argv_surface' contains forbidden instruction noun 'surface'.

## Attempt 4
- Derived score: 3 FAILs, 0 WARNs
- Evidence: specs/.runs/incremental-build-shadow-artifacts-023/attempt-4-evidence.json
- Evidence errors:
  - test name 'test_r1_shape_rows' contains forbidden instruction noun 'rows'.
  - test name 'test_r9_len_rows' contains forbidden instruction noun 'rows'.
  - test name 'test_r17_flip_rows' contains forbidden instruction noun 'rows'.
- Blocking evidence failures:
  - test name 'test_r1_shape_rows' contains forbidden instruction noun 'rows'.
  - test name 'test_r9_len_rows' contains forbidden instruction noun 'rows'.
  - test name 'test_r17_flip_rows' contains forbidden instruction noun 'rows'.

## Attempt 5
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/incremental-build-shadow-artifacts-023/attempt-5-evidence.json

