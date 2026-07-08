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
			provenance = append(provenance, map[string]any{"id": r["id"], "source": r["source"], "generation": r["generation"]})
		}
		transitions := mapRows(summary["transitions"])
		allTransitions = append(allTransitions, transitions...)
		runs = append(runs, map[string]any{
			"label": label,
			"records": recs,
			"provenance": provenance,
			"state_digest": written["state_digest"],
			"transitions": transitions,
		})
	}

	report := map[string]any{
		"schema_version": 1,
		"command": "go run /app/environment/e5 --write-report /app/output/ledger_compaction_report.json",
		"runs": runs,
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
