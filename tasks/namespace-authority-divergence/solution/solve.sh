#!/usr/bin/env bash
set -euo pipefail

log() { printf '[solve] %s\n' "$1"; }

cd /app
mkdir -p /app/output
rm -f /app/output/recovery_transcript.json

log "apply source fixes"
if grep -q 'probe_quench' /app/m2/q19/src/mux_path.rs; then
  echo "solve: baseline already patched" >&2
else
  cd /solution
  patch -d /app -p0 --batch < oracle.patch
fi
cd /app
cargo build --release --locked
/app/target/release/rx

log "sanity-check output contract"
python3 <<'PY'
import json
from pathlib import Path

data = json.loads(Path("/app/output/recovery_transcript.json").read_text(encoding="utf-8"))
assert data["summary"]["roll_digest"] == "004f7027"
seq = []
for run in data["runs"]:
    for ent in run["entries"]:
        seq.append(int(ent["tail_seq"]))
assert seq == list(range(1, len(seq) + 1))
PY

log "done"
