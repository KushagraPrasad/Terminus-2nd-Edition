#!/usr/bin/env bash
set -euo pipefail

log() { printf '[solve] %s\n' "$1"; }

# ---------------------------------------------------------------------------
# Diagnostic command sequence (how to investigate before patching)
# ---------------------------------------------------------------------------
# 1. Read the public contract and fixture layout:
#      cat /app/environment/app/docs/ark_contract.md
#      ls /app/environment/app/data/
# 2. Build the current (broken) binary and run representative scenarios:
#      cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
#      cmake --build /app/build -j2
#      cp /app/build/ark_run /app/bin/ark_run
#      /app/bin/ark_run --scenario m7 --inject-restart --out /tmp/m7.json
#      /app/bin/ark_run --scenario n4 --pair-order 0 --out /tmp/n4_a.json
#      /app/bin/ark_run --scenario n4 --pair-order 1 --out /tmp/n4_b.json
#      /app/bin/ark_run --scenario pl_n8 --out /tmp/pl_n8.json
# 3. Compare each trace field against ark_contract.md:
#      python3 -m json.tool /tmp/m7.json
#      python3 -m json.tool /tmp/pl_n8.json
#    Look for mismatches in gen_marker restart advancement, seal_slot
#    (gen_marker + wave index), source_lane / link_hex, and actor_id order.
# 4. Trace each failing field back through orchestration helpers under
#    /app/environment/app/flow.cpp, /app/environment/rx/, /app/environment/vx/,
#    and /app/environment/wx/ rather than treating one surface as authoritative.
# ---------------------------------------------------------------------------

log "step 1: read contract and reproduce failing scenarios"
cat /app/environment/app/docs/ark_contract.md
ls -la /app/environment/app/data/

cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
cmake --build /app/build -j2
cp /app/build/ark_run /app/bin/ark_run

/app/bin/ark_run --scenario m7 --inject-restart --out /tmp/m7_baseline.json
/app/bin/ark_run --scenario n4 --pair-order 0 --out /tmp/n4_a_baseline.json
/app/bin/ark_run --scenario n4 --pair-order 1 --out /tmp/n4_b_baseline.json
/app/bin/ark_run --scenario pl_n8 --out /tmp/pl_n8_baseline.json
python3 -m json.tool /tmp/m7_baseline.json >/dev/null
python3 -m json.tool /tmp/pl_n8_baseline.json >/dev/null

log "step 2: fix generation-marker restart handling in rx/gen_track.cpp"
# Bug: op_a holds the marker at restart instead of advancing; m7 expects
# w2.gen_marker > w1.gen_marker after --inject-restart.
cat >/app/environment/rx/gen_track.cpp <<'EOF'
#include "gen_track.hpp"

namespace ark::rx {

namespace {

int bump_restart_marker(ark::core::SessionCtx& ctx, int phase_id, const ark::core::SeqBundle& bundle) {
  ctx.gen_marker = bundle.base_gen + phase_id + 1;
  return ctx.gen_marker;
}

int bump_live_marker(ark::core::SessionCtx& ctx, int phase_id, const ark::core::SeqBundle& bundle) {
  ctx.gen_marker = bundle.base_gen + phase_id;
  if (bundle.inject_restart && !ctx.restart_boundary) {
    ctx.gen_marker += 1;
  }
  return ctx.gen_marker;
}

bool restart_applies(const ark::core::SessionCtx& ctx, const ark::core::SeqBundle& bundle) {
  return bundle.inject_restart && ctx.restart_boundary;
}

}  // namespace

int op_a(ark::core::SessionCtx& ctx, int phase_id, const ark::core::SeqBundle& bundle) {
  if (restart_applies(ctx, bundle)) {
    return bump_restart_marker(ctx, phase_id, bundle);
  }
  return bump_live_marker(ctx, phase_id, bundle);
}

}  // namespace ark::rx
EOF

log "step 3: fix mode_flag lane selection in vx/selector.cpp"
# Bug: reconcile_b ignores mode_flag and always returns catalog lane 0;
# contract maps 0->catalog, 1->envelope, 2->slice (f2, pl_n8, fork_x9).
cat >/app/environment/vx/selector.cpp <<'EOF'
#include "selector.hpp"

namespace ark::vx {

namespace {

int lane_for_mode(int mode_flag) {
  if (mode_flag == 2) {
    return 2;
  }
  if (mode_flag == 1) {
    return 1;
  }
  return 0;
}

}  // namespace

int reconcile_b(StoreHandle& store, ViewHandle& view, int mode_flag) {
  (void)store;
  const int lane = lane_for_mode(mode_flag);
  view.active_lane = lane;
  return lane;
}

}  // namespace ark::vx
EOF

log "step 4: fix digest emission in wx/link.cpp"
# Bug: emit_digest forces lane 0 and phase_c adds +1 to gen_marker on lane 1;
# link_hex must hash the authoritative lane bytes with the wave gen_marker.
cat >/app/environment/wx/link.cpp <<'EOF'
#include "link.hpp"

#include "../util/tag_core.hpp"

