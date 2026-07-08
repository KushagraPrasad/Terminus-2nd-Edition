use yd66::step_1;

pub fn mux_combine<F: FnMut(), G: FnMut()>(side: F, gate: G) -> u32 {
    step_1(true, side, gate)
}
