#!/bin/bash
set -euo pipefail
cd /app/environment

fix_a3() {
cat > a3/p1.go <<'EOF'
package a3

var PivM31 = piv_m31

func piv_m31(rows []map[string]any, marks []map[string]any, cap int) map[string]any {
	limit := float64(cap)
	seenMarks := map[string]float64{}
	for _, m := range marks {
		label, _ := m["label"].(string)
		g, ok := m["generation"].(float64)
		if !ok {
			continue
		}
		if label != "" {
			if prev, ok := seenMarks[label]; !ok || g > prev {
				seenMarks[label] = g
			}
		}
		if g > limit {
			limit = g
		}
	}
	kept := make([]map[string]any, 0, len(rows))
	seenRows := map[string]float64{}
	for _, r := range rows {
		id, _ := r["id"].(string)
		if id == "" {
			continue
		}
		g, _ := r["generation"].(float64)
		active, ok := r["active"].(bool)
		if !ok {
			active = true
		}
		if !active || g > limit {
			continue
		}
		if prev, ok := seenRows[id]; ok && g <= prev {
			continue
		}
		seenRows[id] = g
		kept = append(kept, r)
	}
	return map[string]any{"rows": kept, "limit": limit, "marks": marks, "mark_generations": seenMarks}
}
EOF
}

fix_b7() {
cat > b7/p1.go <<'EOF'
package b7

var ArcR8 = arc_r8

func arc_r8(left map[string]any, right map[string]any, opts map[string]any) map[string]any {
	rows, _ := left["rows"].([]map[string]any)
	rank := map[string]float64{}
	if raw, ok := right["rank"].(map[string]any); ok {
		for k, v := range raw {
			if n, ok := v.(float64); ok {
				rank[k] = n
			}
		}
	}
	chosen := map[string]map[string]any{}
	for _, r := range rows {
		id, _ := r["id"].(string)
		if id == "" {
			continue
		}
		active, ok := r["active"].(bool)
		if ok && !active {
			continue
		}
		cur, ok := chosen[id]
		if !ok {
			chosen[id] = r
			continue
		}
		cg, _ := cur["generation"].(float64)
		rg, _ := r["generation"].(float64)
		cs, _ := cur["source"].(string)
		rs, _ := r["source"].(string)
		if rg > cg || (rg == cg && rank[rs] > rank[cs]) {
			chosen[id] = r
		}
	}
	out := make([]map[string]any, 0, len(chosen))
	ids := make([]string, 0, len(chosen))
	for id := range chosen {
		ids = append(ids, id)
	}
	for len(ids) > 0 {
		pick := 0
		for i := 1; i < len(ids); i++ {
			if ids[i] < ids[pick] {
				pick = i
			}
		}
		out = append(out, chosen[ids[pick]])
		ids = append(ids[:pick], ids[pick+1:]...)
	}
	return map[string]any{"records": out, "rank": right["rank"], "label": opts["label"]}
}
EOF
}

fix_c4() {
cat > c4/p1.go <<'EOF'
package c4

var MeshV6 = mesh_v6

func mesh_v6(items []map[string]any, memo map[string]any) map[string]any {
	label, _ := memo["label"].(string)
	if label == "" {
		label = "unknown"
	}
	max := 0.0
	counts := map[string]int{}
	ids := map[string]bool{}
	for _, item := range items {
		if g, _ := item["generation"].(float64); g > max {
			max = g
		}
		if source, _ := item["source"].(string); source != "" {
			counts[source]++
		}
		if id, _ := item["id"].(string); id != "" {
			ids[id] = true
		}
	}
	transitions := []map[string]any{{
		"label":          label,
		"record_count":   len(items),
		"max_generation": max,
		"source_counts":  counts,
		"distinct_ids":   len(ids),
	}}
	return map[string]any{"transitions": transitions, "max_generation": max, "source_counts": counts}
}
EOF
}

