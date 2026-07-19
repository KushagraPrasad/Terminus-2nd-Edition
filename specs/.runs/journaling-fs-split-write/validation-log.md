# Validation Log: journaling-fs-split-write

## Attempt 1
- Derived score: 2 FAILs, 0 WARNs
- Evidence: specs/.runs/journaling-fs-split-write/attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.naming_pass: Additional properties are not allowed ('recomputed_concentration' was unexpected)
  - Schema validation failed at $.waiver_plan.waivers_expected: 'none' is not of type 'boolean'
- Blocking evidence failures:
  - Schema validation failed at $.naming_pass: Additional properties are not allowed ('recomputed_concentration' was unexpected)
  - Schema validation failed at $.waiver_plan.waivers_expected: 'none' is not of type 'boolean'

## Attempt 2
- Derived score: 2 FAILs, 0 WARNs
- Evidence: specs/.runs/journaling-fs-split-write/attempt-2-evidence.json
- Evidence errors:
  - platform_files is missing required platform path(s): construction_manifest.json, instruction.md, output_contract.toml, solution/solve.sh, task.toml, tests/test_outputs.py
  - task_files entries must be under environment/ or steps/: tests/test_recovery.py
- Blocking evidence failures:
  - platform_files is missing required platform path(s): construction_manifest.json, instruction.md, output_contract.toml, solution/solve.sh, task.toml, tests/test_outputs.py
  - task_files entries must be under environment/ or steps/: tests/test_recovery.py

## Attempt 3
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/journaling-fs-split-write/attempt-3-evidence.json

