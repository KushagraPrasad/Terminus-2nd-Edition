# Validation Log: namespace-restore-replay-loop-028

## Attempt 1
- Derived score: 3 FAILs, 0 WARNs
- Evidence: specs/.runs/namespace-restore-replay-loop-028/attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.category_profile.allowed_instruction_disclosures: ['assets', 'obligations', 'optimization target', 'report schema'] is not of type 'string'
  - Schema validation failed at $.category_profile.category_specific_verifier_risks: ['toy checklist', 'golden report leakage'] is not of type 'string'
  - Schema validation failed at $.category_profile.forbidden_instruction_leaks: ['patch sites', 'replay phase', 'fast-path module'] is not of type 'string'
- Blocking evidence failures:
  - Schema validation failed at $.category_profile.allowed_instruction_disclosures: ['assets', 'obligations', 'optimization target', 'report schema'] is not of type 'string'
  - Schema validation failed at $.category_profile.category_specific_verifier_risks: ['toy checklist', 'golden report leakage'] is not of type 'string'
  - Schema validation failed at $.category_profile.forbidden_instruction_leaks: ['patch sites', 'replay phase', 'fast-path module'] is not of type 'string'

## Attempt 2
- Derived score: 2 FAILs, 0 WARNs
- Evidence: specs/.runs/namespace-restore-replay-loop-028/attempt-2-evidence.json
- Evidence errors:
  - anti_trivialization_checks is missing required ids: disclosure_collapse, hidden_instance, single_artifact_repair, generalization, prompt_honesty, cheating_vs_difficulty, mechanical_fix_filter, localized_fix, oracle_locality, small_declarative_cluster, grep_collapse, pre_factored_helper, recipe_discount, security_aura_discount, orthogonal_checklist, harness_discount, one_pass_solvability, hard_only_gate, discovery_budget_test, instruction_specificity_test, topology_distribution_test.
  - anti_trivialization_checks contains unexpected ids: c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21.
- Blocking evidence failures:
  - anti_trivialization_checks is missing required ids: disclosure_collapse, hidden_instance, single_artifact_repair, generalization, prompt_honesty, cheating_vs_difficulty, mechanical_fix_filter, localized_fix, oracle_locality, small_declarative_cluster, grep_collapse, pre_factored_helper, recipe_discount, security_aura_discount, orthogonal_checklist, harness_discount, one_pass_solvability, hard_only_gate, discovery_budget_test, instruction_specificity_test, topology_distribution_test.
  - anti_trivialization_checks contains unexpected ids: c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21.

## Attempt 3
- Derived score: 20 FAILs, 0 WARNs
- Evidence: specs/.runs/namespace-restore-replay-loop-028/attempt-3-evidence.json
- Evidence errors:
  - anti_trivialization_checks entry 'disclosure_collapse' must use name 'Disclosure-collapse', found 'Disclosure Collapse'.
  - anti_trivialization_checks entry 'hidden_instance' must use name 'Hidden-instance', found 'Hidden Instance'.
  - anti_trivialization_checks entry 'single_artifact_repair' must use name 'Single-artifact repair', found 'Single Artifact Repair'.
  - anti_trivialization_checks entry 'prompt_honesty' must use name 'Prompt-honesty', found 'Prompt Honesty'.
  - anti_trivialization_checks entry 'cheating_vs_difficulty' must use name 'Cheating-vs-difficulty', found 'Cheating Vs Difficulty'.
  - anti_trivialization_checks entry 'mechanical_fix_filter' must use name 'Mechanical-fix filter', found 'Mechanical Fix Filter'.
  - anti_trivialization_checks entry 'localized_fix' must use name 'Localized-fix', found 'Localized Fix'.
  - anti_trivialization_checks entry 'oracle_locality' must use name 'Oracle-locality', found 'Oracle Locality'.
  - anti_trivialization_checks entry 'small_declarative_cluster' must use name 'Small declarative-cluster', found 'Small Declarative Cluster'.
  - anti_trivialization_checks entry 'grep_collapse' must use name 'Grep-collapse', found 'Grep Collapse'.
  - anti_trivialization_checks entry 'pre_factored_helper' must use name 'Pre-factored-helper', found 'Pre Factored Helper'.
  - anti_trivialization_checks entry 'recipe_discount' must use name 'Recipe-discount', found 'Recipe Discount'.
  - anti_trivialization_checks entry 'security_aura_discount' must use name 'Security-aura discount', found 'Security Aura Discount'.
  - anti_trivialization_checks entry 'orthogonal_checklist' must use name 'Orthogonal-checklist', found 'Orthogonal Checklist'.
  - anti_trivialization_checks entry 'harness_discount' must use name 'Harness-discount', found 'Harness Discount'.
  - anti_trivialization_checks entry 'one_pass_solvability' must use name 'One-pass solvability', found 'One Pass Solvability'.
  - anti_trivialization_checks entry 'hard_only_gate' must use name 'Hard-only gate', found 'Hard Only Gate'.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery Budget Test'.
  - anti_trivialization_checks entry 'instruction_specificity_test' must use name 'Instruction specificity test', found 'Instruction Specificity Test'.
  - anti_trivialization_checks entry 'topology_distribution_test' must use name 'Topology distribution test', found 'Topology Distribution Test'.
