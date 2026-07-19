# Difficulty Mechanism Plan

## Mechanisms
- mechanism: journal_reconstruction
- mechanism: state_recovery
- mechanism: replay_system
- mechanism: cross_file_cross_format_invariants

## Failure Modes
- failure_mode: Models will likely overlook the implicit requirement to securely reconstruct the journal across arbitrary splits.
- failure_mode: Agents fail to recognize the replay_system invariants that require strict ordering of checksum transactions.
- failure_mode: The agent confuses state_recovery boundaries and drops final blocks upon recovery restart.
- failure_mode: Deceptive local evidence leads the model to skip secondary cache invalidation during recovery phases.
