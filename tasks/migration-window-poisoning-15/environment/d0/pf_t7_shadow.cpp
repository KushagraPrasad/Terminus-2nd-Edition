#include <cstdint>
#include <vector>

int pf_t7_shadow(const std::vector<std::uint8_t>& a, const std::vector<std::uint8_t>& b) {
  int x = 0;
  const std::size_t n = a.size() < b.size() ? a.size() : b.size();
  for (std::size_t i = 0; i < n; ++i) {
    x ^= static_cast<int>(a[i] ^ b[i]);
  }
  return x;
}
