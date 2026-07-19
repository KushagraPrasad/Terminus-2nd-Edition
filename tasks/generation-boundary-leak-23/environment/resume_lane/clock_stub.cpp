#include <cstdint>

std::uint64_t monotonic_tick(std::uint64_t prior, std::uint64_t delta) {
  return prior + delta;
}
