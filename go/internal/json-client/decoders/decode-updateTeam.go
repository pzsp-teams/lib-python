package decoders

type UpdateTeamDTO struct {
	DisplayName *string `json:"displayName"`
	Description *string `json:"description"`
	Visibility  *string `json:"visibility"`
}
