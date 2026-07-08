#pragma once

#include <cstdint>
#include <string>
#include <string_view>
#include <vector>

namespace ark::util {

std::string sha256_hex(std::string_view data);
std::string link_tag(std::string_view envelope_bytes, std::string_view kit_id, int gen_marker);
std::string fresh_tag(std::string_view actor_id, std::string_view wave_id, int gen_marker);

}  // namespace ark::util
