#pragma once
#include "core/types.hpp"
#include <string>
#include <vector>
namespace ops { std::vector<view::Row> advance_span(const std::vector<view::Row>& batch, const std::string& marker); std::vector<std::string> run_steps(const std::string& mode); }
