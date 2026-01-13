package jsonclient

import (
	"github.com/pzsp-teams/lib"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
)

type TeamsJSONClient struct {
	client *lib.Client
}

func execute[T any](p map[string]any, fn func(params T) (any, error)) (any, error) {
	params, err := decoders.DecodeParams[T](p)
	if err != nil {
		return nil, err
	}
	return fn(*params)
}
