package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
	"github.com/pzsp-teams/lib/chats"
	"github.com/pzsp-teams/lib/models"
	"github.com/pzsp-teams/lib/search"
)

type createOneToOneChatParams struct {
	RecipientRef string `json:"recipientRef"`
}

func (c *TeamsJSONClient) CreateOneToOneChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params createOneToOneChatParams) (any, error) {
		return c.client.Chats.CreateOneOnOne(ctx, params.RecipientRef)
	})
}

type createGroupChatParams struct {
	RecipientRefs []string `json:"recipientRefs"`
	Topic         string   `json:"topic"`
	IncludeMe     bool     `json:"includeMe"`
}

func (c *TeamsJSONClient) CreateGroupChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params createGroupChatParams) (any, error) {
		return c.client.Chats.CreateGroup(ctx, params.RecipientRefs, params.Topic, params.IncludeMe)
	})
}

type baseChatParams struct {
	ChatRef decoders.ChatRefDTO `json:"chatRef"`
}

func (c *TeamsJSONClient) GetChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params baseChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		return c.client.Chats.GetChat(ctx, chatRef)
	})
}

type groupChatMemberParams struct {
	GroupChatRef string `json:"groupChatRef"`
	UserRef      string `json:"userRef"`
}

func (c *TeamsJSONClient) AddMemberToGroupChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params groupChatMemberParams) (any, error) {
		return c.client.Chats.AddMemberToGroupChat(ctx, chats.GroupChatRef{Ref: params.GroupChatRef}, params.UserRef)
	})
}

func (c *TeamsJSONClient) RemoveMemberFromGroupChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params groupChatMemberParams) (any, error) {
		err := c.client.Chats.RemoveMemberFromGroupChat(ctx, chats.GroupChatRef{Ref: params.GroupChatRef}, params.UserRef)
		return "removed", err
	})
}

type listMembersInChatParams struct {
	GroupChatRef string `json:"groupChatRef"`
}

func (c *TeamsJSONClient) ListGroupChatMembers(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params listMembersInChatParams) (any, error) {
		return c.client.Chats.ListGroupChatMembers(ctx, chats.GroupChatRef{Ref: params.GroupChatRef})
	})
}

type updateGroupChatTopicParams struct {
	GroupChatRef string `json:"groupChatRef"`
	Topic        string `json:"topic"`
}

func (c *TeamsJSONClient) UpdateGroupChatTopic(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params updateGroupChatTopicParams) (any, error) {
		return c.client.Chats.UpdateGroupChatTopic(ctx, chats.GroupChatRef{Ref: params.GroupChatRef}, params.Topic)
	})
}

type listMessagesInChatParams struct {
	ChatRef       decoders.ChatRefDTO  `json:"chatRef"`
	IncludeSystem bool                 `json:"includeSystem"`
	NextLink      decoders.NextLinkDTO `json:"nextLink"`
}

func (c *TeamsJSONClient) ListMessagesInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params listMessagesInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		nextLink := decoders.GetNextLink(&params.NextLink)
		return c.client.Chats.ListMessages(ctx, chatRef, params.IncludeSystem, nextLink)
	})
}

type sendMessageInChatParams struct {
	ChatRef decoders.ChatRefDTO     `json:"chatRef"`
	Body    decoders.MessageBodyDTO `json:"body"`
}

func (c *TeamsJSONClient) SendMessageInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params sendMessageInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		body, err := decoders.DecodeParams[models.MessageBody](params.Body)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.SendMessage(ctx, chatRef, *body)
	})
}

type messageInChatParams struct {
	ChatRef   decoders.ChatRefDTO `json:"chatRef"`
	MessageID string              `json:"messageId"`
}

func (c *TeamsJSONClient) DeleteMessageInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params messageInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		err := c.client.Chats.DeleteMessage(ctx, chatRef, params.MessageID)
		return "deleted", err
	})
}

func (c *TeamsJSONClient) GetMessageInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params messageInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		return c.client.Chats.GetMessage(ctx, chatRef, params.MessageID)
	})
}

type ListMyChatsParams struct {
	ChatType string `json:"chatType"`
}

func (c *TeamsJSONClient) ListMyChats(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params ListMyChatsParams) (any, error) {
		var chatType models.ChatType
		if params.ChatType != "" {
			chatType = models.ChatType(params.ChatType)
		}
		return c.client.Chats.ListChats(ctx, &chatType)
	})
}

type listChatMessagesParams struct {
	StartTime string `json:"startTime"`
	EndTime   string `json:"endTime"`
	Top       *int32 `json:"top"`
}

func (c *TeamsJSONClient) ListMyChatMessages(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params listChatMessagesParams) (any, error) {
		parsedStartTime, parsedEndTime, err := decoders.DecodeTimeRange(params.StartTime, params.EndTime)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.ListAllMessages(ctx, parsedStartTime, parsedEndTime, params.Top)
	})
}

func (c *TeamsJSONClient) ListPinnedMessagesInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params baseChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		return c.client.Chats.ListPinnedMessages(ctx, chatRef)
	})
}

func (c *TeamsJSONClient) PinMessageInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params messageInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		err := c.client.Chats.PinMessage(ctx, chatRef, params.MessageID)
		return "pinned", err
	})
}

func (c *TeamsJSONClient) UnpinMessageInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params messageInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		err := c.client.Chats.UnpinMessage(ctx, chatRef, params.MessageID)
		return "unpinned", err
	})
}

type mentionInChatParams struct {
	ChatRef     decoders.ChatRefDTO `json:"chatRef"`
	RawMentions []string            `json:"rawMentions"`
}

func (c *TeamsJSONClient) GetMentionsInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params mentionInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		return c.client.Chats.GetMentions(ctx, chatRef, params.RawMentions)
	})
}

type searchMessagesInChatParams struct {
	ChatRef       decoders.ChatRefDTO              `json:"chatRef"`
	SearchOptions decoders.SearchMessageOptionsDTO `json:"searchMessagesOptions"`
	SearchConfig  decoders.SearchConfigDTO         `json:"searchConfig"`
}

func (c *TeamsJSONClient) SearchMessagesInChat(ctx context.Context, p map[string]any) (any, error) {
	return execute(p, func(params searchMessagesInChatParams) (any, error) {
		chatRef := decoders.GetChatRef(params.ChatRef)
		searchOptions := decoders.DecodeSearchMessageOptions(&params.SearchOptions)
		searchConfig, err := decoders.DecodeParams[search.SearchConfig](&params.SearchConfig)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.SearchMessages(ctx, chatRef, searchOptions, searchConfig)
	})
}
