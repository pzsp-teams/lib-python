package decoders

import (
	"fmt"

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

func GetChatRef(dto ChatRefDTO) (chats.ChatRef, error) {
	switch dto.Type {
	case ChatTypeGroup:
		return chats.GroupChatRef{Ref: dto.Ref}, nil
	case ChatTypeOneOnOne:
		return chats.OneOnOneChatRef{Ref: dto.Ref}, nil
	default:
		return nil, fmt.Errorf("unknown chat type: %s", dto.Type)
	}
}


