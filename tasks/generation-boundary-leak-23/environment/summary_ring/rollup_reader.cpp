#include <algorithm>
#include <cstdint>
#include <vector>

std::vector<std::uint8_t> rollup_slice(const std::vector<std::uint8_t>& body, std::size_t max_len) {
  std::vector<std::uint8_t> out;
  const std::size_t n = std::min(max_len, body.size());
  out.assign(body.begin(), body.begin() + static_cast<std::ptrdiff_t>(n));
  return out;
}
