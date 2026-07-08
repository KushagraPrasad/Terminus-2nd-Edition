package a3

var PivM31 = piv_m31

func piv_m31(rows []map[string]any, marks []map[string]any, cap int) map[string]any {
	limit := float64(cap)
	for _, m := range marks {
		if m["label"] == "restart" {
			limit = 1
		}
	}
	kept := make([]map[string]any, 0, len(rows))
	for _, r := range rows {
		g, _ := r["generation"].(float64)
		active, ok := r["active"].(bool)
		if !ok {
			active = true
		}
		if active && g <= limit {
			kept = append(kept, r)
		}
	}
	return map[string]any{"rows": kept, "limit": limit, "marks": marks}
}
