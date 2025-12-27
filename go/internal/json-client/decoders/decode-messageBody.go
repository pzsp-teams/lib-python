package decoders

import (
	"github.com/mitchellh/mapstructure"
	"github.com/pzsp-teams/lib/models"
)

type messageBodyDTO struct {
	ContentType string `json:"contentType"`
	Content     string `json:"content"`
}

func DecodeMessageBody(body *messageBodyDTO) (*models.MessageBody, error) {
	var result models.MessageBody

	config := &mapstructure.DecoderConfig{
		Metadata:        nil,
		Result:          &result,
		TagName:         "json",
		WeaklyTypedInput: true,
	}

	decoder, err := mapstructure.NewDecoder(config)
	if err != nil {
		return nil, err
	}

	if err := decoder.Decode(body); err != nil {
		return nil, err
	}

	return &result, nil
}
