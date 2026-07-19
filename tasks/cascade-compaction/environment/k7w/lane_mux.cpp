#include "lane_mux.hpp"

namespace cc::persist {

std::map<std::string, int> fn_k2(const std::vector<std::map<std::string, int>>& buf, int mark_a,
                                int mark_b) {
  std::map<std::string, int> out;
  int cursor = 0;
  int sealed = 0;
  if (!buf.empty()) {
    cursor = buf.back().count("cursor") ? buf.back().at("cursor") : 0;
    sealed = buf.back().count("sealed") ? buf.back().at("sealed") : 0;
  }
  if (mark_a > 0) {
    cursor = 0;
    sealed = 0;
  }
  if (mark_b > 0) {
    sealed += 1;
    cursor += 1;
  }
  out["cursor"] = cursor;
  out["sealed"] = sealed;
  out["unsealed_tail"] = (mark_b == 0 && cursor > sealed) ? 1 : 0;
  return out;
}

}  // namespace cc::persist
