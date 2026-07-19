#include "lane_buffer.hpp"

namespace cc::persist {

int lane_buffer_push(std::vector<int>& lane, int value) {
  lane.push_back(value);
  return static_cast<int>(lane.size());
}

}  // namespace cc::persist
