package decoders

import (
	"github.com/pzsp-teams/lib/chats"
)

type ChatRefDTO struct {
	Ref  string `json:"ref"`
	Type string `json:"type"`
}

const (
	ChatTypeGroup = "group"
	ChatTypeOneOnOne = "oneOnOne"
)

func GetChatRef(dto ChatRefDTO) chats.ChatRef {
	switch dto.Type {
	case ChatTypeGroup:
		return chats.GroupChatRef{Ref: dto.Ref}
	case ChatTypeOneOnOne:
		return chats.OneOnOneChatRef{Ref: dto.Ref}
	default:
		return nil
	}
}