fix_d9() {
cat > d9/p1.go <<'EOF'
package d9

import (
	"fmt"
	"sort"
	"strings"
)

var SlotH4 = slot_h4

func slot_h4(bundle map[string]any, target string) map[string]any {
	recs, _ := bundle["records"].([]map[string]any)
	parts := make([]string, 0, len(recs))
	ids := map[string]bool{}
	for _, r := range recs {
		id, _ := r["id"].(string)
		source, _ := r["source"].(string)
		g, _ := r["generation"].(float64)
		value, _ := r["value"].(float64)
		if id == "" || source == "" {
			continue
		}
		ids[id] = true
		parts = append(parts, fmt.Sprintf("%s:%d:%d:%s", id, int(g), int(value), source))
	}
	sort.Strings(parts)
	digest := strings.Join(parts, "|")
	return map[string]any{
		"target":       target,
		"state_digest": digest,
		"record_count": len(recs),
		"distinct_ids": len(ids),
		"note":         fmt.Sprintf("%d:%d", len(parts), len(digest)),
	}
}
EOF
}

fix_e5() {
cat > e5/p1.go <<'EOF'
package main

import (
	"flag"
	"fmt"
	"os"

	"lcx/a3"
	"lcx/b7"
	"lcx/c4"
	"lcx/d9"
	"lcx/j4"
)

func main() {
	out := flag.String("write-report", "/app/output/ledger_compaction_report.json", "write report path")
	flag.Parse()
	if err := run(*out); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run(out string) error {
	alpha, err := j4.ReadJSON("/app/environment/f6/r1.json")
	if err != nil {
		return err
	}
	beta, err := j4.ReadJSON("/app/environment/f6/r2.json")
	if err != nil {
		return err
	}
	meta, err := j4.ReadJSON("/app/environment/f6/r3.json")
	if err != nil {
		return err
	}
	r1, err := j4.ReadJSON("/app/environment/g8/r1.json")
	if err != nil {
		return err
	}
	r2, err := j4.ReadJSON("/app/environment/g8/r2.json")
	if err != nil {
		return err
	}

	labels := []string{"clean", "restart", "rollback", "idempotent"}
	runs := make([]map[string]any, 0, len(labels))
	allTransitions := []map[string]any{}
	for _, label := range labels {
		rows := append([]map[string]any{}, rowsFrom(alpha["rows"])...)
		rows = append(rows, rowsFrom(beta["rows"])...)
		marks := append([]map[string]any{}, rowsFrom(alpha["marks"])...)
		if label == "restart" || label == "idempotent" {
			rows = append(rows, rowsFrom(r1["rows"])...)
			if mark, ok := r1["mark"].(map[string]any); ok {
				marks = append(marks, mark)
			}
		}
		if label == "rollback" || label == "idempotent" {
			rows = append(rows, rowsFrom(r2["rows"])...)
			if mark, ok := r2["mark"].(map[string]any); ok {
				marks = append(marks, mark)
			}
		}

		view := a3.PivM31(rows, marks, 3)
		merged := b7.ArcR8(view, meta, map[string]any{"label": label})
		recs := mapRows(merged["records"])
		summary := c4.MeshV6(recs, map[string]any{"label": label})
		written := d9.SlotH4(map[string]any{"records": recs}, out)
		provenance := []map[string]any{}
		for _, r := range recs {
			provenance = append(provenance, map[string]any{
				"id":         r["id"],
				"source":     r["source"],
				"generation": r["generation"],
				"value":      r["value"],
			})
		}
		transitions := mapRows(summary["transitions"])
		allTransitions = append(allTransitions, transitions...)
		runs = append(runs, map[string]any{
			"label":        label,
			"records":      recs,
			"provenance":   provenance,
			"state_digest": written["state_digest"],
			"transitions":  transitions,
		})
	}

	report := map[string]any{
		"schema_version": 1,
		"command":        "go run /app/environment/e5 --write-report /app/output/ledger_compaction_report.json",
		"runs":           runs,
		"artifacts": []map[string]any{
			{"path": "/app/environment/f6/r1.json", "row_count": len(rowsFrom(alpha["rows"]))},
			{"path": "/app/environment/f6/r2.json", "row_count": len(rowsFrom(beta["rows"]))},
			{"path": "/app/environment/g8/r1.json", "row_count": len(rowsFrom(r1["rows"]))},
			{"path": "/app/environment/g8/r2.json", "row_count": len(rowsFrom(r2["rows"]))},
		},
		"state_transitions": allTransitions,
	}
	return j4.WriteJSON(out, report)
}
EOF
}

fix_a3
fix_b7
fix_c4
fix_d9
fix_e5
