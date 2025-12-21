package decoders

import(
	msmodels "github.com/microsoftgraph/msgraph-sdk-go/models"
)

type TeamPatchDTO struct {
    DisplayName *string `json:"displayName"`
    Description *string `json:"description"`
    // Dodaj inne pola, które chcesz aktualizować...
}

func GetMSTeam(patch *TeamPatchDTO) *msmodels.Team {
	team := msmodels.NewTeam()

	if patch.DisplayName != nil {
		team.SetDisplayName(patch.DisplayName)
	}
	if patch.Description != nil {
		team.SetDescription(patch.Description)
	}
	// Ustaw inne pola w podobny sposób...

	return team
}