- Blocking evidence failures:
  - anti_trivialization_checks entry 'disclosure_collapse' must use name 'Disclosure-collapse', found 'Disclosure Collapse'.
  - anti_trivialization_checks entry 'hidden_instance' must use name 'Hidden-instance', found 'Hidden Instance'.
  - anti_trivialization_checks entry 'single_artifact_repair' must use name 'Single-artifact repair', found 'Single Artifact Repair'.
  - anti_trivialization_checks entry 'prompt_honesty' must use name 'Prompt-honesty', found 'Prompt Honesty'.
  - anti_trivialization_checks entry 'cheating_vs_difficulty' must use name 'Cheating-vs-difficulty', found 'Cheating Vs Difficulty'.
  - anti_trivialization_checks entry 'mechanical_fix_filter' must use name 'Mechanical-fix filter', found 'Mechanical Fix Filter'.
  - anti_trivialization_checks entry 'localized_fix' must use name 'Localized-fix', found 'Localized Fix'.
  - anti_trivialization_checks entry 'oracle_locality' must use name 'Oracle-locality', found 'Oracle Locality'.
  - anti_trivialization_checks entry 'small_declarative_cluster' must use name 'Small declarative-cluster', found 'Small Declarative Cluster'.
  - anti_trivialization_checks entry 'grep_collapse' must use name 'Grep-collapse', found 'Grep Collapse'.
  - anti_trivialization_checks entry 'pre_factored_helper' must use name 'Pre-factored-helper', found 'Pre Factored Helper'.
  - anti_trivialization_checks entry 'recipe_discount' must use name 'Recipe-discount', found 'Recipe Discount'.
  - anti_trivialization_checks entry 'security_aura_discount' must use name 'Security-aura discount', found 'Security Aura Discount'.
  - anti_trivialization_checks entry 'orthogonal_checklist' must use name 'Orthogonal-checklist', found 'Orthogonal Checklist'.
  - anti_trivialization_checks entry 'harness_discount' must use name 'Harness-discount', found 'Harness Discount'.
  - anti_trivialization_checks entry 'one_pass_solvability' must use name 'One-pass solvability', found 'One Pass Solvability'.
  - anti_trivialization_checks entry 'hard_only_gate' must use name 'Hard-only gate', found 'Hard Only Gate'.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery Budget Test'.
  - anti_trivialization_checks entry 'instruction_specificity_test' must use name 'Instruction specificity test', found 'Instruction Specificity Test'.
  - anti_trivialization_checks entry 'topology_distribution_test' must use name 'Topology distribution test', found 'Topology Distribution Test'.

## Attempt 4
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/namespace-restore-replay-loop-028/attempt-4-evidence.json

