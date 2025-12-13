from dataclasses import dataclass
from teams_lib_pzsp2_z1.model.team import Team
from teams_lib_pzsp2_z1.model.channel import Channel

@dataclass
class FakeServerData:
    teams: list[Team]
    channels: dict[str, list[Channel]]

    def __init__(self) -> FakeServerData:
        self.teams = [
            Team(
                ID="team-123-abc",
                DisplayName="Test Team",
                Description="A team for testing",
                IsArchived=False,
                Visibility="Private",
            ),
        ]
        self.channels = {
            "team-123-abc": [
                Channel(
                    ID="19:123123@thread.tacv2",
                    Name="General",
                    IsGeneral=True,
                ),
                Channel(
                    ID="19:999999@thread.tacv2",
                    Name="Development",
                    IsGeneral=False,
                ),
            ],
        }

    def get_myJoinedTeams_response(self) -> dict:
        return {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#teams",
            "value": [
                {
                    "id": team.ID,
                    "displayName": team.DisplayName,
                    "description": team.Description,
                    "isArchived": team.IsArchived,
                    "visibility": team.Visibility,
                }
                for team in self.teams
            ],
        }

    def get_listChannels_response(self, team_id: str) -> dict:
        return {
            "@odata.context": f"https://graph.microsoft.com/v1.0/$metadata#teams('{team_id}')/channels",
            "value": [
                {
                    "id": channel.ID,
                    "displayName": channel.Name,
                    "isGeneral": channel.IsGeneral,
                }
                for channel in self.channels.get(team_id, [])
            ],
        }