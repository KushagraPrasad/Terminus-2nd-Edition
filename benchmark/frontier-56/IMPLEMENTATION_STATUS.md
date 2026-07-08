# Frontier 56 — Implementation Status

## Approval progress: **3/56**

| Registry ID | Zip | Status |
|-------------|-----|--------|
| `happens-before-model-check` | `Task_Ready_To_Submit/happens-before-model-check.zip` | **approved** |
| `cross-module-float-policy-drift` | `Task_Ready_To_Submit/cross-module-float-policy-drift.zip` | **approved** |
| `mac-policy-boolean-precedence` | `Task_Ready_To_Submit/mac-policy-boolean-precedence.zip` | **approved** |

Per-task Step 4 evidence: [`approval-status.json`](approval-status.json)

## Gate scan (latest)

- **`task_gate --skip-harbor` PASS:** 6/56
- **Harbor-ready + blocked on `approve_task`:** 3 (see approval-status.json)
- **Remaining:** need mechanical fixes + per-task remediation

## Batch commands (run in order)

```bash
# 1. Mechanical fixes (test.sh, difficulty, reference_pattern, output_contract, spec symlinks)
python3 scripts/frontier_56_mechanical_fixes.py

# 2. Scan local gates
python3 scripts/frontier_56_batch.py --batch 0 --preflight   # pilot 8
python3 scripts/frontier_56_batch.py --batch 1 --preflight   # batches 1-7

# 3. Drive Step 4 (Harbor + approve) — long-running
python3 scripts/frontier_56_approve_all.py --resume

# 4. Status
python3 scripts/frontier_56_step4.py --status
grep 'status = "approved"' benchmark/frontier-56/registry.toml | wc -l
```

## What blocks the remaining 53 tasks

| Blocker | ~Count | Fix |
|---------|--------|-----|
| `run_static_checks.py` | 30 | `output_contract.toml`, pinned apt, remove `rubric.txt`, Dockerfile hygiene |
| `actionability_check.py` | 11 | Instruction/schema disclosure |
| `collapse_check.py` | 3 | Instruction/oracle redesign |
| `spec_satisfiability` at approve | shared tasks | Registry-aligned specs, `category_profile`, reference pattern |
| Symlink registry IDs | 9 shared underlying | Approve per registry ID with logical name (supported in `approve_task.py`) |

## Infrastructure delivered

- `scripts/frontier_56_mechanical_fixes.py` — bulk mechanical remediation
- `scripts/frontier_56_approve_all.py` — Harbor + `approve_task.py --strict` batch driver
- `scripts/frontier_56_step4.py` — single-task Step 4
- `sample_task_3/` — tasks grouped by category (symlinks)
- `approve_task.py` — symlink-aware logical task names

## Honest estimate

Full **56/56 strict approval** requires continuing the batch loop above: mechanical fixes → `task_gate` → Harbor 3×3 + 10× + 20× → `approve_task.py --strict` per registry ID. Harbor alone is ~15–20 min per task (~14–18 hours total). Plan for multi-session batch runs using `--resume`.
