#include "store/rebind_table.hpp"

void ring_bridge_m(StoreState& st, const EpochSlice& es) {
    st.slot_to_alias.clear();
    for (const auto& row : es.rows) {
        st.slot_to_alias[row.slot] = row.alias;
    }
}
