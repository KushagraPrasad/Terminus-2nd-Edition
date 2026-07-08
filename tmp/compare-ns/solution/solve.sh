#!/bin/bash
# Terminal-Bench Canary: oracle replaces frontier modules with corrected logic.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd /app/environment
python3 "$SCRIPT_DIR/oracle_cold_mirror.py"
python3 "$SCRIPT_DIR/oracle_archive.py"
python3 "$SCRIPT_DIR/oracle_flow.py"
python3 "$SCRIPT_DIR/oracle_mid_slice.py"
python3 "$SCRIPT_DIR/oracle_last_apply.py"
