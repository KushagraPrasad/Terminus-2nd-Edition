#pragma once

#include "../engine/types.hpp"

namespace cb::driver {

engine::RunRecord build_run(const std::string& run_id, const engine::SeqBundle& bundle, const engine::ViewRow& view);

}  // namespace cb::driver
