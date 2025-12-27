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

type listMessagesOptionsDTO struct {
	Top           *int32 `json:"top"`
	ExpandReplies bool   `json:"expandReplies"`
}

type listMessagesParams struct {
	TeamRef    string                 `json:"teamRef"`
	ChannelRef string                 `json:"channelRef"`
	Options    listMessagesOptionsDTO `json:"options"`
}

func (jsonclient *TeamsJSONClient) ListMessagesInChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[listMessagesParams](p)
	if err != nil {
		return nil, err
	}
	options, err := decoders.DecodeParams[models.ListMessagesOptions](params.Options)
	if err != nil {
		return nil, err
	}
	messages, err := jsonclient.client.Channels.ListMessages(context.TODO(), params.TeamRef, params.ChannelRef, options)
	if err != nil {
		return nil, err
	}
	return messages, nil
}

type getMessageParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
}

func (jsonclient *TeamsJSONClient) GetMessageInChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[getMessageParams](p)
	if err != nil {
		return nil, err
	}
	message, err := jsonclient.client.Channels.GetMessage(context.TODO(), params.TeamRef, params.ChannelRef, params.MessageID)
	if err != nil {
		return nil, err
	}
	return message, nil
}

type listRepliesParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
	Top        *int32 `json:"top"`
}

func (jsonclient *TeamsJSONClient) ListMessageRepliesInChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[listRepliesParams](p)
	if err != nil {
		return nil, err
	}
	messages, err := jsonclient.client.Channels.ListReplies(context.TODO(), params.TeamRef, params.ChannelRef, params.MessageID, params.Top)
	if err != nil {
		return nil, err
	}
	return messages, nil
}

type getReplyParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
	ReplyID    string `json:"replyId"`
}

func (jsonclient *TeamsJSONClient) GetMessageReplyInChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[getReplyParams](p)
	if err != nil {
		return nil, err
	}
	message, err := jsonclient.client.Channels.GetReply(context.TODO(), params.TeamRef, params.ChannelRef, params.MessageID, params.ReplyID)
	if err != nil {
		return nil, err
	}
	return message, nil
}

func (jsonclient *TeamsJSONClient) ListChannelMembers(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[baseChannelParams](p)
	if err != nil {
		return nil, err
	}
	members, err := jsonclient.client.Channels.ListMembers(context.TODO(), params.TeamRef, params.ChannelRef)
	if err != nil {
		return nil, err
	}
	return members, nil
}

type addOrUpdateMemberToChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	UserRef    string `json:"userRef"`
	IsOwner    bool   `json:"isOwner"`
}

func (jsonclient *TeamsJSONClient) AddMemberToChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[addOrUpdateMemberToChannelParams](p)
	if err != nil {
		return nil, err
	}
	member, err := jsonclient.client.Channels.AddMember(context.TODO(), params.TeamRef, params.ChannelRef, params.UserRef, params.IsOwner)
	if err != nil {
		return nil, err
	}
	return member, nil
}

func (jsonclient *TeamsJSONClient) UpdateMemberInChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[addOrUpdateMemberToChannelParams](p)
	if err != nil {
		return nil, err
	}
	member, err := jsonclient.client.Channels.UpdateMemberRole(context.TODO(), params.TeamRef, params.ChannelRef, params.UserRef, params.IsOwner)
	if err != nil {
		return nil, err
	}
	return member, nil
}

type removeMemberFromChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	UserRef    string `json:"userRef"`
}

func (jsonclient *TeamsJSONClient) RemoveMemberFromChannel(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[removeMemberFromChannelParams](p)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Channels.RemoveMember(context.TODO(), params.TeamRef, params.ChannelRef, params.UserRef)
	if err != nil {
		return nil, err
	}
	return "removed", nil
}

