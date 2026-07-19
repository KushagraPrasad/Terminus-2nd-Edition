#pragma once

#include <string>
#include <vector>

namespace cc::util {

std::string sha256_hex(const std::string& data);
std::string chain_fold(const std::vector<std::string>& parts);

}  // namespace cc::util
