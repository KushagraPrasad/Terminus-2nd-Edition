package mx

import (
	"os"
)

func Mx_r9(f8Path string, resolvedRoles map[string]map[string]string) (map[string]map[string]string, error) {
	return mx_r9(f8Path, resolvedRoles)
}

func mx_r9(f8Path string, resolvedRoles map[string]map[string]string) (map[string]map[string]string, error) {
	result := make(map[string]map[string]string)
	for k, v := range resolvedRoles {
		vCopy := make(map[string]string)
		for subK, subV := range v {
			vCopy[subK] = subV
		}
		result[k] = vCopy
	}
	content, err := os.ReadFile(f8Path)
	if err != nil {
		return nil, err
	}
	return applyParser(string(content), result), nil
}
