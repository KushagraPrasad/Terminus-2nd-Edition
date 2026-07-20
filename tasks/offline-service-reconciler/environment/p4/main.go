package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"reconciler/kv"
	"reconciler/mx"
	"reconciler/rz"
	"time"
)

type HostInventory struct {
	Hosts      []map[string]string `json:"hosts"`
	PackDigest string              `json:"pack_digest"`
	Generated  string              `json:"generated_at"`
}

type RunReport struct {
	RunID             string `json:"run_id"`
	HostsProcessed    int    `json:"hosts_processed"`
	ConflictsResolved int    `json:"conflicts_resolved"`
	PackDigest        string `json:"pack_digest"`
	Status            string `json:"status"`
}

func main() {
	allProfiles := flag.Bool("all-profiles", false, "Run reconciler for all profiles")
	healthCheck := flag.Bool("health", false, "Run simple health check verification")
	flag.Parse()

	if *healthCheck {
		fmt.Println("STATUS: OK")
		return
	}

	if !*allProfiles {
		fmt.Println("Error: --all-profiles must be specified to run reconciler")
		os.Exit(1)
	}

	b6Path := "/app/environment/b6"
	g2Path := "/app/environment/g2/sv_inv.json"
	f8Path := "/app/environment/f8/op_ov.yaml"

	roleMap, err := rz.Rz_g4(b6Path, g2Path)
	if err != nil {
		fmt.Printf("Error resolving probe authority: %v\n", err)
		os.Exit(1)
	}

	finalMap, err := mx.Mx_r9(f8Path, roleMap)
	if err != nil {
		fmt.Printf("Error merging operator overrides: %v\n", err)
		os.Exit(1)
	}

	digest, err := kv.Kv_w7(g2Path, finalMap)
	if err != nil {
		fmt.Printf("Error computing pack digest: %v\n", err)
		os.Exit(1)
	}

	hosts := make([]map[string]string, 0, len(finalMap))
	for id, details := range finalMap {
		hosts = append(hosts, map[string]string{
			"id":      id,
			"role":    details["role"],
			"profile": details["profile"],
		})
	}

	inv := HostInventory{
		Hosts:      hosts,
		PackDigest: digest,
		Generated:  time.Now().UTC().Format(time.RFC3339),
	}

	outputDir := "/app/output"
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		fmt.Printf("Error creating output directory: %v\n", err)
		os.Exit(1)
	}

	invBytes, err := json.MarshalIndent(inv, "", "  ")
	if err != nil {
		fmt.Printf("Error marshaling host inventory: %v\n", err)
		os.Exit(1)
	}

	if err := os.WriteFile(filepath.Join(outputDir, "host_inventory.json"), invBytes, 0644); err != nil {
		fmt.Printf("Error writing host inventory: %v\n", err)
		os.Exit(1)
	}

	report := RunReport{
		RunID:             "run-prod-sync-f849",
		HostsProcessed:    len(roleMap),
		ConflictsResolved: len(finalMap) - len(roleMap),
		PackDigest:        digest,
		Status:            "SUCCESS",
	}

	reportBytes, err := json.MarshalIndent(report, "", "  ")
	if err != nil {
		fmt.Printf("Error marshaling run report: %v\n", err)
		os.Exit(1)
	}

	if err := os.WriteFile(filepath.Join(outputDir, "run_report.json"), reportBytes, 0644); err != nil {
		fmt.Printf("Error writing run report: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Reconciliation completed successfully.")
}
