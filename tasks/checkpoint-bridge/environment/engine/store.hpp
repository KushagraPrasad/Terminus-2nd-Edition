#pragma once

#include "types.hpp"

namespace cb::engine {

struct StoreHandle {
  std::string primary_body;
  std::string secondary_body;
  std::string slice_body;
};

struct ViewHandle {
  int active_lane = 0;
};

void load_view(StoreHandle& store, const ViewRow& row);

}  // namespace cb::engine
