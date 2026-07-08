use yc55::fold_key;

pub fn step_key(step_ix: usize, fam_ix: u32, prev: u32) -> u64 {
    fold_key(step_ix, fam_ix, prev)
}
