#pragma once

#include <string>

namespace cc::engine {

struct SessionState {
  int gen_high_water = 0;
  std::string ledger_anchor_hex;
};

SessionState load_session(const std::string& path);
void save_session(const std::string& path, const SessionState& state);

}  // namespace cc::engine
