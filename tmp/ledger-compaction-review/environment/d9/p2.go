package d9

func ArtifactRow(path string, count int) map[string]any {
	return map[string]any{"path": path, "row_count": count}
}
