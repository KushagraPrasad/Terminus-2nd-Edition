# Validation Log: distributed-tombstone-revival-015

## Attempt 1
- Derived score: 3 FAILs, 0 WARNs
- Evidence: specs/.runs/distributed-tombstone-revival-015/attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.calibration_plan: Additional properties are not allowed ('post_upload_difficulty', 'verifier_offline' were unexpected)
  - Schema validation failed at $.difficulty_mechanism_plan: {'mechanisms': ['stateful_multi_step_dependencies', 'false_green_intermediate_states', 'buried_local_constraints', 'rollback_recovery_requirements', 'cross_file_cross_format_invariants'], 'adversarial_layers_count': 5, 'fairness_guardrails': 'Deterministic offline cargo; no timing thresholds', 'layers': [{'mechanism': 'stateful_multi_step_dependencies', 'placement': 'cargo rebuild then tv driver then JSON report', 'why_model_misses_it': 'patches sources without locked rebuild graph', 'fairness_guardrail': 'build_hints document commands'}, {'mechanism': 'false_green_intermediate_states', 'placement': 'lane_mux closure before replay completes', 'why_model_misses_it': 'stops at quiesced summary with disagreeing echo pairs', 'fairness_guardrail': 'tests require pair agreement'}, {'mechanism': 'buried_local_constraints', 'placement': 'mix_key lineage fold in seal.rs', 'why_model_misses_it': 'facet_hex looks valid while skew stays wrong', 'fairness_guardrail': 'ablation test reverts fold'}, {'mechanism': 'rollback_recovery_requirements', 'placement': 'pack_bind durable refresh after partial recovery', 'why_model_misses_it': 'probe_ok true while gen_ok/store_ok diverge', 'fairness_guardrail': 'dual-crate ablation'}, {'mechanism': 'cross_file_cross_format_invariants', 'placement': 'emit_rows vs data/*.toml seeds', 'why_model_misses_it': 'JSON shape passes without seed cross-check', 'fairness_guardrail': 'pipeline rebuild tests'}]} is not of type 'array'
  - Schema validation failed at $.verifier_scoring_plan.metrics: {'functional_correctness': 0.45, 'hidden_invariants': 0.25, 'state_hygiene': 0.15, 'interface_correctness': 0.1, 'deliverable_completeness': 0.05} is not of type 'array'
- Blocking evidence failures:
  - Schema validation failed at $.calibration_plan: Additional properties are not allowed ('post_upload_difficulty', 'verifier_offline' were unexpected)
  - Schema validation failed at $.difficulty_mechanism_plan: {'mechanisms': ['stateful_multi_step_dependencies', 'false_green_intermediate_states', 'buried_local_constraints', 'rollback_recovery_requirements', 'cross_file_cross_format_invariants'], 'adversarial_layers_count': 5, 'fairness_guardrails': 'Deterministic offline cargo; no timing thresholds', 'layers': [{'mechanism': 'stateful_multi_step_dependencies', 'placement': 'cargo rebuild then tv driver then JSON report', 'why_model_misses_it': 'patches sources without locked rebuild graph', 'fairness_guardrail': 'build_hints document commands'}, {'mechanism': 'false_green_intermediate_states', 'placement': 'lane_mux closure before replay completes', 'why_model_misses_it': 'stops at quiesced summary with disagreeing echo pairs', 'fairness_guardrail': 'tests require pair agreement'}, {'mechanism': 'buried_local_constraints', 'placement': 'mix_key lineage fold in seal.rs', 'why_model_misses_it': 'facet_hex looks valid while skew stays wrong', 'fairness_guardrail': 'ablation test reverts fold'}, {'mechanism': 'rollback_recovery_requirements', 'placement': 'pack_bind durable refresh after partial recovery', 'why_model_misses_it': 'probe_ok true while gen_ok/store_ok diverge', 'fairness_guardrail': 'dual-crate ablation'}, {'mechanism': 'cross_file_cross_format_invariants', 'placement': 'emit_rows vs data/*.toml seeds', 'why_model_misses_it': 'JSON shape passes without seed cross-check', 'fairness_guardrail': 'pipeline rebuild tests'}]} is not of type 'array'
  - Schema validation failed at $.verifier_scoring_plan.metrics: {'functional_correctness': 0.45, 'hidden_invariants': 0.25, 'state_hygiene': 0.15, 'interface_correctness': 0.1, 'deliverable_completeness': 0.05} is not of type 'array'

