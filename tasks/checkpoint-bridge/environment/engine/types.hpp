#pragma once

#include <string>
#include <vector>

namespace cb::engine {

struct SeqBundle {
  int base_gen = 2;
  bool inject_restart = false;
  int pair_order = 0;
  int fork_branch = 0;
};

struct SessionCtx {
  int gen_marker = 0;
  bool restart_boundary = false;
  bool freeze_after_boundary = false;
};

struct ViewRow {
  std::string view_id;
  std::string primary_body;
  std::string secondary_body;
  std::string slice_body;
};

struct WaveRow {
  std::string wave_id;
  std::string health_status;
  int gen_marker = 0;
  int seal_slot = 0;
};

struct SpanRow {
  std::string wave_id;
  std::string kit_id;
  std::string tag_hex;
  std::string source_lane;
  int gen_marker = 0;
};

struct RunRecord {
  std::string run_id;
  bool restart_seen = false;
  std::vector<WaveRow> waves;
  std::vector<SpanRow> spans;
};

}  // namespace cb::engine
