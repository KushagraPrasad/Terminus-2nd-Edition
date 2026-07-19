#include "core/checks.hpp"
#include <sstream>
namespace core {
bool rows_are_named(const std::vector<view::Row>& rows) { for (const auto& row : rows) { if (row.name.empty() || row.run.empty()) return false; } return true; }
std::string describe_rows(const std::vector<view::Row>& rows) { std::ostringstream out; out << rows.size() << " rows"; if (!rows.empty()) out << " first=" << rows.front().name; return out.str(); }
}
