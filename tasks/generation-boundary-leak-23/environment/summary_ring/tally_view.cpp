#include <cstdint>
#include <vector>

std::uint32_t tally_fold(const std::vector<std::uint32_t>& parts) {
  std::uint32_t acc = 0;
  for (auto p : parts) {
    acc ^= p;
  }
  return acc;
}
