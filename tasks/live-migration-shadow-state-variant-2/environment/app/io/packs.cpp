#include "io/packs.hpp"
#include <fstream>
#include <sstream>
#include <stdexcept>
namespace { std::vector<std::string> split(const std::string& line) { std::vector<std::string> parts; std::stringstream ss(line); std::string item; while (std::getline(ss, item, '|')) parts.push_back(item); return parts; } }
namespace io {
std::vector<view::Row> load_rows(const std::string& root) {
  std::ifstream in(root + "/fixtures/packs.tsv");
  if (!in) throw std::runtime_error("could not open local scenario rows");
  std::vector<view::Row> rows; std::string line;
  while (std::getline(in, line)) {
    if (line.empty() || line[0] == '#') continue;
    auto p = split(line); if (p.size() != 10) throw std::runtime_error("malformed local scenario row");
    view::Row row; row.run = p[0]; row.mode = p[1]; row.name = p[2]; row.generation = std::stoi(p[3]); row.active = p[4]; row.pack = p[5]; row.summary = p[6]; row.chain = p[7]; row.file = p[8]; row.span = p[9]; row.removed = (p[9] == "removed"); rows.push_back(row);
  }
  return rows;
}
}
