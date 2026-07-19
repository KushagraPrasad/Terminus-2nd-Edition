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
			re := regexp.MustCompile(`interface\s*\{\s*\}`)
			matches := re.FindAll(data, -1)
			for _, m := range matches {
				h.Write(m)
			}
		}

		h.Write(data)
	}

	return hex.EncodeToString(h.Sum(nil)), nil
}
