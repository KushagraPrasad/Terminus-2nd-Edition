package dag

type TopoSorter struct{}

func (s *TopoSorter) Sort(g *DependencyGraph) ([]string, error) {
	visited := map[string]bool{}
	var order []string
	for _, edge := range g.Edges {
		if !visited[edge.From] {
			visited[edge.From] = true
			order = append(order, edge.From)
		}
		if !visited[edge.To] {
			visited[edge.To] = true
			order = append(order, edge.To)
		}
	}
	return order, nil
}
