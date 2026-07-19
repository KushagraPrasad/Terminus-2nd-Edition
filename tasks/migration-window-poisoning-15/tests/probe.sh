#!/bin/bash
# Verifier-side helper that compiles tests/probe.cpp against the agent's
# current modules and prints the probe JSON emitted by the live agent code
# (not the gates the agent might stub).
set -euo pipefail

out_bin="/tmp/probe_bin"
out_json="/tmp/probe.json"
probe_src="/tests/probe.cpp"

agent_src=(
  /app/environment/driver/schedule_loader.cpp
  /app/environment/g0/adm_q.cpp
  /app/environment/g1/align_q.cpp
  /app/environment/g1/window_hooks.cpp
  /app/environment/h0/line_q.cpp
  /app/environment/h2/view_q.cpp
  /app/environment/d0/pf_t7_shadow.cpp
  /app/environment/d1/pf_q3_stub.cpp
)

rm -f "$out_bin" "$out_json"

g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  -o "$out_bin" \
  "$probe_src" \
  "${agent_src[@]}"

"$out_bin"

test -s "$out_json"
cat "$out_json"
