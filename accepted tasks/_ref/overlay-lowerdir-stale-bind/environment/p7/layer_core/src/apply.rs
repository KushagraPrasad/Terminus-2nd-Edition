pub fn mix_columns(q: &[[f64; 4]; 3], weights: [f64; 3]) -> [f64; 4] {
    let mut out = [0.0; 4];
    for j in 0..4 {
        let mut acc = 0.0;
        for k in 0..3 {
            acc += q[k][j] * weights[k];
        }
        out[j] = acc;
    }
    out
}
