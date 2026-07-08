### Decision
GO

### Metadata
- Task name: game-logic-invariant-model-check
- Title: Game Logic Invariant Model Check
- Category: games
- Task shape: formal_reasoning
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.rules_runner` rebuilds `/app/output/game_logic_invariant_model_check_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by turn-based engine accepts illegal captures when en passant window drifts.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
