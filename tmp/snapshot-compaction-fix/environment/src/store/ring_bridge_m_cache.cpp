#include "store/rebind_table.hpp"

#include <vector>

std::vector<int> ring_bridge_m_cache(const EpochSlice& es) {
    std::vector<int> aliases;
    aliases.reserve(es.rows.size());
    for (const auto& row : es.rows) {
        aliases.push_back(row.alias);
    }
    return aliases;
}
