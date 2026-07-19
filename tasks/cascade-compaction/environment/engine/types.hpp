#pragma once

#include <map>
#include <string>
#include <vector>

namespace cc::engine {

struct Row {
  int phase = 0;
  int gen_stamp = 0;
  int sealed_count = 0;
  std::string lane_tag;
};

struct RunDoc {
  std::string profile_id;
  bool restart_seen = false;
  std::vector<Row> rows;
  std::string manifest_chain_hex;
  std::string summary_chain_hex;
  std::string summary_code;
};

struct Profile {
  std::string id;
  bool inject_restart = false;
  bool inject_rollback = false;
  bool conflict = false;
  int phase_count = 3;
};

using Ctx = std::map<std::string, int>;

}  // namespace cc::engine
