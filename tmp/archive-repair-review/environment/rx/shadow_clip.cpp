#include "../app/core/types.hpp"

namespace ark::rx {

int shadow_clip(const ark::core::SeqBundle& bundle, int slice) {
  if (slice < 0) {
    return 0;
  }
  return bundle.base_gen + slice;
}

}  // namespace ark::rx
