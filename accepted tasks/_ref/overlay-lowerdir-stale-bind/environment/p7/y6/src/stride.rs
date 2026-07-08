pub fn step_1<F: FnMut(), G: FnMut()>(gate_first: bool, mut side: F, mut gate: G) -> u32 {
    if gate_first {
        gate();
        side();
        0u32
    } else {
        side();
        gate();
        1u32
    }
}

