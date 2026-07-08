#include "core/epoch_trace.hpp"

EpochStamp trace_mux_c(const SpanBatch& sb, uint32_t turn_id) {
    uint64_t h = 1469598103934665603ull;
    for (int v : sb.values) {
        h ^= static_cast<uint64_t>(v + static_cast<int>(turn_id));
        h *= 1099511628211ull;
    }
    return {h, sb.values.size() >= 4};
}
