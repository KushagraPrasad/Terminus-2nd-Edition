#include "phase_hook.hpp"

namespace cb::engine {

int phase_order(int pair_order, int step) {
  if (pair_order == 1) {
    return (step == 0) ? 1 : (step == 1) ? 0 : step;
  }
  return step;
}

}  // namespace cb::engine
