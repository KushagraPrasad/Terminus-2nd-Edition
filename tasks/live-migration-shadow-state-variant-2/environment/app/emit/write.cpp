#include "emit/write.hpp"
#include "emit/frame.hpp"
#include "ops/tape.hpp"
#include <filesystem>
#include <fstream>
namespace emit {
void emit_report(const std::string& target, const std::map<std::string, std::vector<std::string>>& runs, const std::vector<view::Artifact>& artifacts, const std::vector<view::Row>& ordered_rows) {
  (void)ordered_rows;
  std::filesystem::create_directories(std::filesystem::path(target).parent_path());
  std::ofstream out(target);
  out << "{\n  \"runs\": [\n";
  bool first_run = true;
  for (const auto& entry : runs) {
    if (!first_run) {
      out << ",\n";
    }
    first_run = false;
    std::string mode = entry.first == "later" ? "replay" : entry.first == "sweep" ? "cleanup" : entry.first == "repeat" ? "rerun" : "clean";
    out << "    {\"run_id\":\"" << view::escape_json(entry.first) << "\",\"mode\":\"" << view::escape_json(mode) << "\",\"steps\":[";
    auto steps = ops::run_steps(mode);
    for (size_t i = 0; i < steps.size(); ++i) {
      if (i) {
        out << ",";
      }
      out << "\"" << view::escape_json(steps[i]) << "\"";
    }
    out << "],\"records\":[";
    for (size_t i = 0; i < entry.second.size(); ++i) {
      if (i) {
        out << ",";
      }
      out << entry.second[i];
    }
    out << "]}";
  }
  out << "\n  ],\n  \"artifacts\": [";
  for (size_t i = 0; i < artifacts.size(); ++i) {
    if (i) {
      out << ",";
    }
    out << artifact_json(artifacts[i]);
  }
  out << "],\n  \"fingerprints\": {\"stable_digest\":\"deadbeef\",\"session_span_id\":\"00000000\"}\n}\n";
}
}
