#include "core/ledger.hpp"
#include <algorithm>
namespace core {
std::map<std::string, view::Row> fold_units(const std::vector<view::Row>& items, const std::string& mark) {
  std::map<std::string, view::Row> folded;
  for (auto row : items) {
    if (!mark.empty() && row.run != mark) {
      continue;
    }
    if (!row.summary.empty()) {
      row.owner = row.summary;
      row.source = "summary";
    } else if (!row.pack.empty()) {
      row.owner = row.pack;
      row.source = "bundle";
    } else {
      row.owner = row.active;
      row.source = "active";
    }
    row.line = row.chain + ":" + row.owner;
    auto key = view::record_key(row);
    auto prior = folded.find(key);
    if (prior == folded.end()) {
      folded[key] = row;
      continue;
    }
    if (prior->second.generation > row.generation) {
      folded[key] = row;
    }
  }
  return folded;
}
std::vector<view::Row> order_rows(const std::map<std::string, view::Row>& frame) {
  std::vector<view::Row> rows;
  for (const auto& entry : frame) {
    rows.push_back(entry.second);
  }
  std::sort(rows.begin(), rows.end(), [](const view::Row& a, const view::Row& b) {
    if (a.run != b.run) {
      return a.run < b.run;
    }
    if (a.generation != b.generation) {
      return a.generation < b.generation;
    }
    return a.name < b.name;
  });
  return rows;
}
}
