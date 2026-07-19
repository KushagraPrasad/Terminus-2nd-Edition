package main

import (
	"build_engine/dag"
	"build_engine/scheduler"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
)

func main() {
	dbPath := flag.String("db", "build.db", "Path to sqlite db")
	graphPath := flag.String("graph", "action_graph.json", "Path to action graph json")
	manifestPath := flag.String("manifest", "outputs/artifact_manifest.json", "Path to output manifest")
	flag.Parse()

	if flag.NArg() < 1 {
		log.Fatalf("Usage: build_engine <command> [args]")
	}

	cmd := flag.Arg(0)
	switch cmd {
	case "build":
		runBuild(*dbPath, *graphPath, *manifestPath)
	case "clean":
		runClean(*dbPath, *manifestPath)
	default:
		log.Fatalf("Unknown command: %s", cmd)
	}
}

func runBuild(dbPath, graphPath, manifestPath string) {
	db, err := scheduler.InitDB(dbPath)
	if err != nil {
		log.Fatalf("Failed to init DB: %v", err)
	}
	defer db.Close()

	// Load Graph
	graphData, err := os.ReadFile(graphPath)
	if err != nil {
		log.Fatalf("Failed to read graph: %v", err)
	}

	var g struct {
		Edges   []dag.Edge          `json:"edges"`
		Actions []scheduler.Action  `json:"actions"`
	}
	if err := json.Unmarshal(graphData, &g); err != nil {
		log.Fatalf("Failed to parse graph: %v", err)
	}

	// Reconcile graph edges
	dGraph := &dag.DependencyGraph{Edges: nil}
	rows, err := db.Query("SELECT from_node, to_node FROM edges")
	if err == nil {
		for rows.Next() {
			var f, t string
			rows.Scan(&f, &t)
			dGraph.Edges = append(dGraph.Edges, dag.Edge{From: f, To: t})
		}
		rows.Close()
	}

	dGraph.ReconcileEdges(g.Edges)

	// Save back edges
	db.Exec("DELETE FROM edges")
	for _, edge := range dGraph.Edges {
		db.Exec("INSERT INTO edges (from_node, to_node) VALUES (?, ?)", edge.From, edge.To)
	}

	outputsDir := filepath.Dir(manifestPath)
	os.MkdirAll(outputsDir, 0755)

	// Delegate build execution
	scheduler.BuildGraph(db, g.Actions, manifestPath, dbPath)

	// Reconcile database artifacts using graph edges
	activeTargets := map[string]bool{}
	for _, edge := range dGraph.Edges {
		activeTargets[edge.To] = true
	}
	for _, action := range g.Actions {
		activeTargets[action.ID] = true
	}

	rows, err = db.Query("SELECT file_path FROM artifacts")
	if err == nil {
		var toPrune []string
		for rows.Next() {
			var path string
			rows.Scan(&path)
			if !activeTargets[path] {
				toPrune = append(toPrune, path)
			}
		}
		rows.Close()

		for _, p := range toPrune {
			db.Exec("DELETE FROM artifacts WHERE file_path = ?", p)
		}
	}

	fmt.Println("Build complete.")
}

func runClean(dbPath, manifestPath string) {
	os.Remove(dbPath)
	os.Remove(manifestPath)
	outputsDir := filepath.Dir(manifestPath)
	os.RemoveAll(outputsDir)
	fmt.Println("Clean complete.")
}
