# Verifier notes

Scoring rebuilds the matrix with `cmake -S /app -B /app/build`, `cmake --build /app/build -j2`, and `/app/bin/snapshot_matrix`, then runs pytest on the regenerated `/app/output/report.json`.

Harness-only pytest flags such as `--ctrf` are not part of the repair contract.
