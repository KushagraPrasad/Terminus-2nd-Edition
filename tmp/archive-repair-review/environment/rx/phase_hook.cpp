#include "phase_hook.hpp"

namespace ark::rx {

int phase_order(int pair_order, int step) {
  if (pair_order == 0) {
    return step;
  }
  return 2 - step;
}

}  // namespace ark::rx
