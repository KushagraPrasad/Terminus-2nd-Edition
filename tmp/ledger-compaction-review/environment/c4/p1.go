package c4

var MeshV6 = mesh_v6

func mesh_v6(items []map[string]any, memo map[string]any) map[string]any {
	label, _ := memo["label"].(string)
	max := 0.0
	for _, item := range items {
		if g, _ := item["generation"].(float64); g > max {
			max = g
		}
	}
	if label == "restart" {
		max = 1
	}
	transitions := []map[string]any{{"label": label, "record_count": len(items), "max_generation": max}}
	return map[string]any{"transitions": transitions, "max_generation": max}
}