## Attempt 2
- Derived score: 23 FAILs, 0 WARNs
- Evidence: specs/.runs/distributed-tombstone-revival-015/attempt-2-evidence.json
- Evidence errors:
  - hardness_axes is missing required ids: diagnose_or_design.
  - hardness_axes contains unexpected ids: diagnose.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery budget test'.
  - test name 'test_rows_wave_table' contains forbidden instruction noun 'wave'.
  - test name 'test_rows_wave_table' contains forbidden instruction noun 'rows'.
  - test name 'test_paired_echo_agreement' contains forbidden instruction noun 'echo'.
  - test name 'test_closure_flags_zero_skew' contains forbidden instruction noun 'closure'.
  - test name 'test_closure_flags_zero_skew' contains forbidden instruction noun 'skew'.
  - test name 'test_summary_reconcile_quiesced' contains forbidden instruction noun 'quiesced'.
  - test name 'test_summary_reconcile_quiesced' contains forbidden instruction noun 'reconcile'.
  - test name 'test_summary_reconcile_quiesced' contains forbidden instruction noun 'summary'.
  - test name 'test_span_band_matches_skew' contains forbidden instruction noun 'skew'.
  - test name 'test_span_band_matches_skew' contains forbidden instruction noun 'span'.
  - test name 'test_trace_digest_driver_contract' contains forbidden instruction noun 'driver'.
  - test name 'test_trace_digest_driver_contract' contains forbidden instruction noun 'trace'.
  - test name 'test_trace_digest_driver_contract' contains forbidden instruction noun 'digest'.
  - test name 'test_trace_digest_anchor' contains forbidden instruction noun 'trace'.
  - test name 'test_trace_digest_anchor' contains forbidden instruction noun 'digest'.
  - test name 'test_facet_hex_shape' contains forbidden instruction noun 'facet'.
  - test name 'test_facet_hex_shape' contains forbidden instruction noun 'hex'.
  - test name 'test_rows_total_integer' contains forbidden instruction noun 'rows'.
  - test name 'test_pipeline_overwrites_manual_json' contains forbidden instruction noun 'manual'.
  - test name 'test_store_ladder_sensitivity' contains forbidden instruction noun 'store'.
- Blocking evidence failures:
  - hardness_axes is missing required ids: diagnose_or_design.
  - hardness_axes contains unexpected ids: diagnose.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery budget test'.
  - test name 'test_rows_wave_table' contains forbidden instruction noun 'wave'.
  - test name 'test_rows_wave_table' contains forbidden instruction noun 'rows'.
  - test name 'test_paired_echo_agreement' contains forbidden instruction noun 'echo'.
  - test name 'test_closure_flags_zero_skew' contains forbidden instruction noun 'closure'.
  - test name 'test_closure_flags_zero_skew' contains forbidden instruction noun 'skew'.
  - test name 'test_summary_reconcile_quiesced' contains forbidden instruction noun 'quiesced'.
  - test name 'test_summary_reconcile_quiesced' contains forbidden instruction noun 'reconcile'.
  - test name 'test_summary_reconcile_quiesced' contains forbidden instruction noun 'summary'.
  - test name 'test_span_band_matches_skew' contains forbidden instruction noun 'skew'.
  - test name 'test_span_band_matches_skew' contains forbidden instruction noun 'span'.
  - test name 'test_trace_digest_driver_contract' contains forbidden instruction noun 'driver'.
  - test name 'test_trace_digest_driver_contract' contains forbidden instruction noun 'trace'.
  - test name 'test_trace_digest_driver_contract' contains forbidden instruction noun 'digest'.
  - test name 'test_trace_digest_anchor' contains forbidden instruction noun 'trace'.
  - test name 'test_trace_digest_anchor' contains forbidden instruction noun 'digest'.
  - test name 'test_facet_hex_shape' contains forbidden instruction noun 'facet'.
  - test name 'test_facet_hex_shape' contains forbidden instruction noun 'hex'.
  - test name 'test_rows_total_integer' contains forbidden instruction noun 'rows'.
  - test name 'test_pipeline_overwrites_manual_json' contains forbidden instruction noun 'manual'.
  - test name 'test_store_ladder_sensitivity' contains forbidden instruction noun 'store'.

## Attempt 3
- Derived score: 5 FAILs, 0 WARNs
- Evidence: specs/.runs/distributed-tombstone-revival-015/attempt-3-evidence.json
- Evidence errors:
  - test name 'test_q9_closure_zero' contains forbidden instruction noun 'closure'.
  - test name 'test_q11_span_match' contains forbidden instruction noun 'span'.
  - test name 'test_q12_digest_contract' contains forbidden instruction noun 'digest'.
  - test name 'test_q13_digest_anchor' contains forbidden instruction noun 'digest'.
  - test name 'test_q14_hex_format' contains forbidden instruction noun 'hex'.
- Blocking evidence failures:
  - test name 'test_q9_closure_zero' contains forbidden instruction noun 'closure'.
  - test name 'test_q11_span_match' contains forbidden instruction noun 'span'.
  - test name 'test_q12_digest_contract' contains forbidden instruction noun 'digest'.
  - test name 'test_q13_digest_anchor' contains forbidden instruction noun 'digest'.
  - test name 'test_q14_hex_format' contains forbidden instruction noun 'hex'.

## Attempt 4
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/distributed-tombstone-revival-015/attempt-4-evidence.json

## Attempt 5
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/distributed-tombstone-revival-015/attempt-5-evidence.json

