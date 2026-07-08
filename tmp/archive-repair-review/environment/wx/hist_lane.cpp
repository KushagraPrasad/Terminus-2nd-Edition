#include "../app/core/types.hpp"

namespace ark::wx {

int hist_lane_write(const ark::core::RunRecord& run) {
  return static_cast<int>(run.waves.size());
}

}  // namespace ark::wx
