package decoders

import(
	msmodels "github.com/microsoftgraph/msgraph-sdk-go/models"
)

type TeamPatchDTO struct {
	DisplayName       *string                  `json:"displayName"`
	Description       *string                  `json:"description"`
	Classification    *string                  `json:"classification"`
	Visibility        *string                  `json:"visibility"`
	IsArchived        *bool                    `json:"isArchived"`

	MemberSettings    *TeamMemberSettingsDTO    `json:"memberSettings"`
	GuestSettings     *TeamGuestSettingsDTO     `json:"guestSettings"`
	MessagingSettings *TeamMessagingSettingsDTO `json:"messagingSettings"`
	FunSettings       *TeamFunSettingsDTO       `json:"funSettings"`
}

type TeamMemberSettingsDTO struct {
	AllowCreateUpdateChannels        *bool `json:"allowCreateUpdateChannels"`
	AllowDeleteChannels              *bool `json:"allowDeleteChannels"`
	AllowAddRemoveApps               *bool `json:"allowAddRemoveApps"`
	AllowCreateUpdateRemoveTabs      *bool `json:"allowCreateUpdateRemoveTabs"`
	AllowCreateUpdateRemoveConnectors *bool `json:"allowCreateUpdateRemoveConnectors"`
}

type TeamGuestSettingsDTO struct {
	AllowCreateUpdateChannels *bool `json:"allowCreateUpdateChannels"`
	AllowDeleteChannels       *bool `json:"allowDeleteChannels"`
}

type TeamMessagingSettingsDTO struct {
	AllowUserEditMessages    *bool `json:"allowUserEditMessages"`
	AllowUserDeleteMessages  *bool `json:"allowUserDeleteMessages"`
	AllowOwnerDeleteMessages *bool `json:"allowOwnerDeleteMessages"`
	AllowTeamMentions        *bool `json:"allowTeamMentions"`
	AllowChannelMentions     *bool `json:"allowChannelMentions"`
}

type TeamFunSettingsDTO struct {
	AllowGiphy                   *bool   `json:"allowGiphy"`
	GiphyContentRating           *string `json:"giphyContentRating"`
	AllowStickersAndMemes        *bool   `json:"allowStickersAndMemes"`
	AllowCustomMemes             *bool   `json:"allowCustomMemes"`
}

func GetMSTeam(patch *TeamPatchDTO) *msmodels.Team {
	team := msmodels.NewTeam()

	if patch.DisplayName != nil {
		team.SetDisplayName(patch.DisplayName)
	}
	if patch.Description != nil {
		team.SetDescription(patch.Description)
	}
	if patch.Classification != nil {
		team.SetClassification(patch.Classification)
	}
	if patch.IsArchived != nil {
		team.SetIsArchived(patch.IsArchived)
	}
	if patch.Visibility != nil {
		switch *patch.Visibility {
		case "Public":
			v := msmodels.PUBLIC_TEAMVISIBILITYTYPE
			team.SetVisibility(&v)
		case "Private":
			v := msmodels.PRIVATE_TEAMVISIBILITYTYPE
			team.SetVisibility(&v)
		case "HiddenMembership":
			v := msmodels.HIDDENMEMBERSHIP_TEAMVISIBILITYTYPE
			team.SetVisibility(&v)
		}
	}

	if patch.MemberSettings != nil {
		msSettings := msmodels.NewTeamMemberSettings()
		p := patch.MemberSettings
		if p.AllowCreateUpdateChannels != nil { msSettings.SetAllowCreateUpdateChannels(p.AllowCreateUpdateChannels) }
		if p.AllowDeleteChannels != nil { msSettings.SetAllowDeleteChannels(p.AllowDeleteChannels) }
		if p.AllowAddRemoveApps != nil { msSettings.SetAllowAddRemoveApps(p.AllowAddRemoveApps) }
		if p.AllowCreateUpdateRemoveTabs != nil { msSettings.SetAllowCreateUpdateRemoveTabs(p.AllowCreateUpdateRemoveTabs) }
		if p.AllowCreateUpdateRemoveConnectors != nil { msSettings.SetAllowCreateUpdateRemoveConnectors(p.AllowCreateUpdateRemoveConnectors) }

		team.SetMemberSettings(msSettings)
	}

	if patch.GuestSettings != nil {
		msSettings := msmodels.NewTeamGuestSettings()
		p := patch.GuestSettings
		if p.AllowCreateUpdateChannels != nil { msSettings.SetAllowCreateUpdateChannels(p.AllowCreateUpdateChannels) }
		if p.AllowDeleteChannels != nil { msSettings.SetAllowDeleteChannels(p.AllowDeleteChannels) }

		team.SetGuestSettings(msSettings)
	}

	if patch.MessagingSettings != nil {
		msSettings := msmodels.NewTeamMessagingSettings()
		p := patch.MessagingSettings
		if p.AllowUserEditMessages != nil { msSettings.SetAllowUserEditMessages(p.AllowUserEditMessages) }
		if p.AllowUserDeleteMessages != nil { msSettings.SetAllowUserDeleteMessages(p.AllowUserDeleteMessages) }
		if p.AllowOwnerDeleteMessages != nil { msSettings.SetAllowOwnerDeleteMessages(p.AllowOwnerDeleteMessages) }
		if p.AllowTeamMentions != nil { msSettings.SetAllowTeamMentions(p.AllowTeamMentions) }
		if p.AllowChannelMentions != nil { msSettings.SetAllowChannelMentions(p.AllowChannelMentions) }

		team.SetMessagingSettings(msSettings)
	}

	if patch.FunSettings != nil {
		msSettings := msmodels.NewTeamFunSettings()
		p := patch.FunSettings
		if p.AllowGiphy != nil { msSettings.SetAllowGiphy(p.AllowGiphy) }
		if p.GiphyContentRating != nil {
			switch *p.GiphyContentRating {
			case "moderate":
				v := msmodels.MODERATE_GIPHYRATINGTYPE
				msSettings.SetGiphyContentRating(&v)
			case "strict":
				v := msmodels.STRICT_GIPHYRATINGTYPE
				msSettings.SetGiphyContentRating(&v)
			default:
				v := msmodels.MODERATE_GIPHYRATINGTYPE
				msSettings.SetGiphyContentRating(&v)
			}
}
		if p.AllowStickersAndMemes != nil { msSettings.SetAllowStickersAndMemes(p.AllowStickersAndMemes) }
		if p.AllowCustomMemes != nil { msSettings.SetAllowCustomMemes(p.AllowCustomMemes) }

		team.SetFunSettings(msSettings)
	}

	return team
}