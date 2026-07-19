#include "pipeline.hpp"

#include "session_registry.hpp"

#include "../k7w/lane_mux.hpp"
#include "../m9p/stamp_mux.hpp"
#include "../n4q/fold_apply.hpp"
#include "../tools/summary_mux.hpp"

#include <sstream>

namespace cc::engine {

namespace {

constexpr const char* kSessionPath = "/app/environment/state/session.registry";

std::string row_key(int phase, int gen_stamp, int sealed_count) {
  std::ostringstream oss;
  oss << phase << '|' << gen_stamp << '|' << sealed_count;
  return oss.str();
}

}  // namespace

RunDoc execute_profile(const Profile& profile) {
  RunDoc doc;
  doc.profile_id = profile.id;
  doc.restart_seen = profile.inject_restart;
  const SessionState prior = load_session(kSessionPath);
  Ctx ctx;
  ctx["registry_gen_floor"] = 0;
  (void)prior;
  std::vector<std::map<std::string, int>> lane_buf;
  std::vector<std::pair<std::string, std::string>> fold_rows;
  std::vector<std::string> summary_cells;

  for (int phase = 0; phase < profile.phase_count; ++phase) {
    if (profile.inject_restart && phase == profile.phase_count / 2) {
      ctx["restart_flag"] = 1;
    } else {
      ctx["restart_flag"] = 0;
    }
    if (profile.inject_rollback && phase == profile.phase_count - 1) {
      ctx["rollback_flag"] = 1;
    } else {
      ctx["rollback_flag"] = 0;
    }
    ctx["phase_need"] = phase;
    ctx["sealed_total"] = ctx.count("sealed_total") ? ctx["sealed_total"] : 0;

    const int gen = cc::runtime::fn_h8(ctx, phase, phase + 1);
    const int rollback_mark = ctx["rollback_flag"] > 0 ? 1 : 0;
    const int seal_mark = (phase % 2 == 0) ? 1 : 0;
    auto lane_state = cc::persist::fn_k2(lane_buf, rollback_mark, seal_mark);
    lane_buf.push_back(lane_state);
    if (seal_mark > 0) {
      ctx["sealed_total"] = lane_state["sealed"];
    }

    Row row;
    row.phase = phase;
    row.gen_stamp = gen;
    row.sealed_count = lane_state["sealed"];
    row.lane_tag = "m" + std::to_string(phase);
    doc.rows.push_back(row);

    const std::string cell = row_key(row.phase, row.gen_stamp, row.sealed_count);
    fold_rows.emplace_back("m" + std::to_string(phase), cell);
    if (profile.conflict) {
      fold_rows.emplace_back("s" + std::to_string(phase), cell + "|alt");
    }
    summary_cells.push_back(cell);
  }

  doc.manifest_chain_hex = cc::n4q::apply_fold(fold_rows, profile.conflict);
  doc.summary_chain_hex = cc::tools::summary_mux(summary_cells, profile.conflict ? 1 : 0);
  doc.summary_code = "ok";
  return doc;
}

}  // namespace cc::engine
