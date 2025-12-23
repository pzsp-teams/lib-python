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
                Visibility="private",
            ),
            Team(
                ID="team-456-def",
                DisplayName="Another Team",
                Description="Another team for testing",
                IsArchived=False,
                Visibility="public",
            )
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
            "value": [
                {
                    "id": channel.ID,
                    "displayName": channel.Name,
                    "isGeneral": channel.IsGeneral,
                }
                for channel in self.channels.get(team_id, [])
            ],
        }

    def get_team_response(self, team_id: str) -> dict | None:
        return {
            "id": team.ID,
            "displayName": team.DisplayName,
            "description": team.Description,
            "isArchived": team.IsArchived,
            "visibility": team.Visibility,
        } if (team := next((t for t in self.teams if t.ID == team_id), None)) else None



