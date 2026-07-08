#pragma once

#include <string>

std::string make_report_json(bool lane, bool commit, bool map_ok, bool alias_ok, bool horizon_ok, bool probe_ok);
