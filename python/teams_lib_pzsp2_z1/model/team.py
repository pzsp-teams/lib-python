from dataclasses import dataclass


@dataclass
class Team:
    ID: str
    DisplayName: str
    Description: str
    IsArchived: bool
    Visibility: str


@dataclass
class MSTeamsUpdate:
    DisplayName: str | None = None
    Description: str | None = None
    Classification: str | None = None
    Visibility: str | None = None
    IsArchived: bool | None = None
    MemberSettings: "TeamMemberSettingsDTO | None" = None
    GuestSettings: "TeamGuestSettingsDTO | None" = None
    MessagingSettings: "TeamMessagingSettingsDTO | None" = None
    FunSettings: "TeamFunSettingsDTO | None" = None

    @dataclass
    class TeamMemberSettingsDTO:
        AllowCreateUpdateChannels: bool | None = None
        AllowDeleteChannels: bool | None = None
        AllowAddRemoveApps: bool | None = None
        AllowCreateUpdateRemoveTabs: bool | None = None
        AllowCreateUpdateRemoveConnectors: bool | None = None

    @dataclass
    class TeamGuestSettingsDTO:
        AllowCreateUpdateChannels: bool | None = None
        AllowDeleteChannels: bool | None = None

    @dataclass
    class TeamMessagingSettingsDTO:
        AllowUserEditMessages: bool | None = None
        AllowUserDeleteMessages: bool | None = None
        AllowOwnerDeleteMessages: bool | None = None
        AllowTeamMentions: bool | None = None
        AllowChannelMentions: bool | None = None

    @dataclass
    class TeamFunSettingsDTO:
        AllowGiphy: bool | None = None
        GiphyContentRating: str | None = None
        AllowStickersAndMemes: bool | None = None
        AllowCustomMemes: bool | None = None
