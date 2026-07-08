#[derive(Clone, Copy, Debug, PartialEq)]
pub struct FamilySpec {
    pub tag: u32,
    pub diag_scale: f64,
}

impl FamilySpec {
    pub fn block(self) -> OperatorBlock {
        OperatorBlock::diag4(self.diag_scale)
    }
}

#[derive(Clone, Copy, Debug)]
pub struct OperatorBlock {
    pub d0: f64,
    pub d1: f64,
    pub d2: f64,
    pub d3: f64,
}

impl OperatorBlock {
    pub fn diag4(scale: f64) -> Self {
        Self {
            d0: scale,
            d1: scale,
            d2: scale,
            d3: scale * 1.02,
        }
    }

    pub fn apply(self, v: [f64; 4]) -> [f64; 4] {
        [
            self.d0 * v[0],
            self.d1 * v[1],
            self.d2 * v[2],
            self.d3 * v[3],
        ]
    }
}
