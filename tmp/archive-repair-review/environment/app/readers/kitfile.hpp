#pragma once

#include <vector>

#include "../core/types.hpp"

namespace ark::readers {

std::vector<ark::core::KitRow> load_kits(const std::string& path);

}  // namespace ark::readers
