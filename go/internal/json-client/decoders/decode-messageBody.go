package decoders

type MessageBodyDTO struct {
	ContentType string `json:"contentType"`
	Content     string `json:"content"`
}