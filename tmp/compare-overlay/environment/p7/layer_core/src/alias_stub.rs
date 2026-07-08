use crate::family::OperatorBlock;

pub fn gram_schmidt_step(v: [f64; 4], basis: &[[f64; 4]; 3], used: usize) -> [f64; 4] {
    let mut w = v;
    for j in 0..used.min(3) {
        let b = basis[j];
        let mut dot = 0.0;
        let mut nn = 0.0;
        for i in 0..4 {
            dot += w[i] * b[i];
            nn += b[i] * b[i];
        }
        let c = if nn > 1e-12 { dot / nn } else { 0.0 };
        for i in 0..4 {
            w[i] -= c * b[i];
        }
    }
    let norm = (w[0] * w[0] + w[1] * w[1] + w[2] * w[2] + w[3] * w[3]).sqrt();
    if norm > 1e-12 {
        for i in 0..4 {
            w[i] /= norm;
        }
    }
    let _ = OperatorBlock::diag4(1.0);
    w
}
