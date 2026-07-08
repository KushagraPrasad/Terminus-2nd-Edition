#pragma once

#include "core/epoch_trace.hpp"
#include <vector>

bool scan_anchor_chain(const EpochStamp& stamp);
bool zz_mix_n(const std::vector<int>& before, const std::vector<int>& after, int depth_mode);
