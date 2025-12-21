package decoders

import (
	"github.com/mitchellh/mapstructure"
)

func DecodeParams[T any](p interface{}) (*T, error) {
    var result T

    config := &mapstructure.DecoderConfig{
        Metadata: nil,
        Result:   &result,
        TagName:  "json",
        WeaklyTypedInput: true,
    }

    decoder, err := mapstructure.NewDecoder(config)
    if err != nil {
        return nil, err
    }

    if err := decoder.Decode(p); err != nil {
        return nil, err
    }

    return &result, nil
}