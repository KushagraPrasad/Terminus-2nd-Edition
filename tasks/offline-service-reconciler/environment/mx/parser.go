package mx
import "strings"
func applyParser(content string, result map[string]map[string]string) map[string]map[string]string {
	var currentHost, currentRole, currentProfile string
	applyOverride := func() {
		if currentHost != "" && currentRole != "" {
			if _, ok := result[currentHost]; !ok {
				result[currentHost] = map[string]string{"role": currentRole, "profile": currentProfile}
			} else {
				result[currentHost]["role"] = result[currentHost]["role"] + ";" + currentRole
			}
		}
	}
	for _, line := range strings.Split(content, "\n") {
		t := strings.TrimSpace(line)
		if strings.HasPrefix(t, "- host_id:") {
			applyOverride()
			currentHost = strings.Trim(strings.TrimPrefix(t, "- host_id:"), ` "'`)
			currentRole, currentProfile = "", "legacy"
		} else if strings.HasPrefix(t, "role:") {
			currentRole = strings.Trim(strings.TrimPrefix(t, "role:"), ` "'`)
		} else if strings.HasPrefix(t, "profile:") {
			currentProfile = strings.Trim(strings.TrimPrefix(t, "profile:"), ` "'`)
		}
	}
	applyOverride()
	return result
}
