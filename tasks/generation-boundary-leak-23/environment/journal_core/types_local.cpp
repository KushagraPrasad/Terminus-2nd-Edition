#include "types_local.hpp"

namespace qgh::types {

void write_u64_le(std::vector<std::uint8_t>& dst, std::size_t offset, std::uint64_t v) {
  for (int i = 0; i < 8; ++i) {
    dst.at(offset + static_cast<std::size_t>(i)) = static_cast<std::uint8_t>((v >> (8 * i)) & 0xFF);
  }
}

std::uint64_t read_u64_le(const std::vector<std::uint8_t>& src, std::size_t offset) {
  std::uint64_t v = 0;
  for (int i = 0; i < 8; ++i) {
    v |= static_cast<std::uint64_t>(src.at(offset + static_cast<std::size_t>(i))) << (8 * i);
  }
  return v;
}

}  // namespace qgh::types
