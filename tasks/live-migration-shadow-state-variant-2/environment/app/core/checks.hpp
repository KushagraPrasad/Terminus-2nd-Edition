#pragma once
#include "core/types.hpp"
#include <string>
#include <vector>
namespace core { bool rows_are_named(const std::vector<view::Row>& rows); std::string describe_rows(const std::vector<view::Row>& rows); }
