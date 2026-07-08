### Decision
GO

### Metadata
- Task name: sampler-shard-divergence-repair
- Title: Sampler Shard Divergence Repair
- Category: machine-learning
- Task shape: repair_existing_system
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.sampler_runner` rebuilds `/app/output/sampler_shard_divergence_repair_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by distributed sampler shards disagree on epoch boundaries after resume.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
