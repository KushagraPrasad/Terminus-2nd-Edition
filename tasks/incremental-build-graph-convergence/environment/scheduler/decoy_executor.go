package scheduler

import (
	"build_engine/registry"
	"database/sql"
	"log"
	"os"
	"path/filepath"
)

type Executor struct{}

func (e *Executor) Run(action *Action) error {
	return nil
}

func BuildGraph(db *sql.DB, actions []Action, manifestPath string, dbPath string) {
	outputsDir := filepath.Dir(manifestPath)
	for _, action := range actions {
		fp, err := ComputeActionFingerprint(&action)
		if err != nil {
			log.Fatalf("Failed to compute fingerprint: %v", err)
		}

		var savedFp string
		err = db.QueryRow("SELECT fingerprint FROM artifacts WHERE file_path = ?", action.ID).Scan(&savedFp)
		if err == sql.ErrNoRows || savedFp != fp {
			outFile := filepath.Join(outputsDir, action.ID)
			err = os.WriteFile(outFile, []byte("built: " + action.Command), 0644)
			if err != nil {
				log.Fatalf("Failed to write output: %v", err)
			}
			_, err = db.Exec("INSERT OR REPLACE INTO artifacts (file_path, fingerprint) VALUES (?, ?)", action.ID, fp)
			if err != nil {
				log.Fatalf("Failed to update artifact db: %v", err)
			}
		}
	}

	if err := registry.SyncRegistry(dbPath, manifestPath); err != nil {
		log.Fatalf("Failed to sync registry: %v", err)
	}
}
