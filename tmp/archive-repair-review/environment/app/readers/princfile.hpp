#pragma once

#include <vector>

#include "../core/types.hpp"

namespace ark::readers {

std::vector<ark::core::ActorRow> load_actors(const std::string& path);

}  // namespace ark::readers
