from dataclasses import dataclass
from teams_lib_pzsp2_z1.model.team import Team
from teams_lib_pzsp2_z1.model.channel import Channel
from dataclasses import field

@dataclass
class FakeServerData:
    teams: list[Team]
    channels: dict[str, list[Channel]]

    newGroupID: str
    newTeamName: str
    newGroupMailNickname: str
    newTeamVisibility: str
    potentialTeams: list[Team] = field(default_factory=list)

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
            ),
            Team(
                ID="archived-team-789-ghi",
                DisplayName="Archived Team",
                Description="An archived team for testing",
                IsArchived=True,
                Visibility="private",
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
        self.newGroupID = "group-789-ghi"
        self.newTeamName = "New Team"
        self.newGroupMailNickname = "new-team-nickname"
        self.newTeamVisibility = "private"
        self.potentialTeams = []


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

    def get_updateTeam_response(self, team_id: str, update_json: dict) -> dict | None:
        team = next((t for t in self.teams if t.ID == team_id), None)
        if not team:
            return None

        if "displayName" in update_json:
            team.DisplayName = update_json["displayName"]
        if "description" in update_json:
            team.Description = update_json["description"]
        if "visibility" in update_json:
            team.Visibility = update_json["visibility"]

        return {
            "id": team.ID,
            "displayName": team.DisplayName,
            "description": team.Description,
            "isArchived": team.IsArchived,
            "visibility": team.Visibility,
        }

    def get_createGroup_response(self, request_json: dict) -> dict:
        visibility = request_json.get("visibility").lower()
        if visibility not in ("private", "public"):
            visibility = "private"

        self.potentialTeams.append(
            Team(
                ID=self.newGroupID,
                DisplayName=request_json.get("displayName"),
                Description=request_json.get("description"),
                IsArchived=False,
                Visibility=visibility,
            )
        )

        return {
            "id": self.newGroupID,
            "displayName": request_json.get("displayName"),
            "description": request_json.get("displayName"),
            "visibility": visibility,
            "groupTypes": ["Unified"],
            "mailEnabled": True,
            "mailNickname": request_json.get("mailNickname"),
            "securityEnabled": False,
            "createdDateTime": "2024-01-01T00:00:00Z",
        }

    def get_createTeamViaGroup_response(self, group_id: str) -> dict:
        team = next((t for t in self.potentialTeams if t.ID == group_id), None)
        if not team:
            return {}

        self.teams.append(team)

        return {
            "id": team.ID,
            "displayName": team.DisplayName,
            "description": team.Description,
            "isArchived": team.IsArchived,
            "visibility": team.Visibility,
        }

    def get_createTeamFromTemplate_response(self, request_json: dict) -> dict:
        new_team_id = "team-from-template-001"
        new_team = Team(
            ID=new_team_id,
            DisplayName=request_json.get("displayName"),
            Description=request_json.get("description"),
            IsArchived=False,
            Visibility="private",
        )
        self.teams.append(new_team)

        return {
            "id": new_team_id,
        }

    def get_archiveTeam_response(self, team_id: str) -> dict:
        team = next((t for t in self.teams if t.ID == team_id), None)
        if not team:
            return {"success": False}

        team.IsArchived = True
        return {"success": True}

    def get_unarchiveTeam_response(self, team_id: str) -> dict:
        team = next((t for t in self.teams if t.ID == team_id), None)
        if not team:
            return {"success": False}

        team.IsArchived = False
        return {"success": True}

    def get_deleteTeam_response(self, team_id: str) -> dict:
        team = next((t for t in self.teams if t.ID == team_id), None)
        if not team:
            return {"success": False}

        self.teams.remove(team)
        return {"success": True}

    def get_restoreTeam_response(self, team_id: str) -> dict:
        archived_team = next((t for t in self.teams if t.ID == team_id and t.IsArchived), None)
        if not archived_team:
            return {"success": False}

        archived_team.IsArchived = False
        return {
            "id": archived_team.ID,
            "displayName": archived_team.DisplayName,
            "description": archived_team.Description,
            "isArchived": archived_team.IsArchived,
            "visibility": archived_team.Visibility,
            "mailNickname": self.newGroupMailNickname
        }

    def get_channel_response(self, team_id: str, channel_id: str) -> dict | None:
        channel = next((c for c in self.channels.get(team_id, []) if c.ID == channel_id), None)
        if not channel:
            return None

        return {
            "id": channel.ID,
            "displayName": channel.Name,
            "isGeneral": channel.IsGeneral,
        }






