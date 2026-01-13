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
	IsRead      *bool          `json:"isRead"`
	IsMentioned *bool          `json:"isMentioned"`
	To          []string      `json:"to"`
	NotTo       []string      `json:"notTo"`
	StartTime   time.Time     `json:"startTime"`
	EndTime     time.Time     `json:"endTime"`
	Interval    string        `json:"interval"`
	NotFromMe   *bool          `json:"notFromMe"`
	NotToMe     *bool          `json:"notToMe"`
	FromMe      *bool          `json:"fromMe"`
	ToMe        *bool          `json:"toMe"`
}

func DecodeSearchMessageOptions(dto *SearchMessageOptionsDTO) *search.SearchMessagesOptions {
	if dto == nil {
		return nil
	}

	interval := search.TimeInterval(dto.Interval)

	options := &search.SearchMessagesOptions{}
	if dto.Query != "" {
		options.Query = &dto.Query
	}
	options.SearchPage = DecodeSearchPage(&dto.SearchPage)
	if len(dto.From) > 0 {
		options.From = dto.From
	}
	if len(dto.NotFrom) > 0 {
		options.NotFrom = dto.NotFrom
	}
	options.IsRead = dto.IsRead
	options.IsMentioned = dto.IsMentioned
	if len(dto.To) > 0 {
		options.To = dto.To
	}
	if len(dto.NotTo) > 0 {
		options.NotTo = dto.NotTo
	}
	if !dto.StartTime.IsZero() {
		options.StartTime = &dto.StartTime
	}
	if !dto.EndTime.IsZero() {
		options.EndTime = &dto.EndTime
	}
	if dto.Interval != "" {
		options.Interval = &interval
	}
	if dto.NotFromMe != nil {
        options.NotFromMe = *dto.NotFromMe
    }
    if dto.NotToMe != nil {
        options.NotToMe = *dto.NotToMe
    }
    if dto.FromMe != nil {
        options.FromMe = *dto.FromMe
    }
    if dto.ToMe != nil {
        options.ToMe = *dto.ToMe
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
