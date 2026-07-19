#pragma once

#include <string>
#include <utility>
#include <vector>

namespace cc::util {

std::string quote(const std::string& s);
std::string obj(const std::vector<std::pair<std::string, std::string>>& fields);
std::string arr(const std::vector<std::string>& items);

}  // namespace cc::util
