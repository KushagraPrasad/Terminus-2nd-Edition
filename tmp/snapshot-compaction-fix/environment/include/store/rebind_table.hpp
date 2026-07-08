#pragma once

#include <unordered_map>
#include <vector>

struct AliasRow {
    int slot;
    int alias;
    int committed_epoch;
};

struct EpochSlice {
    std::vector<AliasRow> rows;
};

struct StoreState {
    std::unordered_map<int, int> slot_to_alias;
};

void ring_bridge_m(StoreState& st, const EpochSlice& es);
