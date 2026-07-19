#!/bin/bash
set -euo pipefail

cd /app/environment

cat > dag/dag.go << 'EOF'
package dag

type Edge struct {
	From string `json:"from"`
	To   string `json:"to"`
}

type DependencyGraph struct {
	Edges []Edge `json:"edges"`
}

func (g *DependencyGraph) ReconcileEdges(newEdges []Edge) error {
	for i := 0; i < len(g.Edges); {
		found := false
		for _, ne := range newEdges {
			if g.Edges[i].From == ne.From && g.Edges[i].To == ne.To {
				found = true
				break
			}
		}
		if !found {
			g.Edges = append(g.Edges[:i], g.Edges[i+1:]...)
			continue
		}
		i++
	}
	return nil
}

func (g *DependencyGraph) HasCycle() bool {
	visited := map[string]int{}
	var visit func(string) bool
	visit = func(item string) bool {
		visited[item] = 1
		for _, edge := range g.Edges {
			if edge.From != item {
				continue
			}
			if visited[edge.To] == 1 {
				return true
			}
			if visited[edge.To] == 0 && visit(edge.To) {
				return true
			}
		}
		visited[item] = 2
		return false
	}
	for _, edge := range g.Edges {
		if visited[edge.From] == 0 && visit(edge.From) {
			return true
		}
	}
	return false
}

func (g *DependencyGraph) Validate() bool {
	return !g.HasCycle()
}
EOF

cat > scheduler/fingerprint.go << 'EOF'
package scheduler

import (
	"crypto/sha256"
	"encoding/hex"
	"os"
	"path/filepath"
	"regexp"
)

type Action struct {
	ID      string   `json:"id"`
	Command string   `json:"command"`
	Inputs  []string `json:"inputs"`
}

func ComputeActionFingerprint(action *Action) (string, error) {
	h := sha256.New()
	h.Write([]byte(action.Command))

	for _, inp := range action.Inputs {
		data, err := os.ReadFile(inp)
		if err != nil {
			h.Write([]byte("absent:" + inp))
			continue
		}

		if filepath.Ext(inp) == ".go" {
			re := regexp.MustCompile(`type\s+\w+\s+interface\s*\{([^}]+)\}`)
			matches := re.FindAllSubmatch(data, -1)
			for _, m := range matches {
				if len(m) > 1 {
					h.Write(m[1])
				}
			}
			continue
		}
		h.Write(data)
	}

	return hex.EncodeToString(h.Sum(nil)), nil
}
EOF

cat > registry/registry.go << 'EOF'
package registry

import (
	"database/sql"
	"encoding/json"
	"os"
	"path/filepath"
)

func SyncRegistry(dbPath string, manifestPath string) error {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return err
	}
	defer db.Close()

	rows, err := db.Query("SELECT file_path, fingerprint FROM artifacts")
	if err != nil {
		return err
	}
	defer rows.Close()

	dbArtifacts := map[string]string{}
	for rows.Next() {
		var path, fp string
		if err := rows.Scan(&path, &fp); err != nil {
			return err
		}
		dbArtifacts[path] = fp
	}

	outputsDir := filepath.Dir(manifestPath)
	if err := os.MkdirAll(outputsDir, 0755); err != nil {
		return err
	}
	files, err := os.ReadDir(outputsDir)
	if err != nil && !os.IsNotExist(err) {
		return err
	}

	for _, file := range files {
		if file.IsDir() || file.Name() == filepath.Base(manifestPath) {
			continue
		}
		if _, exists := dbArtifacts[file.Name()]; !exists {
			if err := os.Remove(filepath.Join(outputsDir, file.Name())); err != nil && !os.IsNotExist(err) {
				return err
			}
		}
	}

	data, err := json.MarshalIndent(dbArtifacts, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(manifestPath, data, 0644)
}
EOF

cat > main.go << 'EOF'
package main

import (
	"build_engine/dag"
	"build_engine/registry"
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

	switch flag.Arg(0) {
	case "build":
		runBuild(*dbPath, *graphPath, *manifestPath)
	case "clean":
		runClean(*dbPath, *manifestPath)
	default:
		log.Fatalf("Unknown command: %s", flag.Arg(0))
	}
}

func runBuild(dbPath, graphPath, manifestPath string) {
	db, err := scheduler.InitDB(dbPath)
	if err != nil {
		log.Fatalf("Failed to init DB: %v", err)
	}
	defer db.Close()

	graphData, err := os.ReadFile(graphPath)
	if err != nil {
		log.Fatalf("Failed to read graph: %v", err)
	}

	var g struct {
		Edges   []dag.Edge         `json:"edges"`
		Actions []scheduler.Action `json:"actions"`
	}
	if err := json.Unmarshal(graphData, &g); err != nil {
		log.Fatalf("Failed to parse graph: %v", err)
	}

	dGraph := &dag.DependencyGraph{}
	rows, err := db.Query("SELECT from_node, to_node FROM edges")
	if err == nil {
		for rows.Next() {
			var f, t string
			if err := rows.Scan(&f, &t); err != nil {
				log.Fatalf("Failed to scan edge: %v", err)
			}
			dGraph.Edges = append(dGraph.Edges, dag.Edge{From: f, To: t})
		}
		rows.Close()
	}

	if err := dGraph.ReconcileEdges(g.Edges); err != nil {
		log.Fatalf("Failed to reconcile graph: %v", err)
	}
	dGraph.Edges = append([]dag.Edge(nil), g.Edges...)
	if !dGraph.Validate() {
		log.Fatalf("Dependency graph contains a cycle")
	}

	if _, err := db.Exec("DELETE FROM edges"); err != nil {
		log.Fatalf("Failed to clear edge table: %v", err)
	}
	for _, edge := range dGraph.Edges {
		if _, err := db.Exec("INSERT OR REPLACE INTO edges (from_node, to_node) VALUES (?, ?)", edge.From, edge.To); err != nil {
			log.Fatalf("Failed to save edge: %v", err)
		}
	}

	outputsDir := filepath.Dir(manifestPath)
	if err := os.MkdirAll(outputsDir, 0755); err != nil {
		log.Fatalf("Failed to create outputs dir: %v", err)
	}

	scheduler.BuildGraph(db, g.Actions, manifestPath, dbPath)

	activeTargets := map[string]bool{}
	for _, edge := range dGraph.Edges {
		activeTargets[edge.To] = true
	}
	for _, action := range g.Actions {
		activeTargets[action.ID] = true
	}

	rows, err = db.Query("SELECT file_path FROM artifacts")
	if err == nil {
		var stale []string
		for rows.Next() {
			var path string
			if err := rows.Scan(&path); err != nil {
				log.Fatalf("Failed to scan artifact: %v", err)
			}
			if !activeTargets[path] {
				stale = append(stale, path)
			}
		}
		rows.Close()
		for _, path := range stale {
			if _, err := db.Exec("DELETE FROM artifacts WHERE file_path = ?", path); err != nil {
				log.Fatalf("Failed to prune artifact: %v", err)
			}
		}
	}

	if err := registry.SyncRegistry(dbPath, manifestPath); err != nil {
		log.Fatalf("Failed to sync registry: %v", err)
	}

	fmt.Println("Build complete.")
}

func runClean(dbPath, manifestPath string) {
	os.Remove(dbPath)
	os.Remove(manifestPath)
	os.RemoveAll(filepath.Dir(manifestPath))
	fmt.Println("Clean complete.")
}
EOF

go build -o /usr/local/bin/build_engine .
echo "Patches applied and build_engine rebuilt successfully."
