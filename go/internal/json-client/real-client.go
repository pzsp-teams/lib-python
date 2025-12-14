//go:build real

package jsonclient

import (
	"context"

	lib "github.com/pzsp-teams/lib"
	jsonModel "github.com/pzsp-teams/lib-python/internal/json-model"
)

func NewJSONClient(req jsonModel.Request) (*TeamsJSONClient, error) {
	authConfig, err := req.Config.AuthConfigMap.ToAuthConfig()
	if err != nil {
		return nil, err
	}

	senderConfig, err := req.Config.SenderConfigMap.ToSenderConfig()
	if err != nil {
		return nil, err
	}

	cacheEnabled, err := jsonModel.ParseCacheEnabled(req.Params["cacheEnabled"])
	if err != nil {
		return nil, err
	}

	var cachePath *string
	if cacheEnabled {
		path, err := jsonModel.ParseCachePath(req.Params["cachePath"])
		if err != nil {
			return nil, err
		}
		cachePath = path
	}


	client, err := lib.NewClient(context.TODO(), authConfig, senderConfig, cacheEnabled, cachePath)
	if err != nil {
		return nil, err
	}

	return &TeamsJSONClient{client}, nil
}
