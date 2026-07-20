package rz
import ("encoding/json"; "os")
func Rz_g4(b6Path string, g2Path string) (map[string]map[string]string, error) {
	return rz_g4(b6Path, g2Path)
}
func rz_g4(b6Path string, g2Path string) (map[string]map[string]string, error) {
	roleMap, err := LoadProbes(b6Path)
	if err != nil { return nil, err }
	invBytes, err := os.ReadFile(g2Path)
	if err != nil { return nil, err }
	var inv CentralInventory
	if err := json.Unmarshal(invBytes, &inv); err != nil { return nil, err }
	for _, entry := range inv.Hosts {
		if entry.HostID != "" {
			if _, ok := roleMap[entry.HostID]; ok {
				roleMap[entry.HostID]["role"] = entry.Role
			}
		}
	}
	return roleMap, nil
}
