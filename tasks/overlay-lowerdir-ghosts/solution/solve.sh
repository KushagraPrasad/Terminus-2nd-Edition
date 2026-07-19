#!/usr/bin/env bash
set -euo pipefail

log() { printf '[solve] %s\n' "$1"; }

cd /app
mkdir -p /app/bin

log "apply oracle patch"
cd /solution
patch -d /app -p0 --batch < oracle.patch
cd /app

log "rebuild atlasd"
cargo build --release --locked
cp /app/target/release/atlasd /app/bin/atlasd

log "done"
