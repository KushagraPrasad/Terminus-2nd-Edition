# Validation Log: token-revocation-freshness

## Attempt 1
- Derived score: 3 FAILs, 0 WARNs
- Evidence: specs/.runs/token-revocation-freshness/attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.topology_enumeration[0].locations: ['environment/src/cache.ts', 'tests/test_outputs.py'] is too short
  - Schema validation failed at $.topology_enumeration[1].locations: ['environment/src/store.ts', 'tests/test_outputs.py'] is too short
  - Schema validation failed at $.topology_enumeration[2].locations: ['environment/src/validator.ts', 'tests/test_outputs.py'] is too short
- Blocking evidence failures:
  - Schema validation failed at $.topology_enumeration[0].locations: ['environment/src/cache.ts', 'tests/test_outputs.py'] is too short
  - Schema validation failed at $.topology_enumeration[1].locations: ['environment/src/store.ts', 'tests/test_outputs.py'] is too short
  - Schema validation failed at $.topology_enumeration[2].locations: ['environment/src/validator.ts', 'tests/test_outputs.py'] is too short

## Attempt 2
- Derived score: 1 FAILs, 1 WARNs
- Evidence: specs/.runs/token-revocation-freshness/attempt-2-evidence.json
- Evidence errors:
  - test name 'test_monotonic_epoch_rollback' contains forbidden instruction noun 'epoch'.
- Blocking evidence failures:
  - test name 'test_monotonic_epoch_rollback' contains forbidden instruction noun 'epoch'.

## Attempt 3
- Derived score: 0 FAILs, 1 WARNs
- Evidence: specs/.runs/token-revocation-freshness/attempt-3-evidence.json

## Attempt 4
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/token-revocation-freshness/attempt-4-evidence.json

## Attempt 5
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/token-revocation-freshness/attempt-5-evidence.json

