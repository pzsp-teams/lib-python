package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
)

type createOneToOneChatParams struct {
	OwnerEmail     string `json:"ownerEmail"`
	RecipientEmail string `json:"recipientEmail"`
}

func (jsonclient *TeamsJSONClient) CreateOneToOneChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createOneToOneChatParams](p)
	if err != nil {
		return nil, err
	}
	chat, err := jsonclient.client.Chats.CreateOneToOne(context.TODO(), params.OwnerEmail, params.RecipientEmail)
	if err != nil {
		return nil, err
	}
	return chat, nil
}

type createGroupChatParams struct {
	OwnerEmail   string   `json:"ownerEmail"`
	MemberEmails []string `json:"memberEmails"`
	Topic        string   `json:"topic"`
}

func (jsonclient *TeamsJSONClient) CreateGroupChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createGroupChatParams](p)
	if err != nil {
		return nil, err
	}
	chat, err := jsonclient.client.Chats.CreateGroup(context.TODO(), params.OwnerEmail, params.MemberEmails, params.Topic)
	if err != nil {
		return nil, err
	}
	return chat, nil
}

type sendMessageInChatParams struct {
	ChatID  string `json:"chatID"`
	Content string `json:"content"`
}

func (jsonclient *TeamsJSONClient) SendMessageInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[sendMessageInChatParams](p)
	if err != nil {
		return nil, err
	}
	message, err := jsonclient.client.Chats.SendMessage(context.TODO(), params.ChatID, params.Content)
	if err != nil {
		return nil, err
	}
	return message, nil
}

func (jsonclient *TeamsJSONClient) ListMyChats(_ map[string]interface{}) (interface{}, error) {
	chats, err := jsonclient.client.Chats.ListMyJoined(context.TODO())
	if err != nil {
		return nil, err
	}
	return chats, nil
}

type listMembersInChatParams struct {
	ChatID string `json:"chatID"`
}

func (jsonclient *TeamsJSONClient) ListMembersInChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[listMembersInChatParams](p)
	if err != nil {
		return nil, err
	}
	members, err := jsonclient.client.Chats.ListMembers(context.TODO(), params.ChatID)
	if err != nil {
		return nil, err
	}
	return members, nil
}

type addMemberToChatParams struct {
	ChatID    string `json:"chatID"`
	Email string `json:"email"`
}

func (jsonclient *TeamsJSONClient) AddMemberToChat(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[addMemberToChatParams](p)
	if err != nil {
		return nil, err
	}
	member, err := jsonclient.client.Chats.AddMember(context.TODO(), params.ChatID, params.Email)
	if err != nil {
		return nil, err
	}
	return member, nil
}
