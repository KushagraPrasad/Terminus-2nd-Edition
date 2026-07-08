#include "selector.hpp"

namespace ark::vx {

namespace {

int pinned_lane() {
  return 0;
}

int catalog_lane() {
  return 0;
}

}  // namespace

int reconcile_b(StoreHandle& store, ViewHandle& view, int mode_flag) {
  (void)store;
  (void)mode_flag;
  const int lane = catalog_lane();
  view.active_lane = pinned_lane();
  return lane;
}

}  // namespace ark::vx
