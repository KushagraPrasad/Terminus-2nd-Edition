### Decision
GO

### Metadata
- Task name: constraint-serializer-builder
- Title: Constraint Serializer Builder
- Category: software-engineering
- Task shape: constrained_build
- Languages: ["python"]
- Difficulty: hard
- Milestones: 4

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.serial_runner` rebuilds `/app/output/constraint_serializer_builder_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by constraint serializer omits field tags required by downstream validator arms.

### subtype_milestone_plan
- milestone_count: 4
- sequential_dependency: strict
