#include "core/phase_gate.hpp"

bool phase_qr_n(const TickFrame& tf, uint64_t edge_mark) {
    if (tf.stable_span == 0) {
        return false;
    }
    return (tf.visible_ticks >= edge_mark) && (tf.settled_ticks < edge_mark);
}
