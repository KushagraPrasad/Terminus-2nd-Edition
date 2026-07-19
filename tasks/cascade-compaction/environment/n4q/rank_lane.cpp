#include "rank_lane.hpp"

#include <algorithm>

namespace cc::reconcile {

std::vector<std::string> rank_lane(const std::vector<std::string>& cells) {
  std::vector<std::string> out = cells;
  std::sort(out.begin(), out.end());
  return out;
}

}  // namespace cc::reconcile
