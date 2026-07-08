# Frontier 56 Benchmark

Anti-template HARD/EXPERT benchmark collection for frontier coding agent evaluation.

## Workflow

1. **Phase 0** — Audit existing seeds, specs, tasks (`phase0-saturation-report.md`)
2. **Phase 1** — 80 candidate concepts (`phase1-candidates-80.md`)
3. **Phase 2** — Architecture clustering (`phase2-clusters.md`)
4. **Phase 3** — Dedup and anti-template filter (`phase3-dedup-report.md`)
5. **Phase 4** — Select 56 + distinctiveness (`phase4-final-56.md`, `registry.toml`)
6. **Phase 5** — TB3 Steps 2a–4 per task (batched under `batches/`)
7. **Phase 6** — Final diversity self-audit

## Quotas

- **56 tasks** total — exactly 4 per benchmark category (14 categories)
- **≤2 tasks** per architecture family (`architecture-families.yaml`)
- **Pairwise similarity** — reject pairs >75%; document 70–75% pairs

## Commands

```bash
# Generate 80 candidates
python3 scripts/generate_frontier_56_candidates.py

# Run diversity audit (similarity matrix, family caps, anti-template)
python3 scripts/benchmark_diversity_audit.py \
  --candidates benchmark/frontier-56/phase1-candidates-80.md \
  --registry benchmark/frontier-56/registry.toml \
  --output benchmark/frontier-56/phase4-similarity-matrix.json

# Phase 0 saturation audit
python3 scripts/benchmark_diversity_audit.py --phase0 \
  --output benchmark/frontier-56/phase0-saturation-report.json

# Select final 56 from candidates
python3 scripts/benchmark_diversity_audit.py --select-56 \
  --candidates benchmark/frontier-56/phase1-candidates-80.md \
  --registry benchmark/frontier-56/registry.toml \
  --report benchmark/frontier-56/phase4-final-56.md

# Link specs + Step 4 orchestration
python3 scripts/frontier_56_mechanical_fixes.py
python3 scripts/frontier_56_step4.py --link-specs
python3 scripts/frontier_56_step4.py --status
python3 scripts/frontier_56_approve_all.py --resume
PYTHONPATH=$PWD python3 scripts/frontier_56_step4.py --step4 <registry-id>
```

See `benchmark/frontier-56/approval-status.json` for per-task Step 4 progress.

## Registry

[`registry.toml`](registry.toml) is the machine-readable roster. Status values:
`concept` → `spec` → `task` → `approved`.

## TB3 pipeline per task

See [`commands.md`](../../commands.md) and [`prompts/`](../../prompts/).
