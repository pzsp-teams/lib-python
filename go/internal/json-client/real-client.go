//go:build real

package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib"
	"github.com/pzsp-teams/lib/config"
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

	cacheMode, err := jsonModel.ParseCacheMode(req.Config.CacheMode)
	if err != nil {
		return nil, err
	}
	cachePath, err := jsonModel.ParseCachePath(req.Config.CachePath)
	if err != nil {
		if cacheMode == config.CacheDisabled {
			cachePath = nil
		} else {
			return nil, err
		}
	}
	cacheConfig := config.CacheConfig{
		Mode: config.CacheDisabled,
		Provider: config.CacheProviderJSONFile,
		Path: cachePath,
	}


	client, err := lib.NewClient(context.TODO(), authConfig, senderConfig, &cacheConfig)
	if err != nil {
		return nil, err
	}

	return &TeamsJSONClient{client}, nil
}
