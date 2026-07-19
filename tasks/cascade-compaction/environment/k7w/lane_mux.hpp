#pragma once

#include <map>
#include <string>
#include <vector>

namespace cc::persist {

std::map<std::string, int> fn_k2(const std::vector<std::map<std::string, int>>& buf, int mark_a,
                                int mark_b);

}  // namespace cc::persist
