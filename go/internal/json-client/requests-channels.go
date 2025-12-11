package jsonclient

import (
	"context"
	"fmt"
)

type ListChannelsParams struct {
	TeamRef string `json:"teamRef"`
}

func (jsonclient *TeamsJSONClient) ListChannels(params map[string]interface{}) (interface{}, error) {
	teamRef, ok := params["teamRef"].(string)
	if !ok || teamRef == "" {
		return nil, fmt.Errorf("invalid teamRef parameter")
	}
	channels, err := jsonclient.client.Channels.ListChannels(context.TODO(), teamRef)
	if err != nil {
		return nil, err
	} else {
		return channels, nil
	}
}
