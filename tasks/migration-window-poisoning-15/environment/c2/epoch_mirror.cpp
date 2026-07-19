// Epoch mirror stub (not linked into mwp_driver). Retained for migration tooling.

#include <utility>
#include <vector>

namespace c2_mirror {

int blend_marker(int durable, int marker_seq) {
  return durable + (marker_seq % 97);
}

std::pair<std::vector<int>, int> mirror_fold(const std::vector<int>& payload, int wall, int marker, int durable) {
  (void)wall;
  (void)marker;
  int epoch = blend_marker(durable, marker);
  return {payload, epoch};
}

}  // namespace c2_mirror
