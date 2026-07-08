//! Overlay bind rematerialization sweep report: writes JSON with `rows` and `summary`. The summary `trace_digest`
//! field is eight lowercase hex digits from the sorted row keys: each row becomes a single
//! pipe-separated string of `scenario_id`, the three booleans as 0 or 1, `drift_code`, and
//! `facet_hex`; lines are sorted lexicographically, joined with newlines, then reduced with
//! a wrapping 64-bit sum adding `(index + 1) * code_unit` for every UTF-8 code unit in the
//! joined text, masking the low 32 bits for the final formatting.
//!
//! A healthy emission has every `layer_ok`, `gen_ok`, and `mount_ok` field set to true and
//! every `drift_code` field at zero; those are the shapes the verifier expects when
//! `sync_status` reads `settled`. Summary `tier_span` is defined as the maximum absolute
//! `drift_code` across emitted rows. The end-of-ladder subspace error norm must fall below 1e-2
//! for `drift_code` to read zero for that scenario.
//! For the shipped case-lane table in `docs/case_lane_ids.txt`, the known-good repaired emission
//! has summary `trace_digest` equal to `001765f2`.

use layer_core::family::FamilySpec;
use layer_core::mesh::MeshView;
use layer_core::row_help::hex16;
mod gate_mux;
mod stack_mix;
mod step_key;

use yb44::PackState;
use gate_mux::mux_combine;
use stack_mix::stack_apply;
use step_key::step_key;
use serde::Serialize;
use std::cell::Cell;

const _: &str = include_str!("../../../data/ladder.toml");

use std::fs;
use std::path::Path;

#[derive(Clone, Serialize)]
struct RowOut {
    scenario_id: String,
    layer_ok: bool,
    gen_ok: bool,
    mount_ok: bool,
    drift_code: i32,
    facet_hex: String,
}

#[derive(Serialize)]
struct SummaryOut {
    sync_status: String,
    rows_total: usize,
    tier_span: i32,
    trace_digest: String,
}

#[derive(Serialize)]
struct Report {
    rows: Vec<RowOut>,
    summary: SummaryOut,
}

fn family_from_tag(tag: u32) -> FamilySpec {
    if tag == 0 {
        FamilySpec {
            tag: 0,
            diag_scale: 1.0,
        }
    } else {
        FamilySpec {
            tag: 1,
            diag_scale: 2.7,
        }
    }
}

fn build_incoming(fam: FamilySpec) -> [[f64; 4]; 3] {
    let op = fam.block();
    let seeds = [
        [1.0, 0.1, 0.02, 0.0],
        [0.1, 1.0, 0.03, 0.01],
        [0.02, 0.03, 1.0, 0.04],
    ];
    let mut out = [[0.0f64; 4]; 3];
    for k in 0..3 {
        out[k] = layer_core::alias_stub::gram_schmidt_step(seeds[k], &out, k);
        let _ = op.apply(out[k]);
    }
    out
}

fn subspace_residual(op: layer_core::family::OperatorBlock, q: &[[f64; 4]; 3], rhs: [f64; 4]) -> f64 {
    let aq: [[f64; 4]; 3] = [op.apply(q[0]), op.apply(q[1]), op.apply(q[2])];
    let mut m = [[0.0f64; 3]; 3];
    let mut rvec = [0.0f64; 3];
    for i in 0..3 {
        for j in 0..3 {
            let mut s = 0.0;
            for t in 0..4 {
                s += aq[i][t] * aq[j][t];
            }
            m[i][j] = s;
        }
        let mut s = 0.0;
        for t in 0..4 {
            s += aq[i][t] * rhs[t];
        }
        rvec[i] = s;
    }
    let y = solve3(m, rvec);
    let mut ax = [0.0f64; 4];
    for t in 0..4 {
        ax[t] = aq[0][t] * y[0] + aq[1][t] * y[1] + aq[2][t] * y[2];
    }
    let mut acc = 0.0;
    for t in 0..4 {
        let e = ax[t] - rhs[t];
        acc += e * e;
    }
    acc.sqrt()
}

fn solve3(a: [[f64; 3]; 3], b: [f64; 3]) -> [f64; 3] {
    let mut aug = [[0.0f64; 4]; 3];
    for i in 0..3 {
        for j in 0..3 {
            aug[i][j] = a[i][j];
        }
        aug[i][3] = b[i];
    }
    for col in 0..3 {
        let mut piv = col;
        for r in col + 1..3 {
            if aug[r][col].abs() > aug[piv][col].abs() {
                piv = r;
            }
        }
        if aug[piv][col].abs() < 1e-14 {
            continue;
        }
        if piv != col {
            aug.swap(col, piv);
        }
        let div = aug[col][col];
        for j in col..4 {
            aug[col][j] /= div;
        }
        for r in 0..3 {
            if r == col {
                continue;
            }
            let f = aug[r][col];
            for j in col..4 {
                aug[r][j] -= f * aug[col][j];
            }
        }
    }
    [aug[0][3], aug[1][3], aug[2][3]]
}

