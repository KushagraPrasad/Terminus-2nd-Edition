#!/bin/bash
# Terminal-Bench Canary: oracle replaces frontier modules with corrected logic.
set -euo pipefail
cd /app/environment
python3 - <<'PYFIX'
from pathlib import Path

Path('app/flow.cpp').write_text(r"""#include "flow.hpp"
#include "core/ledger.hpp"
#include "emit/frame.hpp"
#include "emit/write.hpp"
#include "io/packs.hpp"
#include "io/store.hpp"
#include "ops/journal.hpp"
#include "ops/reconcile.hpp"
#include "ops/tape.hpp"
#include <set>
namespace app {
ReportParts build_parts(const std::string& root) {
  auto rows = io::load_rows(root);
  rows = ops::apply_log(rows, root);
  rows = ops::merge_tombstones(rows, root);
  std::set<std::string> run_ids;
  for (const auto& row : rows) {
    run_ids.insert(row.run);
  }
  ReportParts parts;
  std::vector<view::Row> all_ordered;
  for (const auto& run : run_ids) {
    auto advanced = ops::advance_span(rows, run);
    auto folded = core::fold_units(advanced, run);
    auto ordered = core::order_rows(folded);
    for (const auto& row : ordered) {
      all_ordered.push_back(row);
    }
    parts.runs[run] = emit::rows_for_run(run, folded);
  }
  parts.artifacts = io::bind_all(all_ordered);
  parts.ordered_rows = all_ordered;
  return parts;
}
}
""")

Path('app/ops/journal.cpp').write_text(r"""#include "ops/journal.hpp"
#include <algorithm>
#include <fstream>
#include <sstream>
namespace {
struct entry {
  int seq = 0;
  std::string run;
  std::string name;
  std::string op;
  int generation = 0;
  std::string active;
};

std::vector<entry> read_log(const std::string& root) {
  std::ifstream in(root + "/fixtures/wal.json");
  if (!in) {
    return {};
  }
  std::string blob((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
  std::vector<entry> items;
  size_t pos = 0;
  while ((pos = blob.find("\"seq\"", pos)) != std::string::npos) {
    entry item;
    auto seq_pos = blob.find(':', pos);
    item.seq = std::stoi(blob.substr(seq_pos + 1));
    auto run_pos = blob.find("\"run\"", pos);
    run_pos = blob.find('"', run_pos + 5);
    auto run_end = blob.find('"', run_pos + 1);
    item.run = blob.substr(run_pos + 1, run_end - run_pos - 1);
    auto name_pos = blob.find("\"name\"", run_end);
    name_pos = blob.find('"', name_pos + 6);
    auto name_end = blob.find('"', name_pos + 1);
    item.name = blob.substr(name_pos + 1, name_end - name_pos - 1);
    auto op_pos = blob.find("\"op\"", name_end);
    op_pos = blob.find('"', op_pos + 4);
    auto op_end = blob.find('"', op_pos + 1);
    item.op = blob.substr(op_pos + 1, op_end - op_pos - 1);
    auto gen_pos = blob.find("\"generation\"", op_end);
    if (gen_pos != std::string::npos && gen_pos < blob.find('{', pos + 1)) {
      gen_pos = blob.find(':', gen_pos);
      item.generation = std::stoi(blob.substr(gen_pos + 1));
    }
    auto act_pos = blob.find("\"active\"", op_end);
    if (act_pos != std::string::npos && act_pos < blob.find('}', pos)) {
      act_pos = blob.find('"', act_pos + 8);
      auto act_end = blob.find('"', act_pos + 1);
      item.active = blob.substr(act_pos + 1, act_end - act_pos - 1);
    }
    items.push_back(item);
    pos = op_end + 1;
  }
  std::sort(items.begin(), items.end(), [](const entry& a, const entry& b) {
    return a.seq < b.seq;
  });
  return items;
}

void bump_row(view::Row& row, const entry& item) {
  if (item.generation > 0) {
    row.generation = item.generation;
  }
  if (!item.active.empty()) {
    row.active = item.active;
  }
  row.source = "log";
}

void tombstone_row(view::Row& row) {
  row.removed = true;
  row.span = "removed";
}
}
namespace ops {
std::vector<view::Row> apply_log(const std::vector<view::Row>& base, const std::string& root) {
  auto items = read_log(root);
  std::vector<view::Row> rows = base;
  for (const auto& item : items) {
    for (auto& row : rows) {
      if (row.run != item.run || row.name != item.name) {
        continue;
      }
      if (item.op == "touch") {
        row.source = "log";
      } else if (item.op == "bump") {
        bump_row(row, item);
      } else if (item.op == "tombstone") {
        tombstone_row(row);
      }
    }
  }
  return rows;
}
}
""")

