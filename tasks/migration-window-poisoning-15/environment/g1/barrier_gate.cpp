// Alternate overlap gate experiment (not linked into mwp_driver).

#include <vector>

bool bg_quiet(int barrier_bits, int overlap_hint, const std::vector<int>& active_tail) {
  (void)overlap_hint;
  return (barrier_bits & 1) != 0 && active_tail.empty();
}
