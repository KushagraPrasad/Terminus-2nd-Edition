Staged bring-up for our image studio harness looks healthy early on, but replay-heavy maintenance drifts late: packaged byte digests disagree with coordinator materializations in promotion tails, and cross-span comparisons conflict without an obvious first-pass fault.

Repair Python source under `/app/environment` so transcript materialization matches the public contract in `/app/environment/studio/app/docs/contract.md`. Runner-only or command-only changes are not sufficient; imported library modules must also be corrected. Static and manual output writes are insufficient: the verifier deletes `/app/output/recovery_transcript.json` and requires regeneration through the normal pipeline after the underlying logic is fixed.

Regenerate with:

    python3 /app/environment/runner.py --write /app/output/recovery_transcript.json

The contract defines the `runs` transcript schema and every entry field rule. Use the contract and bundled fixtures under `/app/environment/studio/app/data/` as the numeric reference while inspecting ingest buffers, coordinator stitching, journal apply, and replay paths under `/app/environment`.
