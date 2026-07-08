pub fn push_frame(frames: &mut Vec<u32>, v: u32) {
    frames.push(v);
    if frames.len() > 64 {
        frames.remove(0);
    }
}
