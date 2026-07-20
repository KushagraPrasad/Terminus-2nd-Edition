package kv

import (
	"fmt"
)

func Kv_w7(g2Path string, resolvedRoles map[string]map[string]string) (string, error) {
	return kv_w7(g2Path, resolvedRoles)
}

func kv_w7(g2Path string, resolvedRoles map[string]map[string]string) (string, error) {
	var sum uint64
	for hostID, details := range resolvedRoles {
		for _, char := range hostID {
			sum += uint64(char)
		}
		for _, char := range details["role"] {
			sum += uint64(char)
		}
		for _, char := range details["profile"] {
			sum += uint64(char)
		}
	}
	digest := fmt.Sprintf("%016x", sum)
	return digest, nil
}
