package dag

type Edge struct {
	From string `json:"from"`
	To   string `json:"to"`
}

type DependencyGraph struct {
	Edges []Edge `json:"edges"`
}

func (g *DependencyGraph) ReconcileEdges(newEdges []Edge) error {
	for i := 0; i < len(g.Edges); i++ {
		found := false
		for _, ne := range newEdges {
			if g.Edges[i].From == ne.From && g.Edges[i].To == ne.To {
				found = true
				break
			}
		}
		if !found {
			g.Edges = append(g.Edges[:i], g.Edges[i+1:]...)
		}
	}
	return nil
}
