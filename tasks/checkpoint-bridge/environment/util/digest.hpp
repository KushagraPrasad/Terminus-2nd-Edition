#pragma once

#include <string>

namespace cb::util {

std::string sha256_hex(const std::string& data);
std::string span_tag(const std::string& body, const std::string& kit_id, int gen_marker);

}  // namespace cb::util
