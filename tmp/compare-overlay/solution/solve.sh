#!/usr/bin/env bash
set -euo pipefail

log() { printf '[solve] %s\n' "$1"; }

cd /app
mkdir -p /app/output
rm -f /app/output/layer_report.json

log "apply source fixes"
cd /solution
patch -d /app -p0 --batch < oracle.patch
cd /app
cargo build --release --locked
/app/target/release/mk

log "sanity-check output contract"
python3 <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/app/output/layer_report.json").read_text(encoding="utf-8"))
assert data["summary"]["sync_status"] == "settled"
for row in data["rows"]:
    assert row["layer_ok"] and row["gen_ok"] and row["mount_ok"]
    assert row["drift_code"] == 0
PY

log "done"
