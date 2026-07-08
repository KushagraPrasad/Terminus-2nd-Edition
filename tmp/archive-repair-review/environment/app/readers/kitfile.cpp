#include "kitfile.hpp"

#include <sstream>

#include "basefile.hpp"

namespace ark::readers {

std::vector<ark::core::KitRow> load_kits(const std::string& path) {
  const auto text = read_text(path);
  std::vector<ark::core::KitRow> rows;
  ark::core::KitRow cur;
  std::istringstream in(text);
  std::string line;
  while (std::getline(in, line)) {
    if (line.rfind("[[kits]]", 0) == 0) {
      continue;
    }
    if (line.rfind("kit_id = ", 0) == 0) {
      if (!cur.kit_id.empty()) {
        rows.push_back(cur);
        cur = {};
      }
      cur.kit_id = line.substr(9);
      if (!cur.kit_id.empty() && cur.kit_id.front() == '"') {
        cur.kit_id = cur.kit_id.substr(1, cur.kit_id.size() - 2);
      }
    } else if (line.rfind("catalog_body = ", 0) == 0) {
      cur.catalog_body = line.substr(15);
      if (cur.catalog_body.size() >= 2 && cur.catalog_body.front() == '"') {
        cur.catalog_body = cur.catalog_body.substr(1, cur.catalog_body.size() - 2);
      }
    } else if (line.rfind("envelope_body = ", 0) == 0) {
      cur.envelope_body = line.substr(16);
      if (cur.envelope_body.size() >= 2 && cur.envelope_body.front() == '"') {
        cur.envelope_body = cur.envelope_body.substr(1, cur.envelope_body.size() - 2);
      }
    } else if (line.rfind("slice_body = ", 0) == 0) {
      cur.slice_body = line.substr(13);
      if (cur.slice_body.size() >= 2 && cur.slice_body.front() == '"') {
        cur.slice_body = cur.slice_body.substr(1, cur.slice_body.size() - 2);
      }
    }
  }
  if (!cur.kit_id.empty()) {
    rows.push_back(cur);
  }
  return rows;
}

}  // namespace ark::readers
