#pragma once

#include <string>
#include <vector>

namespace ark::core {

struct ActorRow {
  std::string actor_id;
  bool revoked = false;
};

struct KitRow {
  std::string kit_id;
  std::string catalog_body;
  std::string envelope_body;
  std::string slice_body;
};

struct WaveRecord {
  std::string wave_id;
  std::string health_status;
  int gen_marker = 0;
  int seal_slot = 0;
};

struct TransitionRow {
  std::string actor_id;
  std::string from_wave;
  std::string to_wave;
  std::string outcome;
};

struct LinkRow {
  std::string wave_id;
  std::string kit_id;
  std::string link_hex;
  std::string source_lane;
  int gen_marker = 0;
};

struct RunRecord {
  std::string run_id;
  std::vector<WaveRecord> waves;
  std::vector<TransitionRow> transitions;
  std::vector<LinkRow> links;
  bool restart_seen = false;
};

struct SessionCtx {
  int gen_marker = 1;
  bool restart_boundary = false;
  int overlap_phase = 0;
  int surface_pick = 0;
};

struct SeqBundle {
  int base_gen = 1;
  bool inject_restart = false;
  int pair_order = 0;
  int fork_branch = 0;
};

}  // namespace ark::core
