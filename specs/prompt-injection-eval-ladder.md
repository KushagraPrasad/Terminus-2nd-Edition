### Decision
GO

### Metadata
- Task name: prompt-injection-eval-ladder
- Title: Prompt Injection Eval Ladder
- Category: machine-learning
- Task shape: adversarial_generalization
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.inject_runner` rebuilds `/app/output/prompt_injection_eval_ladder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by eval harness scores injected prompts as benign on intermediate ladder cases.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
