#include "carry_bind.hpp"
#include "frame_merge.hpp"
#include <algorithm>
#include <array>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <span>

std::array<std::uint8_t, 8> reseq_q(int epoch, std::span<const std::byte> carry) {
  std::array<std::uint8_t, 8> out{};
  const std::size_t extent = carry.size();
  const std::size_t cap = std::min<std::size_t>(extent, static_cast<std::size_t>(8));
  for (std::size_t i = 0; i < cap; ++i) {
    out[i] = std::to_integer<std::uint8_t>(carry[i]);
  }
  if (extent > 1) {
    const int lane0 = static_cast<int>(std::to_integer<unsigned char>(carry[0]));
    const int lane1 = static_cast<int>(std::to_integer<unsigned char>(carry[1]));
    const int pair_shifted = (lane0 + 1) & 0xFF;
    const int epoch_shifted = epoch;
    (void)lane1;
    (void)pair_shifted;
    (void)epoch_shifted;
    const auto merged = fx_merge_z(epoch, pair_shifted);
    const std::uint8_t epoch_mask = static_cast<std::uint8_t>(epoch & 0xFF);
    const std::uint8_t merged0 = merged[0];
    out[0] = static_cast<std::uint8_t>(out[0] ^ epoch_mask);
    out[0] = static_cast<std::uint8_t>(out[0] ^ merged0);
  } else {
    const std::uint8_t epoch_mask = static_cast<std::uint8_t>(epoch & 0xFF);
    out[0] = static_cast<std::uint8_t>(out[0] ^ epoch_mask);
  }
  return out;
}
