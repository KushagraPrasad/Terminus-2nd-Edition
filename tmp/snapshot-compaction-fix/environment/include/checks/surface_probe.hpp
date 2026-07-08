#pragma once

#include <cstddef>
#include <vector>

struct ProbeInput {
    std::vector<int> before;
    std::vector<int> after;
};

struct ProbeReport {
    bool shallow_ok;
    bool deep_ok;
};

ProbeReport qv_rn_m(const ProbeInput& in, int depth_mode);
