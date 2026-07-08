### Decision
GO

### Metadata
- Task name: ai-search-transposition-optimize
- Title: AI Search Transposition Optimize
- Category: games
- Task shape: optimization_under_constraints
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.search_runner` rebuilds `/app/output/ai_search_transposition_optimize_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by deterministic search loses best move when table eviction breaks collision policy.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
