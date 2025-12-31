package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
	"github.com/pzsp-teams/lib/models"
)

type listChannelsParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) ListChannels(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params listChannelsParams) (interface{}, error) {
		return c.client.Channels.ListChannels(context.TODO(), params.TeamRef)
	})
}

type baseChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
}

func (c *TeamsJSONClient) GetChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params baseChannelParams) (interface{}, error) {
		return c.client.Channels.Get(context.TODO(), params.TeamRef, params.ChannelRef)
	})
}

type createChannelParams struct {
	TeamRef string `json:"teamRef"`
	Name    string `json:"name"`
}

func (c *TeamsJSONClient) CreateStandardChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params createChannelParams) (interface{}, error) {
		return c.client.Channels.CreateStandardChannel(context.TODO(), params.TeamRef, params.Name)
	})
}

type createPrivateChannelParams struct {
	TeamRef    string   `json:"teamRef"`
	Name       string   `json:"name"`
	MemberRefs []string `json:"memberRefs"`
	OwnerRefs  []string `json:"ownerRefs"`
}

func (c *TeamsJSONClient) CreatePrivateChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params createPrivateChannelParams) (interface{}, error) {
		return c.client.Channels.CreatePrivateChannel(context.TODO(), params.TeamRef, params.Name, params.MemberRefs, params.OwnerRefs)
	})
}

func (c *TeamsJSONClient) DeleteChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params baseChannelParams) (interface{}, error) {
		err := c.client.Channels.Delete(context.TODO(), params.TeamRef, params.ChannelRef)
		return "deleted", err
	})
}

type sendMessageToChannelParams struct {
	TeamRef    string                  `json:"teamRef"`
	ChannelRef string                  `json:"channelRef"`
	Body       decoders.MessageBodyDTO `json:"body"`
}

func (c *TeamsJSONClient) SendMessageToChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params sendMessageToChannelParams) (interface{}, error) {
		body, err := decoders.DecodeParams[models.MessageBody](&params.Body)
		if err != nil {
			return nil, err
		}
		return c.client.Channels.SendMessage(context.TODO(), params.TeamRef, params.ChannelRef, *body)
	})
}

type sendReplyToChannelParams struct {
	TeamRef    string                  `json:"teamRef"`
	ChannelRef string                  `json:"channelRef"`
	MessageID  string                  `json:"messageId"`
	Body       decoders.MessageBodyDTO `json:"body"`
}

func (c *TeamsJSONClient) SendReplyToChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params sendReplyToChannelParams) (interface{}, error) {
		body, err := decoders.DecodeParams[models.MessageBody](&params.Body)
		if err != nil {
			return nil, err
		}
		return c.client.Channels.SendReply(context.TODO(), params.TeamRef, params.ChannelRef, params.MessageID, *body)
	})
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

func (c *TeamsJSONClient) ListMessagesInChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params listMessagesParams) (interface{}, error) {
		options, err := decoders.DecodeParams[models.ListMessagesOptions](params.Options)
		if err != nil {
			return nil, err
		}
		return c.client.Channels.ListMessages(context.TODO(), params.TeamRef, params.ChannelRef, options)
	})
}

type getMessageParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
}

func (c *TeamsJSONClient) GetMessageInChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params getMessageParams) (interface{}, error) {
		return c.client.Channels.GetMessage(context.TODO(), params.TeamRef, params.ChannelRef, params.MessageID)
	})
}

type listRepliesParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
	Top        *int32 `json:"top"`
}

func (c *TeamsJSONClient) ListMessageRepliesInChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params listRepliesParams) (interface{}, error) {
		return c.client.Channels.ListReplies(context.TODO(), params.TeamRef, params.ChannelRef, params.MessageID, params.Top)
	})
}

type getReplyParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
	ReplyID    string `json:"replyId"`
}

func (c *TeamsJSONClient) GetMessageReplyInChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params getReplyParams) (interface{}, error) {
		return c.client.Channels.GetReply(context.TODO(), params.TeamRef, params.ChannelRef, params.MessageID, params.ReplyID)
	})
}

func (c *TeamsJSONClient) ListChannelMembers(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params baseChannelParams) (interface{}, error) {
		return c.client.Channels.ListMembers(context.TODO(), params.TeamRef, params.ChannelRef)
	})
}

type addOrUpdateMemberToChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	UserRef    string `json:"userRef"`
	IsOwner    bool   `json:"isOwner"`
}

func (c *TeamsJSONClient) AddMemberToChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params addOrUpdateMemberToChannelParams) (interface{}, error) {
		return c.client.Channels.AddMember(context.TODO(), params.TeamRef, params.ChannelRef, params.UserRef, params.IsOwner)
	})
}

func (c *TeamsJSONClient) UpdateMemberInChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params addOrUpdateMemberToChannelParams) (interface{}, error) {
		return c.client.Channels.UpdateMemberRole(context.TODO(), params.TeamRef, params.ChannelRef, params.UserRef, params.IsOwner)
	})
}

type removeMemberFromChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	UserRef    string `json:"userRef"`
}

func (c *TeamsJSONClient) RemoveMemberFromChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params removeMemberFromChannelParams) (interface{}, error) {
		err := c.client.Channels.RemoveMember(context.TODO(), params.TeamRef, params.ChannelRef, params.UserRef)
		return "removed", err
	})
}

type getMentionsInChannelParams struct {
	TeamRef     string   `json:"teamRef"`
	ChannelRef  string   `json:"channelRef"`
	RawMentions []string `json:"rawMentions"`
}

func (c *TeamsJSONClient) GetMentionsInChannel(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params getMentionsInChannelParams) (interface{}, error) {
		return c.client.Channels.GetMentions(context.TODO(), params.TeamRef, params.ChannelRef, params.RawMentions)
	})
}