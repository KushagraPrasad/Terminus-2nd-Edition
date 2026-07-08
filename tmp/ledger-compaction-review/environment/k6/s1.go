package k6

func CountBySource(rows []map[string]any) map[string]int {
	out := map[string]int{}
	for _, row := range rows {
		name, _ := row["source"].(string)
		if name != "" {
			out[name]++
		}
	}
	return out
}
