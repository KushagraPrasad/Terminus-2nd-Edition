#pragma once
#include "core/types.hpp"
#include <map>
#include <string>
#include <vector>
namespace emit {
void emit_report(const std::string& target, const std::map<std::string, std::vector<std::string>>& runs, const std::vector<view::Artifact>& artifacts, const std::vector<view::Row>& ordered_rows);
}
