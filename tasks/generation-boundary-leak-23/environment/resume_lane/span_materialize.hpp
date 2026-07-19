#pragma once
#include <cstddef>
#include <cstdint>
#include <span>
#include <utility>

std::pair<int, int> op_span_y(std::span<const std::byte> buf);
