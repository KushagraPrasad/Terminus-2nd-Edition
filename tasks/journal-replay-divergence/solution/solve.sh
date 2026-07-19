#!/usr/bin/env bash
set -euo pipefail

log() { printf '[solve] %s\n' "$1"; }

cd /app
mkdir -p /app/output /app/var/journal
rm -f /app/output/report.json

log "apply overlay core fixes"
cd /solution
patch -d /app -p0 --batch < oracle_core.patch

log "apply journal replay crate fixes"
install -m 0644 /solution/reference/lane_gate.rs /app/p7/lane_gate/src/lib.rs
install -m 0644 /solution/reference/fold_row.rs /app/p7/fold_row/src/lib.rs
install -m 0644 /solution/reference/wal_store.rs /app/p7/wal_store/src/lib.rs

cd /app
cargo build --release --locked
/app/target/release/journal_run

log "sanity-check output contract"
python3 <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/app/output/report.json").read_text(encoding="utf-8"))
assert data["summary"]["sync_status"] == "settled"
for row in data["rows"]:
    assert row["replay_ok"] and row["lane_ok"] and row["fold_ok"] and row["seal_ok"]
    assert row["drift_code"] == 0
PY

log "done"
