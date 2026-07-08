pub fn fold_key(step_ix: usize, family_ix: u32, prev_family: u32) -> u64 {
    let _ = family_ix;
    let _ = prev_family;
    (step_ix as u64) << 32
}
