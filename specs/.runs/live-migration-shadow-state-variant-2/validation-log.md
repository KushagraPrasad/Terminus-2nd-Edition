# Validation Log: live-migration-shadow-state-variant-2

## Attempt 1
- Derived score: 6 FAILs, 0 WARNs
- Evidence: specs/.runs/live-migration-shadow-state-variant-2/attempt-1-evidence.json
- Evidence errors:
  - hardness_axes is missing required ids: discover, synthesize, diagnose_or_design, navigate_coupling, reason_beyond_training.
  - hardness_axes contains unexpected ids: H1, H2, H3, H4, H5.
  - anti_trivialization_checks is missing required ids: disclosure_collapse, hidden_instance, single_artifact_repair, generalization, prompt_honesty, cheating_vs_difficulty, mechanical_fix_filter, localized_fix, oracle_locality, small_declarative_cluster, grep_collapse, pre_factored_helper, recipe_discount, security_aura_discount, orthogonal_checklist, harness_discount, one_pass_solvability, hard_only_gate, discovery_budget_test, instruction_specificity_test, topology_distribution_test.
  - anti_trivialization_checks contains unexpected ids: AT1, AT2, AT3, AT4, AT5, AT6, AT7, AT8, AT9, AT10, AT11, AT12, AT13, AT14, AT15, AT16, AT17, AT18, AT19, AT20, AT21.
  - rubric_axes is missing required ids: verifiable, well_specified, solvable, difficult, interesting, outcome_verified.
  - rubric_axes contains unexpected ids: R1, R2, R3, R4, R5, R6.
- Blocking evidence failures:
  - hardness_axes is missing required ids: discover, synthesize, diagnose_or_design, navigate_coupling, reason_beyond_training.
  - hardness_axes contains unexpected ids: H1, H2, H3, H4, H5.
  - anti_trivialization_checks is missing required ids: disclosure_collapse, hidden_instance, single_artifact_repair, generalization, prompt_honesty, cheating_vs_difficulty, mechanical_fix_filter, localized_fix, oracle_locality, small_declarative_cluster, grep_collapse, pre_factored_helper, recipe_discount, security_aura_discount, orthogonal_checklist, harness_discount, one_pass_solvability, hard_only_gate, discovery_budget_test, instruction_specificity_test, topology_distribution_test.
  - anti_trivialization_checks contains unexpected ids: AT1, AT2, AT3, AT4, AT5, AT6, AT7, AT8, AT9, AT10, AT11, AT12, AT13, AT14, AT15, AT16, AT17, AT18, AT19, AT20, AT21.
  - rubric_axes is missing required ids: verifiable, well_specified, solvable, difficult, interesting, outcome_verified.
  - rubric_axes contains unexpected ids: R1, R2, R3, R4, R5, R6.

## Attempt 2
- Derived score: 2 FAILs, 0 WARNs
- Evidence: specs/.runs/live-migration-shadow-state-variant-2/attempt-2-evidence.json
- Evidence errors:
  - hardness_axes entry 'diagnose_or_design' must use name 'Diagnose or Design/Search', found 'Diagnose'.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery / design budget test'.
- Blocking evidence failures:
  - hardness_axes entry 'diagnose_or_design' must use name 'Diagnose or Design/Search', found 'Diagnose'.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery / design budget test'.

## Attempt 3
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/live-migration-shadow-state-variant-2/attempt-3-evidence.json

