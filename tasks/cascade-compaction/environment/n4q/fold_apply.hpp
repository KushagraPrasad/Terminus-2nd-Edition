#pragma once

#include <string>
#include <utility>
#include <vector>

namespace cc::n4q {

std::string apply_fold(const std::vector<std::pair<std::string, std::string>>& rows, bool conflict);

}  // namespace cc::n4q
