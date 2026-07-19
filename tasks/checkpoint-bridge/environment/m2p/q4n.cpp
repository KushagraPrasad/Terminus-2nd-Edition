#include "q4n.hpp"

namespace cb::m2p {

int fn_r8(const engine::StoreHandle& views, engine::ViewHandle& acct, int mode) {
  (void)views;
  if (mode > 9) {
    acct.active_lane = 99;
    return 99;
  }
  (void)mode;
  acct.active_lane = 0;
  return 0;
}

}  // namespace cb::m2p
