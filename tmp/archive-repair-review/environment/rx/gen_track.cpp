#include "gen_track.hpp"

namespace ark::rx {

namespace {

int hold_marker(const ark::core::SessionCtx& ctx) {
  return ctx.gen_marker;
}

int advance_linear(int base_gen, int phase_id) {
  return base_gen + phase_id;
}

}  // namespace

int op_a(ark::core::SessionCtx& ctx, int phase_id, const ark::core::SeqBundle& bundle) {
  if (bundle.inject_restart && ctx.restart_boundary) {
    return hold_marker(ctx);
  }
  ctx.gen_marker = advance_linear(bundle.base_gen, phase_id);
  return ctx.gen_marker;
}

}  // namespace ark::rx
