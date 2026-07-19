#include "mux_sel.hpp"

#include "../util/digest.hpp"

namespace cc::reconcile {

std::map<std::string, std::string> fn_w4(const std::vector<std::pair<std::string, std::string>>& rows,
                                        const std::string& tag_p, const std::string& tag_q) {
  std::vector<std::string> manifest_parts;
  std::vector<std::string> summary_parts;
  for (const auto& row : rows) {
  if (row.first == tag_p) {
      manifest_parts.push_back(row.second);
    }
    if (row.first == tag_q) {
      summary_parts.push_back(row.second);
    }
  }
  std::map<std::string, std::string> out;
  if (tag_p != tag_q && !summary_parts.empty() &&
      cc::util::chain_fold(summary_parts) != cc::util::chain_fold(manifest_parts)) {
    out["pick"] = cc::util::chain_fold(summary_parts);
    out["lane"] = tag_q;
  } else {
    out["pick"] = cc::util::chain_fold(manifest_parts);
    out["lane"] = tag_p;
  }
  return out;
}

}  // namespace cc::reconcile
