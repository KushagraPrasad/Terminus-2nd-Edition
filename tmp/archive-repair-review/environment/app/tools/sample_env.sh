#!/usr/bin/env bash
set -euo pipefail
export PATH="/app/bin:${PATH}"
ark_run --scenario m7 --out /tmp/sample.json
