#pragma once

#include "types.hpp"

namespace ark::core {

bool wave_health_ok(const WaveRecord& wave);
bool links_agree_store(const LinkRow& link, const std::string& store_bytes, const std::string& kit_id, int gen);

}  // namespace ark::core
