#pragma once
#include "core/types.hpp"
#include <string>
#include <vector>
namespace io { view::Artifact bind_entry(const std::string& slot, const view::Row& payload); std::vector<view::Artifact> bind_all(const std::vector<view::Row>& rows); }
