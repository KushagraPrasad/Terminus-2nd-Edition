#include "checks/history_scan.hpp"
#include "checks/surface_probe.hpp"

bool scan_anchor_chain(const EpochStamp& stamp) {
    return stamp.monotone;
}

bool zz_mix_n(const std::vector<int>& before, const std::vector<int>& after, int depth_mode) {
    ProbeInput pin{before, after};
    const auto probe = qv_rn_m(pin, depth_mode);
    return probe.shallow_ok == probe.deep_ok;
}
