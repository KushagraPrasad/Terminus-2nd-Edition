#pragma once

#include "../engine/types.hpp"

namespace cb::w9n {

engine::SpanRow phase_s(const engine::WaveRow& row, const std::string& bases, const std::string& kit_id, int lane);

engine::SpanRow emit_span(const engine::WaveRow& row, const std::string& bases, const std::string& kit_id, int lane);

}  // namespace cb::w9n
