#include "ops/probe.hpp"
#include <sstream>
namespace ops { std::string probe_summary(const std::vector<view::Row>& rows) { std::ostringstream out; out << "rows=" << rows.size(); if (!rows.empty()) out << " sample=" << rows.back().name; return out.str(); } }
