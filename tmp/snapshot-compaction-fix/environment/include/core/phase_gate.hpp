#pragma once

#include <cstdint>

struct TickFrame {
    uint64_t visible_ticks;
    uint64_t settled_ticks;
    uint64_t stable_span;
};

bool phase_qr_n(const TickFrame& tf, uint64_t edge_mark);
