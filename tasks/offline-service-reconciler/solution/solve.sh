#!/bin/bash
# Terminal-Bench Canary

# Solution logic to repair all three modules:
# 1. Update rz_g4.go to parse central inventory JSON and apply sig_anchor override.
# 2. Update kv_w7.go to read central inventory file bytes, compute SHA256 of those bytes, and concatenate to resolvedRoles JSON for the final SHA256 hash.
# 3. Update parser.go to merge operator overrides idempotently (without appending overrides history trace on duplicate runs).

cat > /app/environment/rz/rz_g4.go << 'EOF'
package rz
import ("encoding/json"; "os")
func Rz_g4(b6Path string, g2Path string) (map[string]map[string]string, error) {
	return rz_g4(b6Path, g2Path)
}
func rz_g4(b6Path string, g2Path string) (map[string]map[string]string, error) {
	roleMap, err := LoadProbes(b6Path)
	if err != nil { return nil, err }
	invBytes, err := os.ReadFile(g2Path)
	if err != nil { return nil, err }
	var inv CentralInventory
	if err := json.Unmarshal(invBytes, &inv); err != nil { return nil, err }
	for _, entry := range inv.Hosts {
		if entry.SigAnchor {
			if _, ok := roleMap[entry.HostID]; ok {
				roleMap[entry.HostID]["role"] = entry.Role
			}
		}
	}
	return roleMap, nil
}
EOF

cat > /app/environment/kv/kv_w7.go << 'EOF'
package kv

import (
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"os"
	"sort"
)

func Kv_w7(g2Path string, resolvedRoles map[string]map[string]string) (string, error) {
	return kv_w7(g2Path, resolvedRoles)
}

func kv_w7(g2Path string, resolvedRoles map[string]map[string]string) (string, error) {
	invContent, err := os.ReadFile(g2Path)
	if err != nil {
		return "", err
	}

	keys := make([]string, 0, len(resolvedRoles))
	for k := range resolvedRoles {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	ordered := make([]map[string]string, 0, len(keys))
	for _, k := range keys {
		ordered = append(ordered, map[string]string{
			"host_id": k,
			"role":    resolvedRoles[k]["role"],
			"profile": resolvedRoles[k]["profile"],
		})
	}

	serialized, err := json.Marshal(ordered)
	if err != nil {
		return "", err
	}

	hInv := sha256.New()
	hInv.Write(invContent)
	invHash := fmt.Sprintf("%x", hInv.Sum(nil))

	h := sha256.New()
	h.Write([]byte(string(serialized) + "|" + invHash))
	digest := fmt.Sprintf("%x", h.Sum(nil))

	return digest, nil
}
EOF

cat > /app/environment/mx/parser.go << 'EOF'
package mx
import "strings"
func applyParser(content string, result map[string]map[string]string) map[string]map[string]string {
	var currentHost, currentRole, currentProfile string
	applyOverride := func() {
		if currentHost != "" && currentRole != "" {
			if _, ok := result[currentHost]; !ok {
				result[currentHost] = map[string]string{"role": currentRole, "profile": currentProfile}
			} else {
				result[currentHost]["role"] = currentRole
			}
		}
	}
	for _, line := range strings.Split(content, "\n") {
		t := strings.TrimSpace(line)
		if strings.HasPrefix(t, "- host_id:") {
			applyOverride()
			currentHost = strings.Trim(strings.TrimPrefix(t, "- host_id:"), ` "'`)
			currentRole, currentProfile = "", "legacy"
		} else if strings.HasPrefix(t, "role:") {
			currentRole = strings.Trim(strings.TrimPrefix(t, "role:"), ` "'`)
		} else if strings.HasPrefix(t, "profile:") {
			currentProfile = strings.Trim(strings.TrimPrefix(t, "profile:"), ` "'`)
		}
	}
	applyOverride()
	return result
}
EOF
