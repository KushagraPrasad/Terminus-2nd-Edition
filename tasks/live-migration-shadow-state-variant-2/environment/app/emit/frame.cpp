#include "emit/frame.hpp"
#include <sstream>
namespace {
std::string display_active(const view::Row& row) {
  if (!row.summary.empty()) {
    return row.summary;
  }
  if (!row.pack.empty()) {
    return row.pack;
  }
  return row.active;
}

std::string display_summary(const view::Row& row) {
  if (!row.summary.empty()) {
    return row.summary;
  }
  return row.pack.empty() ? row.owner : row.pack;
}

std::string display_source(const view::Row& row, const std::string& label) {
  if (!row.source.empty()) {
    return row.source;
  }
  if (!row.summary.empty()) {
    return "summary";
  }
  return label;
}
}
namespace emit {
std::vector<std::string> shape_rows(const std::string& label, const std::map<std::string, view::Row>& frame, const std::vector<std::string>& order) {
  std::vector<std::string> rows;
  for (const auto& key : order) {
    auto it = frame.find(key);
    if (it == frame.end()) {
      continue;
    }
    const auto& r = it->second;
    std::ostringstream out;
    out << "{\"name\":\"" << view::escape_json(r.name) << "\",\"generation\":" << r.generation << ",\"owner\":\"" << view::escape_json(r.owner) << "\",\"lineage\":\"" << view::escape_json(r.line) << "\",\"boundary\":\"" << view::escape_json(r.span) << "\",\"artifact\":\"" << view::escape_json(r.file) << "\",\"evidence\":{";
    const std::string src = display_source(r, label);
    const std::string active = display_active(r);
    const std::string pack = r.pack.empty() ? r.owner : r.pack;
    const std::string summary = display_summary(r);
    out << "\"active\":\"" << view::escape_json(active) << "\",\"bundle\":\"" << view::escape_json(pack) << "\",\"summary\":\"" << view::escape_json(summary) << "\",\"source\":\"" << view::escape_json(src) << "\"}}";
    rows.push_back(out.str());
  }
  return rows;
}
std::vector<std::string> rows_for_run(const std::string& label, const std::map<std::string, view::Row>& frame) {
  std::vector<std::string> order;
  for (const auto& entry : frame) {
    order.push_back(entry.first);
  }
  return shape_rows(label, frame, order);
}

std::string artifact_json(const view::Artifact& artifact) {
  std::ostringstream out;
  out << "{\"run_id\":\"" << view::escape_json(artifact.run) << "\",\"name\":\"" << view::escape_json(artifact.name) << "\",\"generation\":" << artifact.generation << ",\"owner\":\"" << view::escape_json(artifact.owner) << "\",\"lineage\":\"" << view::escape_json(artifact.line) << "\",\"path\":\"" << view::escape_json(artifact.file) << "\"}";
  return out.str();
}
}
