package decoders

import (
	"time"

	"github.com/pzsp-teams/lib/search"
)

type SearchConfigDTO struct {
	MaxWorkers int `json:"maxWorkers"`
}

type SearchPageDTO struct {
	From *int `json:"from"`
	Size *int `json:"size"`
}

type SearchMessageOptionsDTO struct {
	Query       string        `json:"query"`
	SearchPage  SearchPageDTO `json:"searchPage"`
	From        []string      `json:"from"`
	NotFrom     []string      `json:"notFrom"`
	IsRead      bool          `json:"isRead"`
	IsMentioned bool          `json:"isMentioned"`
	To          []string      `json:"to"`
	NotTo       []string      `json:"notTo"`
	StartTime   time.Time     `json:"startTime"`
	EndTime     time.Time     `json:"endTime"`
	Interval    string        `json:"interval"`
	NotFromMe   bool          `json:"notFromMe"`
	NotToMe     bool          `json:"notToMe"`
	FromMe      bool          `json:"fromMe"`
	ToMe        bool          `json:"toMe"`
}

func DecodeSearchMessageOptions(dto *SearchMessageOptionsDTO) *search.SearchMessagesOptions {
	if dto == nil {
		return nil
	}

	interval := search.TimeInterval(dto.Interval)

	options := &search.SearchMessagesOptions{
		Query:       &dto.Query,
		SearchPage:  DecodeSearchPage(&dto.SearchPage),
		From:        dto.From,
		NotFrom:     dto.NotFrom,
		IsRead:      &dto.IsRead,
		IsMentioned: &dto.IsMentioned,
		To:          dto.To,
		NotTo:       dto.NotTo,
		StartTime:   &dto.StartTime,
		EndTime:     &dto.EndTime,
		Interval:    &interval,
		NotFromMe:   dto.NotFromMe,
		NotToMe:     dto.NotToMe,
		FromMe:      dto.FromMe,
		ToMe:        dto.ToMe,
	}
	return options
}

func DecodeSearchPage(dto *SearchPageDTO) *search.SearchPage {
	if dto == nil {
		return nil
	}

	page := &search.SearchPage{}
	if dto.From != nil {
		from := int32(*dto.From)
		page.From = &from
	}
	if dto.Size != nil {
		size := int32(*dto.Size)
		page.Size = &size
	}

	return page
}
