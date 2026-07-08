pub fn bump_counter(c: &mut u32) {
    *c = c.wrapping_add(1);
}
