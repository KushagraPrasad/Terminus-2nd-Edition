#pragma once

#include <string>
#include <vector>

namespace cb::util {

std::string quote(const std::string& value);
std::string arr(const std::vector<std::string>& items);
std::string obj(const std::vector<std::pair<std::string, std::string>>& fields);

}  // namespace cb::util
