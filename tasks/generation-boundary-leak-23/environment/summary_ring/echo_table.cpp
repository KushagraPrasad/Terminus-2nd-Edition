#include <algorithm>
#include <cstdint>
#include <string>

std::string echo_hex_preview(const std::uint8_t* data, std::size_t len) {
  std::string s;
  const std::size_t cap = std::min(len, static_cast<std::size_t>(8));
  static const char* hex = "0123456789abcdef";
  for (std::size_t i = 0; i < cap; ++i) {
    s.push_back(hex[(data[i] >> 4) & 0xF]);
    s.push_back(hex[data[i] & 0xF]);
  }
  return s;
}
