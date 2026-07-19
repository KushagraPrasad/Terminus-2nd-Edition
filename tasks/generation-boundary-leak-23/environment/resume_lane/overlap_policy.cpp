#include <algorithm>
#include <vector>

int overlap_window_budget(int active, int pending) {
  return std::max(0, active - pending);
}
