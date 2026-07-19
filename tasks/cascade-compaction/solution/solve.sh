#!/usr/bin/env bash
set -euo pipefail

cat >/app/environment/k7w/lane_mux.cpp <<'EOF'
#include "lane_mux.hpp"

namespace cc::persist {

std::map<std::string, int> fn_k2(const std::vector<std::map<std::string, int>>& buf, int mark_a,
                                int mark_b) {
  std::map<std::string, int> out;
  int cursor = 0;
  int sealed = 0;
  if (!buf.empty()) {
    cursor = buf.back().count("cursor") ? buf.back().at("cursor") : 0;
    sealed = buf.back().count("sealed") ? buf.back().at("sealed") : 0;
  }
  if (mark_a > 0 && cursor > sealed) {
    out["cursor"] = cursor;
    out["sealed"] = sealed;
    out["unsealed_tail"] = 1;
    return out;
  }
  if (mark_a > 0) {
    cursor = std::max(0, cursor - 1);
  }
  if (mark_b > 0) {
    sealed += 1;
    cursor += 1;
  }
  out["cursor"] = cursor;
  out["sealed"] = sealed;
  out["unsealed_tail"] = (cursor > sealed) ? 1 : 0;
  return out;
}

}  // namespace cc::persist
EOF

cat >/app/environment/m9p/stamp_mux.cpp <<'EOF'
#include "stamp_mux.hpp"

#include <algorithm>

namespace cc::runtime {

int fn_h8(std::map<std::string, int>& ctx, int gen_a, int gen_b) {
  const int floor = ctx.count("registry_gen_floor") ? ctx["registry_gen_floor"] : 0;
  int active = ctx.count("active_gen") ? ctx["active_gen"] : floor;
  active = std::max(active, floor);
  int sealed = ctx.count("sealed_total") ? ctx["sealed_total"] : 0;
  const int need = ctx.count("phase_need") ? ctx["phase_need"] : 0;
  if (ctx.count("restart_flag") && ctx["restart_flag"] > 0) {
    const int pre = ctx.count("pre_gen") ? ctx["pre_gen"] : active;
    active = std::max({pre + 1, gen_b + 1, floor + 1});
    ctx["active_gen"] = active;
    return active;
  }
  if (gen_b + 1 > active && sealed >= need) {
    active = std::max(gen_b + 1, floor);
  } else if (gen_a > active && sealed >= need) {
    active = std::max(gen_a, floor);
  }
  ctx["pre_gen"] = active;
  ctx["active_gen"] = active;
  return active;
}

}  // namespace cc::runtime
EOF

cat >/app/environment/n4q/mux_sel.cpp <<'EOF'
#include "mux_sel.hpp"

#include "../util/digest.hpp"

namespace cc::reconcile {

std::map<std::string, std::string> fn_w4(const std::vector<std::pair<std::string, std::string>>& rows,
                                        const std::string& tag_p, const std::string& tag_q) {
  std::vector<std::string> manifest_parts;
  for (const auto& row : rows) {
    if (row.first.rfind('m', 0) == 0) {
      manifest_parts.push_back(row.second);
    }
  }
  (void)tag_q;
  std::map<std::string, std::string> out;
  out["pick"] = cc::util::chain_fold(manifest_parts);
  out["lane"] = tag_p;
  return out;
}

}  // namespace cc::reconcile
EOF

cat >/app/environment/engine/session_registry.cpp <<'EOF'
#include "session_registry.hpp"

#include <fstream>
#include <sstream>

namespace cc::engine {

namespace {

int parse_int_field(const std::string& text, const std::string& key) {
  const std::string needle = "\"" + key + "\":";
  const std::size_t pos = text.find(needle);
  if (pos == std::string::npos) {
    return 0;
  }
  return std::stoi(text.substr(pos + needle.size()));
}

std::string parse_string_field(const std::string& text, const std::string& key) {
  const std::string needle = "\"" + key + "\":\"";
  const std::size_t pos = text.find(needle);
  if (pos == std::string::npos) {
    return "";
  }
  const std::size_t start = pos + needle.size();
  const std::size_t end = text.find('"', start);
  if (end == std::string::npos) {
    return "";
  }
  return text.substr(start, end - start);
}

}  // namespace

SessionState load_session(const std::string& path) {
  SessionState state;
  std::ifstream in(path);
  if (!in) {
    return state;
  }
  std::ostringstream buffer;
  buffer << in.rdbuf();
  const std::string text = buffer.str();
  state.gen_high_water = parse_int_field(text, "gen_high_water");
  state.ledger_anchor_hex = parse_string_field(text, "ledger_anchor_hex");
  return state;
}

void save_session(const std::string& path, const SessionState& state) {
  std::ofstream out(path);
  out << "{\"gen_high_water\":" << state.gen_high_water << ",\"ledger_anchor_hex\":\""
      << state.ledger_anchor_hex << "\"}";
}

}  // namespace cc::engine
EOF

sed -i 's/ctx\["registry_gen_floor"\] = 0;/ctx["registry_gen_floor"] = prior.gen_high_water;/' /app/environment/engine/pipeline.cpp
sed -i '/(void)prior;/d' /app/environment/engine/pipeline.cpp

cat >/app/environment/pilot/entry.cpp <<'EOF'
#include "../engine/pipeline.hpp"
#include "../engine/session_registry.hpp"
#include "../engine/types.hpp"
#include "../util/digest.hpp"
#include "../util/json_codec.hpp"

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <string>

