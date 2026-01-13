package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
	"github.com/pzsp-teams/lib/models"
	"github.com/pzsp-teams/lib/search"
)

type listChannelsParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) ListChannels(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params listChannelsParams) (any, error) {
		return c.client.Channels.ListChannels(ctx, params.TeamRef)
	})
}

type baseChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
}

func (c *TeamsJSONClient) GetChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params baseChannelParams) (any, error) {
		return c.client.Channels.Get(ctx, params.TeamRef, params.ChannelRef)
	})
}

type createChannelParams struct {
	TeamRef string `json:"teamRef"`
	Name    string `json:"name"`
}

func (c *TeamsJSONClient) CreateStandardChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params createChannelParams) (any, error) {
		return c.client.Channels.CreateStandardChannel(ctx, params.TeamRef, params.Name)
	})
}

type createPrivateChannelParams struct {
	TeamRef    string   `json:"teamRef"`
	Name       string   `json:"name"`
	MemberRefs []string `json:"memberRefs"`
	OwnerRefs  []string `json:"ownerRefs"`
}

func (c *TeamsJSONClient) CreatePrivateChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params createPrivateChannelParams) (any, error) {
		return c.client.Channels.CreatePrivateChannel(ctx, params.TeamRef, params.Name, params.MemberRefs, params.OwnerRefs)
	})
}

func (c *TeamsJSONClient) DeleteChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params baseChannelParams) (any, error) {
		err := c.client.Channels.Delete(ctx, params.TeamRef, params.ChannelRef)
		return "deleted", err
	})
}

type sendMessageToChannelParams struct {
	TeamRef    string                  `json:"teamRef"`
	ChannelRef string                  `json:"channelRef"`
	Body       decoders.MessageBodyDTO `json:"body"`
}

func (c *TeamsJSONClient) SendMessageToChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params sendMessageToChannelParams) (any, error) {
		body, err := decoders.DecodeParams[models.MessageBody](&params.Body)
		if err != nil {
			return nil, err
		}
		return c.client.Channels.SendMessage(ctx, params.TeamRef, params.ChannelRef, *body)
	})
}

type sendReplyToChannelParams struct {
	TeamRef    string                  `json:"teamRef"`
	ChannelRef string                  `json:"channelRef"`
	MessageID  string                  `json:"messageId"`
	Body       decoders.MessageBodyDTO `json:"body"`
}

func (c *TeamsJSONClient) SendReplyToChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params sendReplyToChannelParams) (any, error) {
		body, err := decoders.DecodeParams[models.MessageBody](&params.Body)
		if err != nil {
			return nil, err
		}
		return c.client.Channels.SendReply(ctx, params.TeamRef, params.ChannelRef, params.MessageID, *body)
	})
}

type listMessagesOptionsDTO struct {
	Top           *int32 `json:"top"`
	ExpandReplies bool   `json:"expandReplies"`
}

type listMessagesParams struct {
	TeamRef       string                 `json:"teamRef"`
	ChannelRef    string                 `json:"channelRef"`
	Options       listMessagesOptionsDTO `json:"options"`
	IncludeSystem bool                   `json:"includeSystem"`
	NextLink      decoders.NextLinkDTO   `json:"nextLink"`
}

func (c *TeamsJSONClient) ListMessagesInChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params listMessagesParams) (any, error) {
		options, err := decoders.DecodeParams[models.ListMessagesOptions](params.Options)
		if err != nil {
			return nil, err
		}
		nextLink := decoders.GetNextLink(&params.NextLink)
		return c.client.Channels.ListMessages(ctx, params.TeamRef, params.ChannelRef, options, params.IncludeSystem, nextLink)
	})
}

type getMessageParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
}

func (c *TeamsJSONClient) GetMessageInChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params getMessageParams) (any, error) {
		return c.client.Channels.GetMessage(ctx, params.TeamRef, params.ChannelRef, params.MessageID)
	})
}

type listRepliesParams struct {
	TeamRef       string               `json:"teamRef"`
	ChannelRef    string               `json:"channelRef"`
	MessageID     string               `json:"messageId"`
	Top           *int32               `json:"top"`
	IncludeSystem bool                 `json:"includeSystem"`
	NextLink      decoders.NextLinkDTO `json:"nextLink"`
}

func (c *TeamsJSONClient) ListMessageRepliesInChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params listRepliesParams) (any, error) {
		nextLink := decoders.GetNextLink(&params.NextLink)
		return c.client.Channels.ListReplies(ctx, params.TeamRef, params.ChannelRef, params.MessageID, params.Top, params.IncludeSystem, nextLink)
	})
}

type getReplyParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	MessageID  string `json:"messageId"`
	ReplyID    string `json:"replyId"`
}

func (c *TeamsJSONClient) GetMessageReplyInChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params getReplyParams) (any, error) {
		return c.client.Channels.GetReply(ctx, params.TeamRef, params.ChannelRef, params.MessageID, params.ReplyID)
	})
}

func (c *TeamsJSONClient) ListChannelMembers(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params baseChannelParams) (any, error) {
		return c.client.Channels.ListMembers(ctx, params.TeamRef, params.ChannelRef)
	})
}

type addOrUpdateMemberToChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	UserRef    string `json:"userRef"`
	IsOwner    bool   `json:"isOwner"`
}

func (c *TeamsJSONClient) AddMemberToChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params addOrUpdateMemberToChannelParams) (any, error) {
		return c.client.Channels.AddMember(ctx, params.TeamRef, params.ChannelRef, params.UserRef, params.IsOwner)
	})
}

func (c *TeamsJSONClient) UpdateMemberInChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params addOrUpdateMemberToChannelParams) (any, error) {
		return c.client.Channels.UpdateMemberRoles(ctx, params.TeamRef, params.ChannelRef, params.UserRef, params.IsOwner)
	})
}

type removeMemberFromChannelParams struct {
	TeamRef    string `json:"teamRef"`
	ChannelRef string `json:"channelRef"`
	UserRef    string `json:"userRef"`
}

func (c *TeamsJSONClient) RemoveMemberFromChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params removeMemberFromChannelParams) (any, error) {
		err := c.client.Channels.RemoveMember(ctx, params.TeamRef, params.ChannelRef, params.UserRef)
		return "removed", err
	})
}

type getMentionsInChannelParams struct {
	TeamRef     string   `json:"teamRef"`
	ChannelRef  string   `json:"channelRef"`
	RawMentions []string `json:"rawMentions"`
}

func (c *TeamsJSONClient) GetMentionsInChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params getMentionsInChannelParams) (any, error) {
		return c.client.Channels.GetMentions(ctx, params.TeamRef, params.ChannelRef, params.RawMentions)
	})
}

type searchMessagesInChannelParams struct {
	TeamRef       string                           `json:"teamRef"`
	ChannelRef    string                           `json:"channelRef"`
	SearchOptions decoders.SearchMessageOptionsDTO `json:"searchMessagesOptions"`
	SearchConfig  decoders.SearchConfigDTO         `json:"searchConfig"`
}

func (c *TeamsJSONClient) SearchMessagesInChannel(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params searchMessagesInChannelParams) (any, error) {
		searchOptions := decoders.DecodeSearchMessageOptions(&params.SearchOptions)
		searchConfig, err := decoders.DecodeParams[search.SearchConfig](&params.SearchConfig)
		if err != nil {
			return nil, err
		}
		return c.client.Channels.SearchMessages(ctx, &params.TeamRef, &params.ChannelRef, searchOptions, searchConfig)
	})
}
