pub fn clip_u32(x: u32) -> u32 {
    x.min(1_000_000)
}
