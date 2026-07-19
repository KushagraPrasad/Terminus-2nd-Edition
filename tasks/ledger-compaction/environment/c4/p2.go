package c4

func LabelsFrom(items []map[string]any) []string {
	labels := []string{}
	for _, item := range items {
		if label, _ := item["label"].(string); label != "" {
			labels = append(labels, label)
		}
	}
	return labels
}
