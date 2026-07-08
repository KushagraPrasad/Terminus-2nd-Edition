#[derive(Clone, Debug)]
pub struct PackState {
    last_a: u64,
    last_b: u64,
    storage: [[f64; 4]; 3],
}

impl PackState {
    pub fn fresh() -> Self {
        Self {
            last_a: u64::MAX,
            last_b: u64::MAX,
            storage: [[0.0; 4]; 3],
        }
    }
}

pub fn merge_pack(
    state: &mut PackState,
    stamp_a: u64,
    stamp_b: u64,
    dim_m: usize,
    incoming: &[[f64; 4]; 3],
) -> [[f64; 4]; 3] {
    let _ = dim_m;
    if state.last_a != stamp_a {
        state.storage = *incoming;
        state.last_a = stamp_a;
        state.last_b = stamp_b;
    } else if state.last_b != stamp_b {
        state.last_b = stamp_b;
    }
    state.storage
}
