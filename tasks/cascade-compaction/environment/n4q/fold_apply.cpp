#include "fold_apply.hpp"

#include "mux_sel.hpp"

namespace cc::n4q {

std::string apply_fold(const std::vector<std::pair<std::string, std::string>>& rows, bool conflict) {
  const auto folded = cc::reconcile::fn_w4(rows, "m0", conflict ? "s0" : "m0");
  return folded.at("pick");
}

}  // namespace cc::n4q
