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

func (jsonclient *TeamsJSONClient) CreateOneToOneChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createOneToOneChatParams](p)
	if err != nil {
		return nil, err
	}
	chat, err := jsonclient.client.Chats.CreateOneOneOne(context.TODO(), params.RecipientRef)
	if err != nil {
		return nil, err
	}
	return chat, nil
}

type createGroupChatParams struct {
	RecipientRefs []string `json:"recipientRefs"`
	Topic         string   `json:"topic"`
	IncludeMe     bool     `json:"includeMe"`
}

func (jsonclient *TeamsJSONClient) CreateGroupChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createGroupChatParams](p)
	if err != nil {
		return nil, err
	}
	chat, err := jsonclient.client.Chats.CreateGroup(context.TODO(), params.RecipientRefs, params.Topic, params.IncludeMe)
	if err != nil {
		return nil, err
	}
	return chat, nil
}

type groupChatMemberParams struct {
	GroupChatRef string `json:"groupChatRef"`
	UserRef      string `json:"userRef"`
}

func (jsonclient *TeamsJSONClient) AddMemberGroupToChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[groupChatMemberParams](p)
	if err != nil {
		return nil, err
	}
	member, err := jsonclient.client.Chats.AddMemberToGroupChat(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef}, params.UserRef)
	if err != nil {
		return nil, err
	}
	return member, nil
}

func (jsonclient *TeamsJSONClient) RemoveMemberFromGroupChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[groupChatMemberParams](p)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Chats.RemoveMemberFromGroupChat(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef}, params.UserRef)
	if err != nil {
		return nil, err
	}
	return "removed", nil
}

type listMembersInChatParams struct {
	GroupChatRef string `json:"groupChatRef"`
}

func (jsonclient *TeamsJSONClient) ListGroupChatMembers(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[listMembersInChatParams](p)
	if err != nil {
		return nil, err
	}
	members, err := jsonclient.client.Chats.ListGroupChatMembers(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef})
	if err != nil {
		return nil, err
	}
	return members, nil
}

type updateGroupChatTopicParams struct {
	GroupChatRef string `json:"groupChatRef"`
	Topic        string `json:"topic"`
}

func (jsonclient *TeamsJSONClient) UpdateGroupChatTopic(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[updateGroupChatTopicParams](p)
	if err != nil {
		return nil, err
	}
	chat, err := jsonclient.client.Chats.UpdateGroupChatTopic(context.TODO(), chats.GroupChatRef{Ref: params.GroupChatRef}, params.Topic)
	if err != nil {
		return nil, err
	}
	return chat, nil
}

type baseChatParams struct {
	ChatRef decoders.ChatRefDTO `json:"chatRef"`
}

func (jsonclient *TeamsJSONClient) ListMessagesInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[baseChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	messages, err := jsonclient.client.Chats.ListMessages(context.TODO(), chatRef)
	if err != nil {
		return nil, err
	}
	return messages, nil
}

type sendMessageInChatParams struct {
	ChatRef decoders.ChatRefDTO     `json:"chatRef"`
	Body    decoders.MessageBodyDTO `json:"body"`
}

func (jsonclient *TeamsJSONClient) SendMessageInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[sendMessageInChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	body, err := decoders.DecodeParams[models.MessageBody](&params.Body)
	if err != nil {
		return nil, err
	}
	message, err := jsonclient.client.Chats.SendMessage(context.TODO(), chatRef, *body)
	if err != nil {
		return nil, err
	}
	return message, nil
}

type messageInChatParams struct {
	ChatRef   decoders.ChatRefDTO `json:"chatRef"`
	MessageID string              `json:"messageId"`
}

func (jsonclient *TeamsJSONClient) DeleteMessageInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[messageInChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Chats.DeleteMessage(context.TODO(), chatRef, params.MessageID)
	if err != nil {
		return nil, err
	}
	return "deleted", nil
}

func (jsonclient *TeamsJSONClient) GetMessageInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[messageInChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	message, err := jsonclient.client.Chats.GetMessage(context.TODO(), chatRef, params.MessageID)
	if err != nil {
		return nil, err
	}
	return message, nil
}

type ListMyChatsParams struct {
	ChatType string `json:"chatType"`
}

func (jsonclient *TeamsJSONClient) ListMyChats(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[ListMyChatsParams](p)
	if err != nil {
		return nil, err
	}
	var chatType models.ChatType
	if params.ChatType != "" {
		chatType = models.ChatType(params.ChatType)
	}
	chatsList, err := jsonclient.client.Chats.ListChats(context.TODO(), &chatType)
	if err != nil {
		return nil, err
	}
	return chatsList, nil
}

type listChatMessagesParams struct {
	StartTime time.Time `json:"startTime"`
	EndTime   time.Time `json:"endTime"`
	Top       *int32    `json:"top"`
}

func (jsonclient *TeamsJSONClient) ListMyChatMessages(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[listChatMessagesParams](p)
	if err != nil {
		return nil, err
	}
	messages, err := jsonclient.client.Chats.ListAllMessages(context.TODO(), &params.StartTime, &params.EndTime, params.Top)
	if err != nil {
		return nil, err
	}
	return messages, nil
}

func (jsonclient *TeamsJSONClient) ListPinnedMessagesInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[baseChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	messages, err := jsonclient.client.Chats.ListPinnedMessages(context.TODO(), chatRef)
	if err != nil {
		return nil, err
	}
	return messages, nil
}

func (jsonclient *TeamsJSONClient) PinMessageInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[messageInChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Chats.PinMessage(context.TODO(), chatRef, params.MessageID)
	if err != nil {
		return nil, err
	}
	return "pinned", nil
}

func (jsonclient *TeamsJSONClient) UnpinMessageInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[messageInChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Chats.UnpinMessage(context.TODO(), chatRef, params.MessageID)
	if err != nil {
		return nil, err
	}
	return "unpinned", nil
}

type mentionInChatParams struct {
	ChatRef decoders.ChatRefDTO `json:"chatRef"`
	RawMentions []string		`json:"rawMentions"`
}

func (jsonclient *TeamsJSONClient) GetMentionsInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[mentionInChatParams](p)
	if err != nil {
		return nil, err
	}
	chatRef, err := decoders.GetChatRef(params.ChatRef)
	if err != nil {
		return nil, err
	}
	mentions, err := jsonclient.client.Chats.GetMentions(context.TODO(), chatRef, params.RawMentions)
	if err != nil {
		return nil, err
	}
	return mentions, nil
}
