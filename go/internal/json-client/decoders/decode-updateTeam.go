package decoders

import (
	"github.com/pzsp-teams/lib/models"
)

type UpdateTeamDTO struct {
	DisplayName string `json:"displayName"`
	Description string `json:"description"`
	Visibility  string `json:"visibility"`
}

func GetUpdateTeam(dto *UpdateTeamDTO) models.TeamUpdate {
	update := models.TeamUpdate{}

	if dto.DisplayName != "" {
		update.DisplayName = &dto.DisplayName
	}
	if dto.Description != "" {
		update.Description = &dto.Description
	}
	if dto.Visibility != "" {
		update.Visibility = &dto.Visibility
	}

	return update
}
