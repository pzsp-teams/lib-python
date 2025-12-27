package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
	"github.com/pzsp-teams/lib/models"
)

type listChannelsParams struct {
	TeamRef string `json:"teamRef"`
}

func (jsonclient *TeamsJSONClient) ListChannels(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[listChannelsParams](p)
	if err != nil {
		return nil, err
	}
	channels, err := jsonclient.client.Channels.ListChannels(context.TODO(), params.TeamRef)
	if err != nil {
		return nil, err
	}
	return channels, nil
}

type baseChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
}

func (jsonclient *TeamsJSONClient) GetChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[baseChannelParams](p)
	if err != nil {
		return nil, err
	}
	channel, err := jsonclient.client.Channels.Get(context.TODO(), params.TeamRef, params.ChannelRef)
	if err != nil {
		return nil, err
	}
	return channel, nil
}

type createChannelParams struct {
	TeamRef string `json:"teamRef"`
	Name    string `json:"name"`
}

func (jsonclient *TeamsJSONClient) CreateStandardChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createChannelParams](p)
	if err != nil {
		return nil, err
	}
	channel, err := jsonclient.client.Channels.CreateStandardChannel(context.TODO(), params.TeamRef, params.Name)
	if err != nil {
		return nil, err
	}
	return channel, nil
}

type createPrivateChannelParams struct {
	TeamRef    string   `json:"teamRef"`
	Name       string   `json:"name"`
	MemberRefs []string `json:"memberRefs"`
	OwnerRefs  []string `json:"ownerRefs"`
}

func (jsonclient *TeamsJSONClient) CreatePrivateChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createPrivateChannelParams](p)
	if err != nil {
		return nil, err
	}
	channel, err := jsonclient.client.Channels.CreatePrivateChannel(context.TODO(), params.TeamRef, params.Name, params.MemberRefs, params.OwnerRefs)
	if err != nil {
		return nil, err
	}
	return channel, nil
}

func (jsonclient *TeamsJSONClient) DeleteChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[baseChannelParams](p)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Channels.Delete(context.TODO(), params.TeamRef, params.ChannelRef)
	if err != nil {
		return nil, err
	}
	return "deleted", nil
}

type messageBodyDTO struct {
	ContentType string `json:"contentType"`
	Content     string `json:"content"`
}

type sendMessageToChannelParams struct {
	TeamRef    string         `json:"teamRef"`
	ChannelRef string         `json:"channelRef"`
	Body       messageBodyDTO `json:"body"`
}

func (jsonclient *TeamsJSONClient) SendMessageToChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[sendMessageToChannelParams](p)
	if err != nil {
		return nil, err
	}
	body, err := decoders.DecodeParams[models.MessageBody](&params.Body)
	if err != nil {
		return nil, err
	}
	sentMessage, err := jsonclient.client.Channels.SendMessage(context.TODO(), params.TeamRef, params.ChannelRef, *body)
	if err != nil {
		return nil, err
	}
	return sentMessage, nil
}


