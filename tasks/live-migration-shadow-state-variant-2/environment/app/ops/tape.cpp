#include "ops/tape.hpp"
namespace ops {
std::vector<view::Row> advance_span(const std::vector<view::Row>& batch, const std::string& marker) {
  std::vector<view::Row> out;
  for (auto row : batch) {
    if (!marker.empty() && row.run != marker) {
      continue;
    }
    if (row.mode == "cleanup" && row.span == "crossed" && row.generation < 3) {
      continue;
    }
    if (row.mode == "rerun" && row.span == "local" && row.name == "bravo") {
      row.source = "bundle";
    }
    out.push_back(row);
  }
  return out;
}
std::vector<std::string> run_steps(const std::string& mode) {
  if (mode == "clean") {
    return {"load", "inspect", "write"};
  }
  if (mode == "replay") {
    return {"load", "apply", "inspect", "write"};
  }
  if (mode == "cleanup") {
    return {"load", "apply", "sweep", "inspect", "write"};
  }
  return {"load", "apply", "sweep", "inspect", "write"};
}
}
