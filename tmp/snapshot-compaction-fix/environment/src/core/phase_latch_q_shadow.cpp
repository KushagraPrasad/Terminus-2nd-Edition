#include "core/phase_gate.hpp"

bool phase_latch_q_shadow(const TickFrame& tf) {
    return tf.visible_ticks > 0 && tf.stable_span > 0;
}
