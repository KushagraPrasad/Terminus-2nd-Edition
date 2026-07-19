#include "flow.hpp"

#include "../c7k/p1m.hpp"
#include "../engine/phase_hook.hpp"
#include "../engine/store.hpp"
#include "../m2p/q4n.hpp"
#include "../w9n/s2t.hpp"

namespace cb::driver {

namespace {

std::string lane_bytes(const engine::StoreHandle& store, int lane) {
  if (lane == 1) {
    return store.secondary_body;
  }
  if (lane == 2) {
    return store.slice_body;
  }
  return store.primary_body;
}

}  // namespace

engine::RunRecord build_run(const std::string& run_id, const engine::SeqBundle& bundle, const engine::ViewRow& view) {
  engine::SessionCtx ctx;
  engine::StoreHandle store;
  engine::ViewHandle acct;
  engine::load_view(store, view);

  engine::RunRecord run;
  run.run_id = run_id;
  run.restart_seen = bundle.inject_restart;

  const int phase_count = (run_id == "fork") ? 2 : 3;
  for (int step = 0; step < phase_count; ++step) {
    int ordered = engine::phase_order(bundle.pair_order, step);
    if (run_id == "beta" && step == phase_count - 1) {
      ordered = phase_count - 1;
    }
    if (bundle.inject_restart && step == 1) {
      ctx.restart_boundary = true;
    }
    int mode_flag = 0;
    if (run_id == "overlap") {
      mode_flag = 2;
    } else if (run_id == "digest" || run_id == "fork") {
      mode_flag = 1;
    } else if (bundle.inject_restart) {
      mode_flag = 1;
    }
    const int gen = cb::c7k::fn_k3(ctx, ordered, bundle.base_gen, bundle.inject_restart);
    const int lane = cb::m2p::fn_r8(store, acct, mode_flag);

    engine::WaveRow wave;
    wave.wave_id = "w" + std::to_string(step);
    wave.gen_marker = gen;
    wave.seal_slot = gen + ordered;
    wave.health_status = "ok";
    run.waves.push_back(wave);

    const std::string bytes = lane_bytes(store, lane);
    const std::string span_base = (lane == 1) ? store.primary_body : bytes;
    run.spans.push_back(cb::w9n::emit_span(wave, span_base, view.view_id, lane));

    ctx.restart_boundary = false;
  }
  return run;
}

}  // namespace cb::driver
