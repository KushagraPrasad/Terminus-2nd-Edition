### Decision
GO

### Metadata
- Task name: calibration-isotonic-monotonic-proof
- Title: Calibration Isotonic Monotonic Proof
- Category: machine-learning
- Task shape: formal_reasoning
- Languages: ["python"]
- Difficulty: hard
- Milestones: 3

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m environment.tools.calib_runner` rebuilds `/app/output/calibration_isotonic_monotonic_proof_report.json`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by isotonic calibration breaks monotonicity after bucket merge on resume.

### subtype_milestone_plan
- milestone_count: 3
- sequential_dependency: strict
