# Validation Log: lease-recovery-coordinator

## Attempt 1
- Derived score: 2 FAILs, 1 WARNs
- Evidence: specs/.runs/lease-recovery-coordinator/attempt-1-evidence.json
- Evidence errors:
  - test name 'test_duplicate_jobs_are_moved_to_canonical_shards_before_old_shard_journals_apply' contains forbidden instruction noun 'journals'.
  - naming_pass.concentration_math disagrees with computed values: location 'partition_resolver' ratio supplied=0.2667 computed=0.266667; location 'reconcile_state_machine' ratio supplied=0.4667 computed=0.466667; location 'reconcile_run' ratio supplied=0.4667 computed=0.466667
- Blocking evidence failures:
  - test name 'test_duplicate_jobs_are_moved_to_canonical_shards_before_old_shard_journals_apply' contains forbidden instruction noun 'journals'.
  - naming_pass.concentration_math disagrees with computed values: location 'partition_resolver' ratio supplied=0.2667 computed=0.266667; location 'reconcile_state_machine' ratio supplied=0.4667 computed=0.466667; location 'reconcile_run' ratio supplied=0.4667 computed=0.466667

## Attempt 2
- Derived score: 0 FAILs, 1 WARNs
- Evidence: specs/.runs/lease-recovery-coordinator/attempt-2-evidence.json

## Attempt 3
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/lease-recovery-coordinator/attempt-3-evidence.json

