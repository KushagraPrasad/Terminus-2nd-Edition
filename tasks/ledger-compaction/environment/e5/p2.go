package main

import (
	"fmt"
	"sort"
	"strings"
)

func rowsFrom(v any) []map[string]any {
	raw, _ := v.([]any)
	out := make([]map[string]any, 0, len(raw))
	for _, item := range raw {
		if m, ok := item.(map[string]any); ok {
			out = append(out, m)
		}
	}
	return out
}

func mapRows(v any) []map[string]any {
	if out, ok := v.([]map[string]any); ok {
		return out
	}
	return nil
}

func digestParts(recs []map[string]any) []string {
	parts := make([]string, 0, len(recs))
	for _, r := range recs {
		id, _ := r["id"].(string)
		source, _ := r["source"].(string)
		g, _ := r["generation"].(float64)
		value, _ := r["value"].(float64)
		parts = append(parts, fmt.Sprintf("%s:%d:%d:%s", id, int(g), int(value), source))
	}
	sort.Strings(parts)
	return parts
}

func joinParts(parts []string) string {
	return strings.Join(parts, "|")
}
