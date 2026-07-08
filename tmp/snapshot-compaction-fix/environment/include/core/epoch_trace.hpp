#pragma once

#include <cstdint>
#include <vector>

struct SpanBatch {
    std::vector<int> values;
};

struct EpochStamp {
    uint64_t checksum;
    bool monotone;
};

EpochStamp trace_mux_c(const SpanBatch& sb, uint32_t turn_id);
