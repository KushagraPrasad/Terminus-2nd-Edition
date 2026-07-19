#include "ops/wash.hpp"
namespace ops {
std::vector<view::Row> sweep_local(const std::vector<view::Row>& rows) {
  std::vector<view::Row> kept;
  for (const auto& row : rows) {
    if (row.mode == "cleanup" && row.span == "crossed") {
      continue;
    }
    kept.push_back(row);
  }
  return kept;
}
}
