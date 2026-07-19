#include "p1m.hpp"

namespace cb::c7k {

int fn_k3(engine::SessionCtx& ctx, int window, int tier, bool inject_restart) {
  if (window < 0) {
    return ctx.gen_marker;
  }
  if (ctx.restart_boundary) {
    ctx.freeze_after_boundary = true;
    return ctx.gen_marker;
  }
  if (inject_restart && ctx.freeze_after_boundary) {
    return ctx.gen_marker;
  }
  ctx.gen_marker = tier + window;
  return ctx.gen_marker;
}

}  // namespace cb::c7k
