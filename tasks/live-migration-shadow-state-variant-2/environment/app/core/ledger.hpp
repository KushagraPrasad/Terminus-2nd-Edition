#pragma once
#include "core/types.hpp"
#include <map>
#include <string>
#include <vector>
namespace core {
std::map<std::string, view::Row> fold_units(const std::vector<view::Row>& items, const std::string& mark);
std::vector<view::Row> order_rows(const std::map<std::string, view::Row>& frame);
}
