use crate::family::OperatorBlock;

pub struct MeshView {
    pub rhs: [f64; 4],
}

impl MeshView {
    pub fn canonical_rhs() -> Self {
        Self {
            rhs: [1.0, 0.0, 0.0, 0.0],
        }
    }

    pub fn residual_norm(&self, op: OperatorBlock, x: [f64; 4]) -> f64 {
        let ax = op.apply(x);
        let mut s = 0.0;
        for i in 0..4 {
            let r = ax[i] - self.rhs[i];
            s += r * r;
        }
        s.sqrt()
    }
}
