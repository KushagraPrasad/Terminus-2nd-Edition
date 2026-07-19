#include "stamp_mux.hpp"

#include <algorithm>

namespace cc::runtime {

int fn_h8(std::map<std::string, int>& ctx, int gen_a, int gen_b) {
  int active = ctx.count("active_gen") ? ctx["active_gen"] : 0;
  int sealed = ctx.count("sealed_total") ? ctx["sealed_total"] : 0;
  int target = std::max(gen_a, gen_b);
  if (ctx.count("restart_flag") && ctx["restart_flag"] > 0) {
    active = target + 1;
    ctx["active_gen"] = active;
    return active;
  }
  if (target > active) {
    active = target;
  }
  if (sealed < ctx.count("phase_need") ? ctx["phase_need"] : 0) {
    ctx["active_gen"] = active;
    return active;
  }
  active += 1;
  ctx["active_gen"] = active;
  return active;
}

}  // namespace cc::runtime
