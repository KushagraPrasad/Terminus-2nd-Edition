#pragma once
#include "core/types.hpp"
#include <map>
#include <string>
#include <vector>
namespace app {
struct ReportParts {
  std::map<std::string, std::vector<std::string>> runs;
  std::vector<view::Artifact> artifacts;
  std::vector<view::Row> ordered_rows;
};
ReportParts build_parts(const std::string& root);
}
