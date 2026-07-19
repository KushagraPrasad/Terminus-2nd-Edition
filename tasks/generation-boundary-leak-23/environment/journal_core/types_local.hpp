#pragma once
#include <cstdint>
#include <vector>

namespace qgh::types {
void write_u64_le(std::vector<std::uint8_t>& dst, std::size_t offset, std::uint64_t v);
std::uint64_t read_u64_le(const std::vector<std::uint8_t>& src, std::size_t offset);
}  // namespace qgh::types