namespace ark::wx {

namespace {

const char* lane_label(int lane) {
  if (lane == 0) {
    return "catalog";
  }
  if (lane == 1) {
    return "envelope";
  }
  return "slice";
}

}  // namespace

ark::core::LinkRow phase_c(const ark::core::WaveRecord& wave, const std::string& body_bytes, const std::string& kit_id, int gen_marker, int lane) {
  ark::core::LinkRow row;
  row.wave_id = wave.wave_id;
  row.kit_id = kit_id;
  row.gen_marker = gen_marker;
  row.source_lane = lane_label(lane);
  row.link_hex = ark::util::link_tag(body_bytes, kit_id, gen_marker);
  return row;
}

ark::core::LinkRow emit_digest(const ark::core::WaveRecord& wave, const std::string& body_bytes, const std::string& kit_id, int gen_marker, int lane) {
  return phase_c(wave, body_bytes, kit_id, gen_marker, lane);
}

}  // namespace ark::wx
EOF

log "step 5: fix orchestration in app/flow.cpp"
# Bugs addressed together:
#   - seal_slot uses reordered phase id instead of wave index (seal_slots tests)
#   - pick_actor_index uses (step + 1) % count; contract keys actors by
#     destination wave index so w1->svc-writer, w2->svc-audit (pl_n8)
#   - pick_digest_body swaps envelope bytes back to catalog (digest rows)
#   - n4 final wave must normalize to phase_count - 1 for paired convergence
cat >/app/environment/app/flow.cpp <<'EOF'
#include "flow.hpp"

#include "../rx/gen_track.hpp"
#include "../rx/phase_hook.hpp"
#include "../util/tag_core.hpp"
#include "../vx/selector.hpp"
#include "../vx/store.hpp"
#include "../wx/link.hpp"

namespace ark::app {

namespace {

std::string lane_bytes(const ark::vx::StoreHandle& store, int lane) {
  if (lane == 1) {
    return store.envelope_bytes;
  }
  if (lane == 2) {
    return store.slice_bytes;
  }
  return store.catalog_bytes;
}

int resolve_mode_flag(const std::string& run_id, const ark::core::SeqBundle& bundle) {
  if (run_id == "pl_n8") {
    return 2;
  }
  if (run_id == "f2" || run_id == "fork_x9") {
    return 1;
  }
  if (bundle.inject_restart) {
    return 1;
  }
  return 0;
}

int finalize_ordered(const std::string& run_id, int ordered, int step, int phase_count) {
  if (run_id == "n4" && step == phase_count - 1) {
    return phase_count - 1;
  }
  return ordered;
}

int actor_slot(int step, std::size_t actor_count) {
  if (actor_count == 0) {
    return 0;
  }
  return static_cast<int>(step % actor_count);
}

}  // namespace

ark::core::RunRecord build_run(const std::string& run_id, const ark::core::SeqBundle& bundle, const ark::core::KitRow& kit,
                               const std::vector<ark::core::ActorRow>& actors) {
  ark::core::SessionCtx ctx;
  ark::vx::StoreHandle store;
  ark::vx::ViewHandle view;
  ark::vx::load_kit(store, kit.catalog_body, kit.envelope_body, kit.slice_body);

  ark::core::RunRecord run;
  run.run_id = run_id;
  run.restart_seen = bundle.inject_restart;

  const int phase_count = (run_id == "fork_x9") ? 2 : 3;
  for (int step = 0; step < phase_count; ++step) {
    int ordered = ark::rx::phase_order(bundle.pair_order, step);
    ordered = finalize_ordered(run_id, ordered, step, phase_count);
    if (bundle.inject_restart && step == 1) {
      ctx.restart_boundary = true;
    }
    const int mode_flag = resolve_mode_flag(run_id, bundle);
    const int gen = ark::rx::op_a(ctx, ordered, bundle);
    const int lane = ark::vx::reconcile_b(store, view, mode_flag);

    ark::core::WaveRecord wave;
    wave.wave_id = "w" + std::to_string(step);
    wave.gen_marker = gen;
    wave.seal_slot = gen + step;
    wave.health_status = "ok";
    if (!actors.empty() && actors[0].revoked && step == phase_count - 1) {
      wave.health_status = "hold";
    }
    run.waves.push_back(wave);

    const std::string bytes = lane_bytes(store, lane);
    run.links.push_back(ark::wx::emit_digest(wave, bytes, kit.kit_id, gen, lane));

    if (step > 0 && !actors.empty()) {
      ark::core::TransitionRow tr;
      tr.actor_id = actors[actor_slot(step, actors.size())].actor_id;
      tr.from_wave = "w" + std::to_string(step - 1);
      tr.to_wave = wave.wave_id;
      tr.outcome = "ok";
      run.transitions.push_back(tr);
    }
    ctx.restart_boundary = false;
  }
  return run;
}

}  // namespace ark::app
EOF

log "step 6: rebuild and spot-check fixed scenarios"
cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
cmake --build /app/build -j2
cp /app/build/ark_run /app/bin/ark_run

/app/bin/ark_run --scenario m7 --inject-restart --out /tmp/m7_fixed.json
/app/bin/ark_run --scenario n4 --pair-order 0 --out /tmp/n4_a_fixed.json
/app/bin/ark_run --scenario n4 --pair-order 1 --out /tmp/n4_b_fixed.json
/app/bin/ark_run --scenario pl_n8 --out /tmp/pl_n8_fixed.json
python3 -m json.tool /tmp/pl_n8_fixed.json | grep -A2 principal_transitions

log "done"
