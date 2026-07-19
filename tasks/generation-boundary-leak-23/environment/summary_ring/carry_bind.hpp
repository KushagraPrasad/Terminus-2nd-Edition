#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <span>

std::array<std::uint8_t, 8> reseq_q(int epoch, std::span<const std::byte> carry);
