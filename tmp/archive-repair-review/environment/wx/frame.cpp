#include "frame.hpp"

#include "../util/json_write.hpp"

namespace ark::wx {

std::string frame_run(const ark::core::RunRecord& run) {
  std::vector<ark::util::JsonObj> fields;
  fields.push_back({"run_id", ark::util::quote(run.run_id)});
  fields.push_back({"restart_seen", run.restart_seen ? "true" : "false"});
  std::vector<std::string> wave_items;
  for (const auto& w : run.waves) {
    wave_items.push_back(ark::util::obj({
        {"wave_id", ark::util::quote(w.wave_id)},
        {"health_status", ark::util::quote(w.health_status)},
        {"gen_marker", std::to_string(w.gen_marker)},
        {"seal_slot", std::to_string(w.seal_slot)},
    }));
  }
  fields.push_back({"waves", ark::util::arr(wave_items)});
  std::vector<std::string> tr_items;
  for (const auto& t : run.transitions) {
    tr_items.push_back(ark::util::obj({
        {"actor_id", ark::util::quote(t.actor_id)},
        {"from_wave", ark::util::quote(t.from_wave)},
        {"to_wave", ark::util::quote(t.to_wave)},
        {"outcome", ark::util::quote(t.outcome)},
    }));
  }
  fields.push_back({"principal_transitions", ark::util::arr(tr_items)});
  std::vector<std::string> link_items;
  for (const auto& l : run.links) {
    link_items.push_back(ark::util::obj({
        {"wave_id", ark::util::quote(l.wave_id)},
        {"kit_id", ark::util::quote(l.kit_id)},
        {"link_hex", ark::util::quote(l.link_hex)},
        {"source_lane", ark::util::quote(l.source_lane)},
        {"gen_marker", std::to_string(l.gen_marker)},
    }));
  }
  fields.push_back({"digest_records", ark::util::arr(link_items)});
  return ark::util::obj(fields);
}

}  // namespace ark::wx
