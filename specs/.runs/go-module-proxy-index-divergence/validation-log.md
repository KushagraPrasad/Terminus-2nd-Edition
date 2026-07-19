# Validation Log: go-module-proxy-index-divergence

## Attempt 1
- Derived score: 1 FAILs, 0 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.realism_source.synthetic_exception_review: '' should be non-empty
- Blocking evidence failures:
  - Schema validation failed at $.realism_source.synthetic_exception_review: '' should be non-empty

## Attempt 2
- Derived score: 6 FAILs, 1 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-2-evidence.json
- Evidence errors:
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery / design budget test (BLOCKING)'.
  - anti_trivialization_checks entry 'topology_distribution_test' must use name 'Topology distribution test', found 'Topology distribution test (BLOCKING)'.
  - test name 'test_version_list_consistency' contains forbidden instruction noun 'version'.
- Blocking evidence failures:
  - verifier_scoring_plan metric 'deliverable_completeness' weight 0.20 drifts too far from recommended 0.05.
  - verifier_scoring_plan.overall_threshold should be >= 0.99 for binary hard-task acceptance.
  - subtype_milestone_plan.local_only_data must be true; hard tasks must pre-bundle required data locally.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery / design budget test (BLOCKING)'.
  - anti_trivialization_checks entry 'topology_distribution_test' must use name 'Topology distribution test', found 'Topology distribution test (BLOCKING)'.
  - test name 'test_version_list_consistency' contains forbidden instruction noun 'version'.

## Attempt 3
- Derived score: 0 FAILs, 1 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-3-evidence.json

## Attempt 4
- Derived score: 0 FAILs, 1 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-4-evidence.json

## Attempt 5
- Derived score: 0 FAILs, 1 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-5-evidence.json

## Attempt 6
- Derived score: 1 FAILs, 0 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-6-evidence.json
- Evidence errors:
  - test name 'test_latest_resolves_active_version' contains forbidden instruction noun 'version'.
- Blocking evidence failures:
  - test name 'test_latest_resolves_active_version' contains forbidden instruction noun 'version'.

## Attempt 7
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-7-evidence.json

## Attempt 8
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/go-module-proxy-index-divergence/attempt-8-evidence.json

