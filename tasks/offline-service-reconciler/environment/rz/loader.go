package rz

import (
	"io/fs"
	"os"
	"path/filepath"
	"strings"
)

type CentralInventory struct {
	Hosts []struct {
		HostID    string `json:"host_id"`
		Role      string `json:"role"`
		SigAnchor bool   `json:"sig_anchor"`
	} `json:"hosts"`
}

func LoadProbes(b6Path string) (map[string]map[string]string, error) {
	roleMap := make(map[string]map[string]string)
	files, err := os.ReadDir(b6Path)
	if err != nil {
		return nil, err
	}
	var tomlFiles []fs.DirEntry
	for _, file := range files {
		if !file.IsDir() && filepath.Ext(file.Name()) == ".toml" {
			tomlFiles = append(tomlFiles, file)
		}
	}
	for _, file := range tomlFiles {
		content, err := os.ReadFile(filepath.Join(b6Path, file.Name()))
		if err != nil {
			return nil, err
		}
		hostID := parseTOMLKey(string(content), "host_id")
		role := parseTOMLKey(string(content), "role")
		profile := parseTOMLKey(string(content), "profile")
		if hostID != "" {
			roleMap[hostID] = map[string]string{
				"role":    role,
				"profile": profile,
			}
		}
	}
	return roleMap, nil
}

func parseTOMLKey(content, key string) string {
	lines := strings.Split(content, "\n")
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, key) {
			parts := strings.SplitN(trimmed, "=", 2)
			if len(parts) == 2 {
				val := strings.TrimSpace(parts[1])
				val = strings.Trim(val, `"'`)
				return val
			}
		}
	}
	return ""
}