Path('app/ops/reconcile.cpp').write_text(r"""#include "ops/reconcile.hpp"
#include <fstream>
namespace {
struct mark {
  std::string run;
  std::string name;
};

std::vector<mark> read_marks(const std::string& root) {
  std::ifstream in(root + "/fixtures/tombstones.json");
  if (!in) {
    return {};
  }
  std::string blob((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
  std::vector<mark> marks;
  size_t pos = 0;
  while ((pos = blob.find("\"run\"", pos)) != std::string::npos) {
    mark item;
    auto run_pos = blob.find('"', pos + 5);
    auto run_end = blob.find('"', run_pos + 1);
    item.run = blob.substr(run_pos + 1, run_end - run_pos - 1);
    auto name_pos = blob.find("\"name\"", run_end);
    name_pos = blob.find('"', name_pos + 6);
    auto name_end = blob.find('"', name_pos + 1);
    item.name = blob.substr(name_pos + 1, name_end - name_pos - 1);
    marks.push_back(item);
    pos = name_end + 1;
  }
  return marks;
}
}
namespace ops {
std::vector<view::Row> merge_tombstones(const std::vector<view::Row>& rows, const std::string& root) {
  auto marks = read_marks(root);
  std::vector<view::Row> out = rows;
  for (const auto& mark : marks) {
    for (auto& row : out) {
      if (row.run == mark.run && row.name == mark.name) {
        row.removed = true;
        row.span = "removed";
      }
    }
  }
  return out;
}

std::vector<view::Row> finalize_batch(const std::vector<view::Row>& rows) {
  return rows;
}
}
""")

Path('app/core/ledger.cpp').write_text(r"""#include "core/ledger.hpp"
#include <algorithm>
namespace {
std::string pick_owner(const view::Row& row) {
  if (row.span == "crossed" && !row.active.empty()) {
    return row.active;
  }
  if (row.source == "log" && !row.active.empty()) {
    return row.active;
  }
  if (!row.pack.empty()) {
    return row.pack;
  }
  if (!row.summary.empty()) {
    return row.summary;
  }
  return row.active.empty() ? "unknown" : row.active;
}

std::string pick_source(const view::Row& row, const std::string& owner) {
  if (row.source == "log" && owner == row.active) {
    return "log";
  }
  if (row.span == "crossed" && owner == row.active) {
    return "active";
  }
  if (owner == row.pack) {
    return "bundle";
  }
  if (owner == row.summary) {
    return "summary";
  }
  return "active";
}
}
namespace core {
std::map<std::string, view::Row> fold_units(const std::vector<view::Row>& items, const std::string& mark) {
  std::map<std::string, view::Row> folded;
  for (auto row : items) {
    if (!mark.empty() && row.run != mark) {
      continue;
    }
    row.owner = pick_owner(row);
    row.source = pick_source(row, row.owner);
    row.line = row.chain + ":" + row.owner;
    auto key = view::record_key(row);
    auto prior = folded.find(key);
    if (prior == folded.end() || row.generation > prior->second.generation) {
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
""")

Path('app/ops/tape.cpp').write_text(r"""#include "ops/tape.hpp"
namespace ops {
std::vector<view::Row> advance_span(const std::vector<view::Row>& batch, const std::string& marker) {
  std::vector<view::Row> out;
  for (auto row : batch) {
    if (!marker.empty() && row.run != marker) {
      continue;
    }
    if (row.removed || row.span == "removed") {
      continue;
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
""")

Path('app/ops/wash.cpp').write_text(r"""#include "ops/wash.hpp"
namespace ops {
std::vector<view::Row> sweep_local(const std::vector<view::Row>& rows) {
  return rows;
}
}
""")

Path('app/io/store.cpp').write_text(r"""#include "io/store.hpp"
namespace io {
view::Artifact bind_entry(const std::string& slot, const view::Row& payload) {
  view::Artifact artifact;
  artifact.run = payload.run;
  artifact.name = payload.name;
  artifact.generation = payload.generation;
  artifact.owner = payload.owner.empty() ? payload.active : payload.owner;
  if (artifact.owner.empty()) {
    artifact.owner = payload.pack;
  }
  artifact.line = payload.chain + ":" + artifact.owner;
  std::string base = slot.empty() ? "local" : slot;
  artifact.file = base + "/" + payload.file;
  return artifact;
}
std::vector<view::Artifact> bind_all(const std::vector<view::Row>& rows) {
  std::vector<view::Artifact> artifacts;
  for (const auto& row : rows) {
    artifacts.push_back(bind_entry("local", row));
  }
  return artifacts;
}
}
""")