fn run_scenario(id: &str, ladder: &[(usize, u32)]) -> RowOut {
    let mesh = MeshView::canonical_rhs();
    let mut pack = PackState::fresh();
    let mut prev_fam: u32 = ladder[0].1;
    let mut stamps: Vec<u64> = Vec::new();
    let mut gate_masks: Vec<u32> = Vec::new();
    let mut last_fam = prev_fam;
    let mut last_q = [[0.0f64; 4]; 3];

    for &(step_ix, fam_ix) in ladder {
        let fam = family_from_tag(fam_ix);
        let stamp = step_key(step_ix, fam_ix, prev_fam);
        let tag_a = (step_ix as u64) << 32;
        let tag_b = ((fam_ix as u64) << 16) | (prev_fam as u64);
        let incoming = build_incoming(fam);
        last_q = stack_apply(&mut pack, tag_a, tag_b, &incoming);
        let touched = Cell::new(false);
        let mask = mux_combine(
            || {
                touched.set(true);
            },
            || {
                let _ = touched.get();
            },
        );
        gate_masks.push(mask);
        stamps.push(stamp);
        prev_fam = fam_ix;
        last_fam = fam_ix;
        let _ = mesh.residual_norm(fam.block(), incoming[0]);
    }

    let fam_last = family_from_tag(last_fam);
    let op = fam_last.block();
    let res = subspace_residual(op, &last_q, mesh.rhs);
    let drift_code = if res < 1e-2 { 0 } else { 1 };
    let layer_ok = drift_code == 0;

    let mut gen_ok = true;
    for i in 1..stamps.len() {
        if stamps[i] < stamps[i - 1] {
            gen_ok = false;
            break;
        }
        let fam_prev = ladder[i - 1].1;
        let fam_cur = ladder[i].1;
        if fam_prev != fam_cur && stamps[i] == stamps[i - 1] {
            gen_ok = false;
        }
    }

    let mount_ok = gate_masks.iter().all(|&m| m == 1);

    RowOut {
        scenario_id: id.to_string(),
        layer_ok,
        gen_ok,
        mount_ok,
        drift_code,
        facet_hex: hex16(*stamps.last().unwrap_or(&0)),
    }
}

fn digest(rows: &[RowOut]) -> String {
    let mut parts = Vec::new();
    for row in rows {
        parts.push(format!(
            "{}|{}|{}|{}|{}|{}",
            row.scenario_id,
            row.layer_ok as u8,
            row.gen_ok as u8,
            row.mount_ok as u8,
            row.drift_code,
            row.facet_hex
        ));
    }
    parts.sort();
    let payload = parts.join("\n");
    let mut total: u64 = 0;
    for (idx, ch) in payload.chars().enumerate() {
        total = total.wrapping_add(((idx + 1) as u64).wrapping_mul(ch as u64));
    }
    format!("{:08x}", total & 0xffff_ffff)
}

fn main() {
    let scenarios: Vec<(&str, Vec<(usize, u32)>)> = vec![
        (
            "lowerdir",
            vec![(0, 0), (0, 1), (1, 1)],
        ),
        (
            "lowerdir_echo",
            vec![(0, 0), (0, 1), (1, 1)],
        ),
        (
            "upper",
            vec![(0, 0), (1, 0), (1, 1), (2, 1)],
        ),
        (
            "upper_echo",
            vec![(0, 0), (1, 0), (1, 1), (2, 1)],
        ),
        (
            "worker",
            vec![(0, 0), (2, 0), (2, 1)],
        ),
        (
            "worker_echo",
            vec![(0, 0), (2, 0), (2, 1)],
        ),
    ];

    let mut rows = Vec::new();
    for (id, ladder) in scenarios {
        rows.push(run_scenario(id, &ladder));
    }

    let all_ok = rows.iter().all(|r| r.layer_ok && r.gen_ok && r.mount_ok);
    let gen_span = rows
        .iter()
        .map(|r| r.drift_code.abs())
        .max()
        .unwrap_or(0);

    let report = Report {
        summary: SummaryOut {
            sync_status: if all_ok {
                "settled".to_string()
            } else {
                "split".to_string()
            },
            rows_total: rows.len(),
            tier_span: gen_span,
            trace_digest: digest(&rows),
        },
        rows,
    };

    let out_dir = Path::new("/app/output");
    let _ = fs::create_dir_all(out_dir);
    let path = out_dir.join("layer_report.json");
    fs::write(path, serde_json::to_string_pretty(&report).unwrap()).unwrap();
}
