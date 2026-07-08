package k6

func MissingKeys(rows []map[string]any, keys []string) []string {
	missing := []string{}
	for _, row := range rows {
		for _, key := range keys {
			if _, ok := row[key]; !ok {
				missing = append(missing, key)
			}
		}
	}
	return missing
}
