package b7

func SurfaceNames(items []map[string]any) []string {
	seen := map[string]bool{}
	out := []string{}
	for _, item := range items {
		name, _ := item["source"].(string)
		if name != "" && !seen[name] {
			seen[name] = true
			out = append(out, name)
		}
	}
	return out
}
