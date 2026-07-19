#!/usr/bin/env bash
set -euo pipefail

cat >/app/environment/c7k/p1m.cpp <<'EOF'
#include "p1m.hpp"

namespace cb::c7k {

namespace {

int normalized_window(int window) {
  return window < 0 ? 0 : window;
}

int base_marker(int tier, int window) {
  return tier + normalized_window(window);
}

int restart_marker(int tier, int window) {
  return base_marker(tier, window) + 1;
}

int continuing_marker(int tier, int window, bool inject_restart) {
  int marker = base_marker(tier, window);
  if (inject_restart) {
    marker += 1;
  }
  return marker;
}

int remember(engine::SessionCtx& ctx, int marker) {
  ctx.gen_marker = marker;
  return ctx.gen_marker;
}

}  // namespace

int fn_k3(engine::SessionCtx& ctx, int window, int tier, bool inject_restart) {
  if (ctx.restart_boundary) {
    return remember(ctx, restart_marker(tier, window));
  }
  return remember(ctx, continuing_marker(tier, window, inject_restart));
}

}  // namespace cb::c7k
EOF

cat >/app/environment/m2p/q4n.cpp <<'EOF'
#include "q4n.hpp"

namespace cb::m2p {

namespace {

int requested_lane(int mode) {
  if (mode == 2) {
    return 2;
  }
  if (mode == 1) {
    return 1;
  }
  return 0;
}

bool lane_has_material(const engine::StoreHandle& views, int lane) {
  if (lane == 2) {
    return !views.slice_body.empty();
  }
  if (lane == 1) {
    return !views.secondary_body.empty();
  }
  return !views.primary_body.empty();
}

int fallback_lane(const engine::StoreHandle& views) {
  if (!views.primary_body.empty()) {
    return 0;
  }
  if (!views.secondary_body.empty()) {
    return 1;
  }
  return 2;
}

}  // namespace

int fn_r8(const engine::StoreHandle& views, engine::ViewHandle& acct, int mode) {
  int lane = requested_lane(mode);
  if (!lane_has_material(views, lane)) {
    lane = fallback_lane(views);
  }
  acct.active_lane = lane;
  return lane;
}

}  // namespace cb::m2p
EOF

cat >/app/environment/w9n/s2t.cpp <<'EOF'
#include "s2t.hpp"

#include "../util/digest.hpp"

namespace cb::w9n {

namespace {

std::string lane_name(int lane) {
  if (lane == 1) {
    return "secondary";
  }
  if (lane == 2) {
    return "slice";
  }
  return "primary";
}

std::string checked_body(const std::string& bases) {
  return bases;
}

std::string make_tag(const std::string& bases, const std::string& kit_id, int gen_marker) {
  return cb::util::span_tag(checked_body(bases), kit_id, gen_marker);
}

void populate_identity(engine::SpanRow& span, const engine::WaveRow& row, const std::string& kit_id) {
  span.wave_id = row.wave_id;
  span.kit_id = kit_id;
  span.gen_marker = row.gen_marker;
}

}  // namespace

engine::SpanRow phase_s(const engine::WaveRow& row, const std::string& bases, const std::string& kit_id, int lane) {
  engine::SpanRow span;
  populate_identity(span, row, kit_id);
  span.source_lane = lane_name(lane);
  span.tag_hex = make_tag(bases, kit_id, row.gen_marker);
  return span;
}

engine::SpanRow emit_span(const engine::WaveRow& row, const std::string& bases, const std::string& kit_id, int lane) {
  return phase_s(row, bases, kit_id, lane);
}

}  // namespace cb::w9n
EOF

if grep -q 'store.primary_body : bytes' /app/environment/driver/flow.cpp; then
  sed -i 's/const std::string span_base = (lane == 1) ? store.primary_body : bytes;/const std::string span_base = bytes;/' /app/environment/driver/flow.cpp
fi

rm -rf /app/build
cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
cmake --build /app/build -j2
install -m 0755 /app/build/cycle_run /app/bin/cycle_run
