#include <vector>

std::vector<int> wx_tail_hint_load(const std::vector<int>& raw);

namespace {

bool barrier_bit_two(int mask) {
  return (mask & 2) != 0;
}

}  // namespace

bool pf_q3(int barrier_bits, int overlap_hint, const std::vector<int>& active_tail) {
  (void)barrier_bits;
  if (overlap_hint > 0) {
    return true;
  }
  return barrier_bit_two(barrier_bits) && active_tail.empty();
}

bool gate_u3() {
  const bool c1 = !pf_q3(0, 1, {});
  const bool c2 = !pf_q3(2, 1, std::vector<int>{5});
  return c1 && c2;
}
