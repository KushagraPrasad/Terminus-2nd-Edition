pub struct ProbeScratch {
    pub buf: [f64; 4],
}

impl ProbeScratch {
    pub fn new() -> Self {
        Self { buf: [0.0; 4] }
    }
}
