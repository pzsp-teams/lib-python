from dataclasses import dataclass
from teams_lib_pzsp2_z1.model.team import Team
from teams_lib_pzsp2_z1.model.channel import Channel
from teams_lib_pzsp2_z1.model.message import Message, MessageFrom
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
        self.messages = {
            "19:123123@thread.tacv2": [
                Message(
                    ID="msg-001",
                    Content="Hello, team!",
                    ContentType="text",
                    From=MessageFrom(
                        UserID="user-123-abc",
                        DisplayName="Alice"
                    ),
                    CreatedDateTime="2024-01-01T10:00:00Z",
                    ReplyCount=0,
                ),
                Message(
                    ID="msg-002",
                    Content="Don't forget the meeting at 3 PM.",
                    ContentType="text",
                    From=MessageFrom(
                        UserID="user-456-def",
                        DisplayName="Bob"
                    ),
                    CreatedDateTime="2024-01-01T11:00:00Z",
                    ReplyCount=2,
                ),
            ],
        }
        self.replies = {
            "msg-002": [
                Message(
                    ID="msg-002-reply-001",
                    Content="Thanks for the reminder!",
                    ContentType="text",
                    From=MessageFrom(
                        UserID="user-789-ghi",
                        DisplayName="Charlie"
                    ),
                    CreatedDateTime="2024-01-01T12:00:00Z",
                    ReplyCount=0,
                ),
                Message(
                    ID="msg-002-reply-002",
                    Content="I'll be there.",
                    ContentType="text",
                    From=MessageFrom(
                        UserID="user-123-abc",
                        DisplayName="Alice"
                    ),
                    CreatedDateTime="2024-01-01T12:30:00Z",
                    ReplyCount=0,
                ),
            ],
        }
        self.newGroupID = "group-789-ghi"
        self.newTeamName = "New Team"
        self.newGroupMailNickname = "new-team-nickname"
        self.newTeamVisibility = "private"
        self.potentialTeams = []
        self.newChannelName = "New Channel"
        self.newChannelID = "19:newchannelid@thread.tacv2"


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

    def get_create_channel_response(self, team_id: str, request_json: dict) -> dict:
        display_name = request_json.get("displayName")
        description = request_json.get("description", display_name)

        new_channel = Channel(
            ID=self.newChannelID,
            Name=display_name,
            IsGeneral=False,
        )

        if team_id not in self.channels:
            self.channels[team_id] = []

        self.channels[team_id].append(new_channel)

        return {
            "id": new_channel.ID,
            "displayName": new_channel.Name,
            "description": description,
            "isGeneral": new_channel.IsGeneral,
            "membershipType": "standard"
        }

    def get_delete_channel_response(self, team_id: str, channel_id: str) -> dict:
        channel = next((c for c in self.channels.get(team_id, []) if c.ID == channel_id), None)
        if not channel:
            return {"success": False}

        self.channels[team_id].remove(channel)
        return {"success": True}

    def get_list_messages_response(self, team_id: str, channel_id: str) -> dict:
        return {
            "value": [
                {
                    "id": message.ID,
                    "body": {
                        "content": message.Content,
                        "contentType": message.ContentType,
                    },
                    "from": {
                        "user": {
                            "id": message.From.UserID,
                            "displayName": message.From.DisplayName,
                        }
                    },
                    "createdDateTime": message.CreatedDateTime,
                    "replies": [{"id": f"dummy-reply-{i}"} for i in range(message.ReplyCount)]
                }
                for message in self.messages.get(channel_id, [])
            ],
        }

    def get_message_response(self, team_id: str, channel_id: str, message_id: str) -> dict | None:
        message = next((m for m in self.messages.get(channel_id, []) if m.ID == message_id), None)
        if not message:
            return None

        return {
            "id": message.ID,
            "body": {
                "content": message.Content,
                "contentType": message.ContentType,
            },
            "from": {
                "user": {
                    "id": message.From.UserID,
                    "displayName": message.From.DisplayName,
                }
            },
            "createdDateTime": message.CreatedDateTime,
            "replies": [{"id": f"dummy-reply-{i}"} for i in range(message.ReplyCount)]
        }







