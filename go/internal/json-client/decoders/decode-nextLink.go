package decoders

type NextLinkDTO struct {
	NextLink string `json:"nextLink"`
}

func GetNextLink(dto *NextLinkDTO) *string {
	if dto.NextLink == "" {
		return nil
	}
	return &dto.NextLink
}