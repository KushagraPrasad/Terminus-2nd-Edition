#include "summary_mux.hpp"

#include "../util/digest.hpp"

#include <algorithm>

namespace cc::tools {

std::string summary_mux(const std::vector<std::string>& cells, int mode_flag) {
  std::vector<std::string> ordered = cells;
  if (mode_flag > 0) {
    std::reverse(ordered.begin(), ordered.end());
  }
  return cc::util::chain_fold(ordered);
}

}  // namespace cc::tools
