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

std::string pick_digest_body(const ark::vx::StoreHandle& store, int lane, const std::string& bytes) {
  if (lane == 1) {
    return store.catalog_bytes;
  }
  return bytes;
}

int pick_actor_index(int step, std::size_t actor_count) {
  if (actor_count == 0) {
    return 0;
  }
  return static_cast<int>((step + 1) % actor_count);
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
    if (bundle.inject_restart && step == 1) {
      ctx.restart_boundary = true;
    }
    int mode_flag = 0;
    if (run_id == "pl_n8") {
      mode_flag = 2;
    } else if (run_id == "f2" || run_id == "fork_x9") {
      mode_flag = 1;
    } else if (bundle.inject_restart) {
      mode_flag = 1;
    }
    const int gen = ark::rx::op_a(ctx, ordered, bundle);
    const int lane = ark::vx::reconcile_b(store, view, mode_flag);

    ark::core::WaveRecord wave;
    wave.wave_id = "w" + std::to_string(step);
    wave.gen_marker = gen;
    wave.seal_slot = gen + ordered;
    wave.health_status = "ok";
    if (!actors.empty() && actors[0].revoked && step == phase_count - 1) {
      wave.health_status = "hold";
    }
    run.waves.push_back(wave);

    const std::string bytes = lane_bytes(store, lane);
    const std::string link_body = pick_digest_body(store, lane, bytes);
    run.links.push_back(ark::wx::emit_digest(wave, link_body, kit.kit_id, gen, lane));

    if (step > 0 && !actors.empty()) {
      ark::core::TransitionRow tr;
      tr.actor_id = actors[pick_actor_index(step, actors.size())].actor_id;
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
