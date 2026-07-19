#pragma once
#include "core/types.hpp"
#include <map>
#include <string>
#include <vector>
namespace emit { std::vector<std::string> shape_rows(const std::string& label, const std::map<std::string, view::Row>& frame, const std::vector<std::string>& order); std::vector<std::string> rows_for_run(const std::string& label, const std::map<std::string, view::Row>& frame); std::string artifact_json(const view::Artifact& artifact); }
