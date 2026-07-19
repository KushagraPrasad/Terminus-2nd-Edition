#!/usr/bin/env bash
set -euo pipefail

cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
cmake --build /app/build -j2
install -m 0755 /app/build/cycle_run /app/bin/cycle_run
exec /app/bin/cycle_run "$@"
