#include "session_registry.hpp"

#include <fstream>

namespace cc::engine {

SessionState load_session(const std::string& path) {
  (void)path;
  return {};
}

void save_session(const std::string& path, const SessionState& state) {
  (void)path;
  (void)state;
}

}  // namespace cc::engine
