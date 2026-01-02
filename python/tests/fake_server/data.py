from dataclasses import dataclass
from teams_lib_pzsp2_z1.model.team import Team
from teams_lib_pzsp2_z1.model.chat import Chat, ChatType
from teams_lib_pzsp2_z1.model.channel import Channel
from teams_lib_pzsp2_z1.model.message import Message, MessageFrom
from teams_lib_pzsp2_z1.model.member import Member
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
                    Name="Something",
                    IsGeneral=False,
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
        self.members = {
            "team-123-abc": {
                "19:123123@thread.tacv2": [
                    Member(
                        ID="user-123-abc",
                        UserID="user-123-abc",
                        DisplayName="Alice",
                        Role="owner",
                        Email="alice@example.com"
                    ),
                    Member(
                        ID="user-456-def",
                        UserID="user-456-def",
                        DisplayName="Bob",
                        Role="member",
                        Email="bob@example.com"
                    ),
                ],
            }
        }
        self.group_chats = [
            Chat(
                ID="chat-123-abc",
                Type=ChatType.GROUP,
                IsHidden=False,
                Topic="Project Discussion",
            ),
            Chat(
                ID="chat-456-def",
                Type=ChatType.GROUP,
                IsHidden=True,
                Topic="Secret Plans",
            ),
        ]
        self.oneonone_chats = [
            Chat(
                ID="chat-789-ghi",
                Type=ChatType.ONEONONE,
                IsHidden=False,
                Topic="",
            ),
        ]
        self.newGroupID = "group-789-ghi"
        self.newTeamName = "New Team"
        self.newGroupMailNickname = "new-team-nickname"
        self.newTeamVisibility = "private"
        self.potentialTeams = []
        self.newChannelName = "New Channel"
        self.newChannelID = "19:newchannelid@thread.tacv2"
        self.newMessageTemplate = Message(
            ID="new-message-id",
            Content="This is a new message.",
            ContentType="text",
            From=MessageFrom(
                UserID="user-new-001",
                DisplayName="New User"
            ),
            CreatedDateTime="2024-01-02T10:00:00Z",
            ReplyCount=0,
        )
        self.newMemberTemplate = Member(
            ID="user-new-002",
            UserID="new-user-002",
            DisplayName="New Member",
            Role="owner",
            Email="newmember@example.com"
        )




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
            "@odata.context": f"https://graph.microsoft.com/v1.0/$metadata#teams('{team_id}')/channels",
            "value": [
                {
                    "@odata.type": "#microsoft.graph.channel",
                    "id": channel.ID,
                    "displayName": channel.Name,
                    "isGeneral": channel.IsGeneral,
                    "membershipType": "standard",
                    "email": ""
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

    def get_send_message_response(self, team_id: str, channel_id: str, request_json: dict) -> dict:
        return {
            "id": self.newMessageTemplate.ID,
            "body": {
                "content": request_json.get("body", {}).get("content"),
                "contentType": request_json.get("body", {}).get("contentType"),
            },
            "from": {
                "user": {
                    "id": self.newMessageTemplate.From.UserID,
                    "displayName": self.newMessageTemplate.From.DisplayName,
                }
            },
            "createdDateTime": self.newMessageTemplate.CreatedDateTime,
        }

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

    def get_list_replies_response(self, team_id: str, channel_id: str, message_id: str) -> dict:
        return {
            "value": [
                {
                    "id": reply.ID,
                    "body": {
                        "content": reply.Content,
                        "contentType": reply.ContentType,
                    },
                    "from": {
                        "user": {
                            "id": reply.From.UserID,
                            "displayName": reply.From.DisplayName,
                        }
                    },
                    "createdDateTime": reply.CreatedDateTime,
                }
                for reply in self.replies.get(message_id, [])
            ],
        }

    def get_reply_response(self, team_id: str, channel_id: str, message_id: str, reply_id: str) -> dict | None:
        reply = next((r for r in self.replies.get(message_id, []) if r.ID == reply_id), None)
        if not reply:
            return None

        return {
            "id": reply.ID,
            "body": {
                "content": reply.Content,
                "contentType": reply.ContentType,
            },
            "from": {
                "user": {
                    "id": reply.From.UserID,
                    "displayName": reply.From.DisplayName,
                }
            },
            "createdDateTime": reply.CreatedDateTime,
        }

    def get_add_member_response(self, team_id: str, request_json: dict) -> dict:
        roles = []
        if self.newMemberTemplate.Role == "owner":
            roles = ["owner"]

        return {
            "@odata.context": f"https://graph.microsoft.com/v1.0/$metadata#teams('{team_id}')/members/$entity",
            "@odata.type": "#microsoft.graph.aadUserConversationMember",

            "id": self.newMemberTemplate.ID,
            "roles": roles,
            "displayName": self.newMemberTemplate.DisplayName,
            "userId": self.newMemberTemplate.UserID,
            "email": self.newMemberTemplate.Email,
        }

    def get_update_member_role_response(self, team_id: str, channel_id: str, member_id: str, request_json: dict) -> dict | None:
        channel_members = self.members.get(team_id, {}).get(channel_id, [])

        member = next((m for m in channel_members if m.ID == member_id), None)
        if not member:
            return None

        if "roles" in request_json:
            member.Role = "owner" if "owner" in request_json["roles"] else "member"

        return {
            "@odata.context": f"https://graph.microsoft.com/v1.0/$metadata#teams('{team_id}')/channels('{channel_id}')/members/$entity",
            "@odata.type": "#microsoft.graph.aadUserConversationMember",
            "id": member.ID,
            "userId": member.UserID,
            "displayName": member.DisplayName,
            "roles": [member.Role] if member.Role == "owner" else [],
            "email": member.Email,
        }

    def get_list_members_response(self, team_id: str, channel_id: str) -> dict:
        return {
            "@odata.context": f"https://graph.microsoft.com/v1.0/$metadata#teams('{team_id}')/channels('{channel_id}')/members",
            "value": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "id": member.ID,
                    "userId": member.UserID,
                    "displayName": member.DisplayName,
                    "roles": [member.Role] if member.Role == "owner" else [],
                    "email": member.Email,
                }
                for member in self.members.get(team_id, {}).get(channel_id, [])
            ],
        }

    def get_remove_member_response(self, team_id: str, channel_id: str, member_id: str) -> dict:
        channel_members = self.members.get(team_id, {}).get(channel_id, [])

        member = next((m for m in channel_members if m.ID == member_id), None)
        if not member:
            return {"success": False}

        channel_members.remove(member)
        return {"success": True}

    def get_list_chats_response(self, chat_type: ChatType) -> dict:
        if chat_type == ChatType.ONEONONE:
            chats = self.oneonone_chats
        else:
            chats = self.group_chats

        print(chat_type)
        print(chat_type == ChatType.ONEONONE)

        return {
            "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#chats",
            "@odata.count": len(chats),
            "value": [
                {
                    "id": chat.ID,
                    "chatType": "oneOnOne" if chat.Type == ChatType.ONEONONE else "group",
                    "isHiddenForAllMembers": chat.IsHidden,
                    "topic": chat.Topic,
                }
                for chat in chats
            ],
        }


