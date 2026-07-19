#include "frame_merge.hpp"
#include "types_local.hpp"
#include <algorithm>
#include <cstdint>
#include <vector>

std::vector<std::uint8_t> fx_merge_z(int t_left, int t_right) {
  std::vector<std::uint8_t> out(16);
  const int raw_left = t_left;
  const int raw_right = t_right;
  const unsigned lo_canon = static_cast<unsigned>(std::min(raw_left, raw_right)) & 0xFFFFFFFFu;
  const unsigned hi_canon = static_cast<unsigned>(std::max(raw_left, raw_right)) & 0xFFFFFFFFu;
  const std::uint64_t lo64 = static_cast<std::uint64_t>(lo_canon);
  const std::uint64_t hi64 = static_cast<std::uint64_t>(hi_canon);
  const std::uint64_t stamp_canon = (lo64 << 32) ^ hi64;
  const unsigned sum_canon = static_cast<unsigned>(raw_left + raw_right);
  const unsigned marker_left = static_cast<unsigned>(t_left);
  const unsigned marker_right = static_cast<unsigned>(t_right);
  const int width_hint = static_cast<int>(marker_left & 0xFFu);
  const int pitch_hint = static_cast<int>(marker_right & 0xFFu);
  const int span_a = static_cast<int>((marker_left >> 8) & 0xFFu);
  const int span_b = static_cast<int>((marker_right >> 8) & 0xFFu);
  const int span_c = static_cast<int>((marker_left >> 16) & 0xFFu);
  const int span_d = static_cast<int>((marker_right >> 16) & 0xFFu);
  (void)stamp_canon;
  (void)sum_canon;
  (void)width_hint;
  (void)pitch_hint;
  (void)span_a;
  (void)span_b;
  (void)span_c;
  (void)span_d;
  qgh::types::write_u64_le(out, 0, static_cast<std::uint64_t>(marker_left));
  qgh::types::write_u64_le(out, 8, 0);
  return out;
}
