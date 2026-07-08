### Decision
GO

### Metadata
- Task name: minimal-http-router-under-size-cap
- Title: Minimal HTTP Router Under Size Cap
- Category: software-engineering
- Task shape: constrained_build
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.router_runner` rebuilds `/app/output/minimal_http_router_under_size_cap_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by embedded router exceeds size cap while dropping trailing route table bytes.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
