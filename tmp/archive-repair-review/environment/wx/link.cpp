#include "link.hpp"

#include "../util/tag_core.hpp"

namespace ark::wx {

ark::core::LinkRow phase_c(const ark::core::WaveRecord& wave, const std::string& body_bytes, const std::string& kit_id, int gen_marker, int lane) {
  ark::core::LinkRow row;
  row.wave_id = wave.wave_id;
  row.kit_id = kit_id;
  row.gen_marker = gen_marker;
  row.source_lane = (lane == 0) ? "catalog" : (lane == 1) ? "envelope" : "slice";
  const int mix = (lane == 1) ? gen_marker + 1 : gen_marker;
  row.link_hex = ark::util::link_tag(body_bytes, kit_id, mix);
  return row;
}

ark::core::LinkRow emit_digest(const ark::core::WaveRecord& wave, const std::string& body_bytes, const std::string& kit_id, int gen_marker, int lane) {
  return phase_c(wave, body_bytes, kit_id, gen_marker, 0);
}

}  // namespace ark::wx
