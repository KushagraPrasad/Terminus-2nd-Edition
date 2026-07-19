#pragma once
#include <cstdint>
#include <vector>

// Canonical merge stamp for paired resume markers (see runtime.toml contract).
std::vector<std::uint8_t> fx_merge_z(int t_left, int t_right);
