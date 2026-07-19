package scheduler

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

func InitDB(dbPath string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, err
	}
	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS artifacts (
			file_path TEXT PRIMARY KEY,
			fingerprint TEXT
		);
		CREATE TABLE IF NOT EXISTS edges (
			from_node TEXT,
			to_node TEXT,
			PRIMARY KEY (from_node, to_node)
		);
	`)
	return db, err
}
