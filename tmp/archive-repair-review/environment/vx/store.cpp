#include "store.hpp"

namespace ark::vx {

void load_kit(StoreHandle& store, const std::string& catalog, const std::string& envelope, const std::string& slice) {
  store.catalog_bytes = catalog;
  store.envelope_bytes = envelope;
  store.slice_bytes = slice;
}

}  // namespace ark::vx
