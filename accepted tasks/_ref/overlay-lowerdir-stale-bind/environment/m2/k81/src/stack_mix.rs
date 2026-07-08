use yb44::{merge_pack, PackState};

pub fn stack_apply(
    pack: &mut PackState,
    tag_a: u64,
    tag_b: u64,
    incoming: &[[f64; 4]; 3],
) -> [[f64; 4]; 3] {
    merge_pack(pack, tag_a, tag_b, 3, incoming)
}
