pub fn dim_check(m: usize) -> usize {
    m.min(3).max(1)
}
