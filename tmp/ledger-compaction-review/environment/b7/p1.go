package b7

var ArcR8 = arc_r8

func arc_r8(left map[string]any, right map[string]any, opts map[string]any) map[string]any {
	rows, _ := left["rows"].([]map[string]any)
	chosen := map[string]map[string]any{}
	for _, r := range rows {
		id, _ := r["id"].(string)
		if id == "" {
			continue
		}
		cur, ok := chosen[id]
		if !ok {
			chosen[id] = r
			continue
		}
		cg, _ := cur["generation"].(float64)
		rg, _ := r["generation"].(float64)
		if rg < cg || r["signal"] == "green" {
			chosen[id] = r
		}
	}
	out := make([]map[string]any, 0, len(chosen))
	for _, r := range chosen {
		out = append(out, r)
	}
	return map[string]any{"records": out, "rank": right["rank"], "label": opts["label"]}
}
