#include "io/store.hpp"
namespace io {
view::Artifact bind_entry(const std::string& slot, const view::Row& payload) {
  view::Artifact artifact;
  artifact.run = payload.run;
  artifact.name = payload.name;
  artifact.generation = payload.generation;
  artifact.owner = payload.pack.empty() ? payload.summary : payload.pack;
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
