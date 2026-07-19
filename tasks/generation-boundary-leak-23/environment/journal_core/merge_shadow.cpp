#include <cstddef>
#include <cstdint>

// Metrics-only canary diff; not used by the replay pipeline.
int shadow_metric_delta(const std::uint8_t* a, const std::uint8_t* b, std::size_t len) {
  int acc = 0;
  for (std::size_t i = 0; i < len; ++i) {
    acc += static_cast<int>(a[i] ^ b[i]);
  }
  return acc;
}