namespace {

constexpr const char* kSessionPath = "/app/environment/state/session.registry";

struct Args {
  std::string profile = "a";
  std::string out = "/app/output/cc_report.json";
  std::string ledger_dir = "/app/output/run_logs";
};

Args parse_args(int argc, char** argv) {
  Args args;
  for (int i = 1; i < argc; ++i) {
    const std::string flag = argv[i];
    if (flag == "--profile" && i + 1 < argc) {
      args.profile = argv[++i];
    } else if (flag == "--out" && i + 1 < argc) {
      args.out = argv[++i];
    } else if (flag == "--ledger-dir" && i + 1 < argc) {
      args.ledger_dir = argv[++i];
    }
  }
  return args;
}

cc::engine::Profile load_profile(const std::string& id) {
  cc::engine::Profile profile;
  profile.id = id;
  if (id == "a") {
    profile.inject_restart = true;
    profile.phase_count = 3;
  } else if (id == "b") {
    profile.conflict = true;
    profile.phase_count = 3;
  } else if (id == "c") {
    profile.inject_rollback = true;
    profile.phase_count = 4;
  } else if (id == "d") {
    profile.inject_restart = true;
    profile.conflict = true;
    profile.phase_count = 4;
  } else {
    profile.phase_count = 2;
  }
  return profile;
}

std::string row_json(const cc::engine::Row& row) {
  return cc::util::obj({{"phase", std::to_string(row.phase)},
                        {"gen_stamp", std::to_string(row.gen_stamp)},
                        {"sealed_count", std::to_string(row.sealed_count)},
                        {"lane_tag", cc::util::quote(row.lane_tag)}});
}

std::string run_json(const cc::engine::RunDoc& doc) {
  std::vector<std::string> rows;
  for (const auto& row : doc.rows) {
    rows.push_back(row_json(row));
  }
  return cc::util::obj({{"profile_id", cc::util::quote(doc.profile_id)},
                        {"restart_seen", doc.restart_seen ? "true" : "false"},
                        {"rows", cc::util::arr(rows)},
                        {"manifest_chain_hex", cc::util::quote(doc.manifest_chain_hex)},
                        {"summary_chain_hex", cc::util::quote(doc.summary_chain_hex)},
                        {"summary_code", cc::util::quote(doc.summary_code)}});
}

std::string read_text(const std::string& path) {
  std::ifstream in(path);
  if (!in) {
    return "";
  }
  std::ostringstream ss;
  ss << in.rdbuf();
  return ss.str();
}

std::string append_report_payload(const std::string& current, const std::string& run_payload) {
  if (current.empty()) {
    return cc::util::obj({{"runs", cc::util::arr({run_payload})}});
  }
  const std::size_t close = current.rfind(']');
  if (close == std::string::npos) {
    return cc::util::obj({{"runs", cc::util::arr({run_payload})}});
  }
  const bool has_existing_run = current.find("\"profile_id\"") != std::string::npos;
  std::string updated = current.substr(0, close);
  if (has_existing_run) {
    updated.push_back(',');
  }
  updated.append(run_payload);
  updated.append(current.substr(close));
  return updated;
}

int run_count_in_report(const std::string& path) {
  const std::string current = read_text(path);
  int count = 0;
  std::size_t pos = 0;
  while ((pos = current.find("\"profile_id\"", pos)) != std::string::npos) {
    ++count;
    pos += 12;
  }
  return count;
}

std::string ledger_path(const std::string& dir, int run_index, const std::string& profile) {
  std::ostringstream path;
  path << dir << "/run_" << std::setw(4) << std::setfill('0') << run_index << '_' << profile
       << ".json";
  return path.str();
}

int max_gen_stamp(const cc::engine::RunDoc& doc) {
  int best = 0;
  for (const auto& row : doc.rows) {
    best = std::max(best, row.gen_stamp);
  }
  return best;
}

}  // namespace

int main(int argc, char** argv) {
  const Args args = parse_args(argc, argv);
  const auto profile = load_profile(args.profile);
  const auto doc = cc::engine::execute_profile(profile);

  std::filesystem::create_directories(std::filesystem::path(args.out).parent_path());
  std::filesystem::create_directories(args.ledger_dir);
  std::filesystem::create_directories(std::filesystem::path(kSessionPath).parent_path());

  const int run_index = run_count_in_report(args.out);
  const std::string run_payload = run_json(doc);
  const std::string report_payload = append_report_payload(read_text(args.out), run_payload);
  std::ofstream out(args.out);
  out << report_payload;

  cc::engine::SessionState session = cc::engine::load_session(kSessionPath);
  const std::string fingerprint = doc.manifest_chain_hex;
  std::string ledger_anchor = fingerprint;
  if (!session.ledger_anchor_hex.empty()) {
    ledger_anchor = cc::util::chain_fold({session.ledger_anchor_hex, fingerprint});
  }

  const int final_sealed = doc.rows.empty() ? 0 : doc.rows.back().sealed_count;
  const std::string ledger_payload =
      cc::util::obj({{"run_index", std::to_string(run_index)},
                     {"profile_id", cc::util::quote(doc.profile_id)},
                     {"fingerprint", cc::util::quote(fingerprint)},
                     {"final_sealed_count", std::to_string(final_sealed)},
                     {"ledger_anchor_hex", cc::util::quote(ledger_anchor)}});
  std::ofstream ledger(ledger_path(args.ledger_dir, run_index, args.profile));
  ledger << ledger_payload;

  session.gen_high_water = std::max(session.gen_high_water, max_gen_stamp(doc));
  session.ledger_anchor_hex = ledger_anchor;
  cc::engine::save_session(kSessionPath, session);
  return 0;
}
EOF

cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
cmake --build /app/build -j2
cp /app/build/cc_run /app/bin/cc_run
