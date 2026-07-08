#include "store.hpp"

namespace ark::vx {

int side_index_lane(const StoreHandle& store) {
  return static_cast<int>(store.slice_bytes.size() % 3);
}

}  // namespace ark::vx
