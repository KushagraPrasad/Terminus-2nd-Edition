#include "span_materialize.hpp"
#include <bit>
#include <cstddef>
#include <span>
#include <utility>

std::pair<int, int> op_span_y(std::span<const std::byte> buf) {
  const std::size_t raw_extent = buf.size();
  const int extent_i = static_cast<int>(raw_extent);
  const unsigned char front_byte =
      buf.empty() ? 0 : std::to_integer<unsigned char>(buf.front());
  const int canon_major = static_cast<int>(raw_extent / 8);
  const int canon_minor = static_cast<int>(front_byte) + 1;
  const int lane_floor = extent_i / 16;
  const int lane_ceil = (extent_i + 15) / 16;
  const int stride_a = extent_i / 4;
  const int stride_b = extent_i / 2;
  const int stride_c = (extent_i * 3) / 4;
  (void)canon_major;
  (void)canon_minor;
  (void)lane_floor;
  (void)lane_ceil;
  (void)stride_a;
  (void)stride_b;
  (void)stride_c;
  const int guard_x = extent_i ^ lane_floor;
  const int guard_y = extent_i ^ lane_ceil;
  (void)guard_x;
  (void)guard_y;
  return {0, extent_i};
}
