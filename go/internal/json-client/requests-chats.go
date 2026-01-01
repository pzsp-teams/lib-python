package jsonclient

import (
	"context"
	"time"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
	"github.com/pzsp-teams/lib/chats"
	"github.com/pzsp-teams/lib/models"
)

type createOneToOneChatParams struct {
	RecipientRef string `json:"recipientRef"`
}

func (c *TeamsJSONClient) CreateOneToOneChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params createOneToOneChatParams) (interface{}, error) {
		return c.client.Chats.CreateOneOneOne(context.TODO(), params.RecipientRef)
	})
}

type createGroupChatParams struct {
	RecipientRefs []string `json:"recipientRefs"`
	Topic         string   `json:"topic"`
	IncludeMe     bool     `json:"includeMe"`
}

func (c *TeamsJSONClient) CreateGroupChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params createGroupChatParams) (interface{}, error) {
		return c.client.Chats.CreateGroup(context.TODO(), params.RecipientRefs, params.Topic, params.IncludeMe)
	})
}

type groupChatMemberParams struct {
	GroupChatRef string `json:"groupChatRef"`
	UserRef      string `json:"userRef"`
}

func (c *TeamsJSONClient) AddMemberToGroupChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params groupChatMemberParams) (interface{}, error) {
		return c.client.Chats.AddMemberToGroupChat(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef}, params.UserRef)
	})
}

func (c *TeamsJSONClient) RemoveMemberFromGroupChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params groupChatMemberParams) (interface{}, error) {
		err := c.client.Chats.RemoveMemberFromGroupChat(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef}, params.UserRef)
		return "removed", err
	})
}

type listMembersInChatParams struct {
	GroupChatRef string `json:"groupChatRef"`
}

func (c *TeamsJSONClient) ListGroupChatMembers(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params listMembersInChatParams) (interface{}, error) {
		return c.client.Chats.ListGroupChatMembers(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef})
	})
}

type updateGroupChatTopicParams struct {
	GroupChatRef string `json:"groupChatRef"`
	Topic        string `json:"topic"`
}

func (c *TeamsJSONClient) UpdateGroupChatTopic(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params updateGroupChatTopicParams) (interface{}, error) {
		return c.client.Chats.UpdateGroupChatTopic(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef}, params.Topic)
	})
}

type baseChatParams struct {
	ChatRef decoders.ChatRefDTO `json:"chatRef"`
}

func (c *TeamsJSONClient) ListMessagesInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params baseChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.ListMessages(context.TODO(), chatRef)
	})
}

type sendMessageInChatParams struct {
	ChatRef decoders.ChatRefDTO     `json:"chatRef"`
	Body    decoders.MessageBodyDTO `json:"body"`
}

func (c *TeamsJSONClient) SendMessageInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params sendMessageInChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		body, err := decoders.DecodeParams[models.MessageBody](params.Body)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.SendMessage(context.TODO(), chatRef, *body)
	})
}

type messageInChatParams struct {
	ChatRef   decoders.ChatRefDTO `json:"chatRef"`
	MessageID string              `json:"messageId"`
}

func (c *TeamsJSONClient) DeleteMessageInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params messageInChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		err = c.client.Chats.DeleteMessage(context.TODO(), chatRef, params.MessageID)
		return "deleted", err
	})
}

func (c *TeamsJSONClient) GetMessageInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params messageInChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.GetMessage(context.TODO(), chatRef, params.MessageID)
	})
}

type ListMyChatsParams struct {
	ChatType string `json:"chatType"`
}

func (c *TeamsJSONClient) ListMyChats(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params ListMyChatsParams) (interface{}, error) {
		var chatType models.ChatType
		if params.ChatType != "" {
			chatType = models.ChatType(params.ChatType)
		}
		return c.client.Chats.ListChats(context.TODO(), &chatType)
	})
}

type listChatMessagesParams struct {
	StartTime time.Time `json:"startTime"`
	EndTime   time.Time `json:"endTime"`
	Top       *int32    `json:"top"`
}

func (c *TeamsJSONClient) ListMyChatMessages(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params listChatMessagesParams) (interface{}, error) {
		return c.client.Chats.ListAllMessages(context.TODO(), &params.StartTime, &params.EndTime, params.Top)
	})
}

func (c *TeamsJSONClient) ListPinnedMessagesInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params baseChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.ListPinnedMessages(context.TODO(), chatRef)
	})
}

func (c *TeamsJSONClient) PinMessageInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params messageInChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		err = c.client.Chats.PinMessage(context.TODO(), chatRef, params.MessageID)
		return "pinned", err
	})
}

func (c *TeamsJSONClient) UnpinMessageInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params messageInChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		err = c.client.Chats.UnpinMessage(context.TODO(), chatRef, params.MessageID)
		return "unpinned", err
	})
}

type mentionInChatParams struct {
	ChatRef     decoders.ChatRefDTO `json:"chatRef"`
	RawMentions []string            `json:"rawMentions"`
}

func (c *TeamsJSONClient) GetMentionsInChat(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params mentionInChatParams) (interface{}, error) {
		chatRef, err := decoders.GetChatRef(params.ChatRef)
		if err != nil {
			return nil, err
		}
		return c.client.Chats.GetMentions(context.TODO(), chatRef, params.RawMentions)
	})
}
