#include "frame.hpp"

#include "../util/json_emit.hpp"

namespace cb::w9n {

std::string frame_run(const engine::RunRecord& run) {
  std::vector<std::string> waves;
  for (const auto& wave : run.waves) {
    waves.push_back(cb::util::obj({
        {"wave_id", cb::util::quote(wave.wave_id)},
        {"health_status", cb::util::quote(wave.health_status)},
        {"gen_marker", std::to_string(wave.gen_marker)},
        {"seal_slot", std::to_string(wave.seal_slot)},
    }));
  }
  std::vector<std::string> spans;
  for (const auto& span : run.spans) {
    spans.push_back(cb::util::obj({
        {"wave_id", cb::util::quote(span.wave_id)},
        {"kit_id", cb::util::quote(span.kit_id)},
        {"tag_hex", cb::util::quote(span.tag_hex)},
        {"source_lane", cb::util::quote(span.source_lane)},
        {"gen_marker", std::to_string(span.gen_marker)},
    }));
  }
  return cb::util::obj({
      {"run_id", cb::util::quote(run.run_id)},
      {"restart_seen", run.restart_seen ? "true" : "false"},
      {"waves", cb::util::arr(waves)},
      {"span_records", cb::util::arr(spans)},
  });
}

}  // namespace cb::w9n
