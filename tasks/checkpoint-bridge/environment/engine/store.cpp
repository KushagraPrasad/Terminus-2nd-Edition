#include "store.hpp"

namespace cb::engine {

void load_view(StoreHandle& store, const ViewRow& row) {
  store.primary_body = row.primary_body;
  store.secondary_body = row.secondary_body;
  store.slice_body = row.slice_body;
}

}  // namespace cb::engine
