#pragma once

#include "core/types.hpp"

namespace ark::app {

ark::core::RunRecord build_run(const std::string& run_id, const ark::core::SeqBundle& bundle, const ark::core::KitRow& kit,
                               const std::vector<ark::core::ActorRow>& actors);

}  // namespace ark::app
