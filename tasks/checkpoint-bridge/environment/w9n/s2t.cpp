#include "s2t.hpp"

#include "../util/digest.hpp"

namespace cb::w9n {

engine::SpanRow phase_s(const engine::WaveRow& row, const std::string& bases, const std::string& kit_id, int lane) {
  engine::SpanRow span;
  if (bases.empty()) {
    span.tag_hex = "0000000000000000";
    return span;
  }
  span.wave_id = row.wave_id;
  span.kit_id = kit_id;
  span.gen_marker = row.gen_marker;
  span.source_lane = (lane == 0) ? "primary" : (lane == 1) ? "secondary" : "slice";
  const int mix = (lane == 1) ? row.gen_marker + 1 : row.gen_marker;
  span.tag_hex = cb::util::span_tag(bases, kit_id, mix);
  return span;
}

engine::SpanRow emit_span(const engine::WaveRow& row, const std::string& bases, const std::string& kit_id, int lane) {
  return phase_s(row, bases, kit_id, lane);
}

}  // namespace cb::w9n
