#pragma once

#include <string>

#include "../app/core/types.hpp"

namespace ark::wx {

ark::core::LinkRow phase_c(const ark::core::WaveRecord& wave, const std::string& body_bytes, const std::string& kit_id, int gen_marker, int lane);

ark::core::LinkRow emit_digest(const ark::core::WaveRecord& wave, const std::string& body_bytes, const std::string& kit_id, int gen_marker, int lane);

}  // namespace ark::wx
