#pragma once

#include <string>

namespace ark::vx {

struct StoreHandle {
  std::string catalog_bytes;
  std::string envelope_bytes;
  std::string slice_bytes;
};

struct ViewHandle {
  int active_lane = 0;
};

void load_kit(StoreHandle& store, const std::string& catalog, const std::string& envelope, const std::string& slice);

}  // namespace ark::vx
