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
	files, err := os.ReadDir(outputsDir)
	if err != nil && !os.IsNotExist(err) {
		return err
	}

	manifestData := map[string]string{}
	for _, file := range files {
		if file.IsDir() {
			continue
		}
		name := file.Name()
		if name == filepath.Base(manifestPath) {
			continue
		}
		manifestData[name] = "present"
	}

	data, err := json.MarshalIndent(manifestData, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(manifestPath, data, 0644)
}