Path('app/emit/frame.cpp').write_text(r"""#include "emit/frame.hpp"
#include <sstream>
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
    const std::string src = r.source.empty() ? label : r.source;
    const std::string active = r.active.empty() ? r.owner : r.active;
    const std::string pack = r.pack.empty() ? r.owner : r.pack;
    const std::string summary = r.summary.empty() ? pack : r.summary;
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
""")

Path('app/emit/write.cpp').write_text(r"""#include "emit/write.hpp"
#include "emit/frame.hpp"
#include "ops/tape.hpp"
#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <openssl/sha.h>
#include <sstream>
#include <string>
#include <vector>
namespace {
int read_anchor(const std::string& root) {
  std::ifstream in(root + "/fixtures/ledger_seed.json");
  std::string blob((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
  auto pos = blob.find("\"anchor\"");
  if (pos == std::string::npos) {
    return 0;
  }
  pos = blob.find(':', pos);
  return std::stoi(blob.substr(pos + 1));
}

std::string sha256_hex(const std::string& text) {
  unsigned char digest[SHA256_DIGEST_LENGTH];
  SHA256(reinterpret_cast<const unsigned char*>(text.data()), text.size(), digest);
  std::ostringstream out;
  for (unsigned char byte : digest) {
    out << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte);
  }
  return out.str();
}

std::string stable_digest_for(const std::vector<view::Row>& rows, int anchor) {
  std::vector<std::string> segments;
  for (const auto& row : rows) {
    if (row.span == "removed") {
      continue;
    }
    std::ostringstream seg;
    seg << row.run << '|' << row.name << '|' << row.generation << '|' << row.owner << '|' << row.line << '|' << row.span << "|anchor:" << anchor;
    segments.push_back(seg.str());
  }
  std::sort(segments.begin(), segments.end());
  std::ostringstream joined;
  for (size_t i = 0; i < segments.size(); ++i) {
    if (i) {
      joined << '\n';
    }
    joined << segments[i];
  }
  return sha256_hex(joined.str());
}

std::string next_session_span() {
  const std::filesystem::path counter_path = "/tmp/mig_obs_session.seq";
  long long value = 0;
  if (std::filesystem::exists(counter_path)) {
    std::ifstream in(counter_path);
    in >> value;
  }
  value += 1;
  std::ofstream out(counter_path, std::ios::trunc);
  out << value;
  return sha256_hex("session:" + std::to_string(value)).substr(0, 8);
}
}
namespace emit {
void emit_report(const std::string& target, const std::map<std::string, std::vector<std::string>>& runs, const std::vector<view::Artifact>& artifacts, const std::vector<view::Row>& ordered_rows) {
  const int anchor = read_anchor("/app/environment/app");
  const std::string stable = stable_digest_for(ordered_rows, anchor);
  const std::string session = next_session_span();
  std::filesystem::create_directories(std::filesystem::path(target).parent_path());
  std::ofstream report_stream(target);
  report_stream << "{\n  \"runs\": [\n";
  bool first_run = true;
  for (const auto& entry : runs) {
    if (!first_run) {
      report_stream << ",\n";
    }
    first_run = false;
    std::string mode = entry.first == "later" ? "replay" : entry.first == "sweep" ? "cleanup" : entry.first == "repeat" ? "rerun" : "clean";
    report_stream << "    {\"run_id\":\"" << view::escape_json(entry.first) << "\",\"mode\":\"" << view::escape_json(mode) << "\",\"steps\":[";
    auto steps = ops::run_steps(mode);
    for (size_t i = 0; i < steps.size(); ++i) {
      if (i) {
        report_stream << ",";
      }
      report_stream << "\"" << view::escape_json(steps[i]) << "\"";
    }
    report_stream << "],\"records\":[";
    for (size_t i = 0; i < entry.second.size(); ++i) {
      if (i) {
        report_stream << ",";
      }
      report_stream << entry.second[i];
    }
    report_stream << "]}";
  }
  report_stream << "\n  ],\n  \"artifacts\": [";
  for (size_t i = 0; i < artifacts.size(); ++i) {
    if (i) {
      report_stream << ",";
    }
    report_stream << artifact_json(artifacts[i]);
  }
  report_stream << "],\n  \"fingerprints\": {\"stable_digest\":\"" << stable << "\",\"session_span_id\":\"" << session << "\"}\n}\n";
}
}
""")
PYFIX
