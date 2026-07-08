package d9

import (
	"fmt"
	"sort"
	"strings"
)

var SlotH4 = slot_h4

func slot_h4(bundle map[string]any, target string) map[string]any {
	recs, _ := bundle["records"].([]map[string]any)
	ids := make([]string, 0, len(recs))
	for _, r := range recs {
		id, _ := r["id"].(string)
		ids = append(ids, id)
	}
	sort.Strings(ids)
	return map[string]any{"target": target, "state_digest": strings.Join(ids, "|"), "record_count": len(recs), "note": fmt.Sprintf("%d", len(ids))}
}
