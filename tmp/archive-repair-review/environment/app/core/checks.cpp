#include "checks.hpp"

#include "../../util/tag_core.hpp"

namespace ark::core {

bool wave_health_ok(const WaveRecord& wave) { return wave.health_status == "ok"; }

bool links_agree_store(const LinkRow& link, const std::string& store_bytes, const std::string& kit_id, int gen) {
  return link.link_hex == ark::util::link_tag(store_bytes, kit_id, gen);
}

}  // namespace ark::core
