from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from unittest import result
from urllib import request

from werkzeug import Response

from teams_lib_pzsp2_z1.model.team import Team
from teams_lib_pzsp2_z1.model.chat import Chat, ChatType
from teams_lib_pzsp2_z1.model.channel import Channel
from teams_lib_pzsp2_z1.model.message import Message, MessageFrom
from teams_lib_pzsp2_z1.model.member import Member

# --- Constants for OData ---
ODATA_CONTEXT = "@odata.context"
ODATA_TYPE = "@odata.type"
ODATA_COUNT = "@odata.count"
GRAPH_URL = "https://graph.microsoft.com/v1.0/$metadata"

@dataclass
class FakeServerData:
    teams: List[Team]
    channels: Dict[str, List[Channel]]

    # State tracking variables
    newGroupID: str
    newTeamName: str
    newGroupMailNickname: str
    newTeamVisibility: str
    potentialTeams: List[Team] = field(default_factory=list)

    # Initial data containers
    messages: Dict[str, List[Message]] = field(default_factory=dict)
    replies: Dict[str, List[Message]] = field(default_factory=dict)
    members: Dict[str, Dict[str, List[Member]]] = field(default_factory=dict)
    group_chat_members: Dict[str, List[Member]] = field(default_factory=dict)
    chat_messages: Dict[str, List[Message]] = field(default_factory=dict)
    users: List[Member] = field(default_factory=list)
    me: Member = field(default_factory=Member) # type: ignore
    group_chats: List[Chat] = field(default_factory=list)
    oneonone_chats: List[Chat] = field(default_factory=list)

    # Templates and temporary state
    newChannelName: str = "New Channel"
    newChannelID: str = "19:newchannelid@thread.tacv2"
    newMessageTemplate: Message = field(default_factory=lambda: Message(
        id="new-message-id",
        content="This is a new message.",
        content_type="text",
        sender=MessageFrom(user_id="user-new-001", display_name="New User"),
        created_date_time="2024-01-02T10:00:00Z",
        reply_count=0,
    ))
    newMemberTemplate: Member = field(default_factory=lambda: Member(
        id="user-new-002", user_id="new-user-002", display_name="New Member",
        role="owner", email="newmember@example.com"
    ))
    newChatTemplate: Chat = field(default_factory=lambda: Chat(
        id="new-chat-001", type=ChatType.GROUP, is_hidden=False, topic="New Chat Topic"
    ))
    updatedGroupChatTopic: str = "Updated Chat Topic"

    def __init__(self) -> None:
        # --- Teams ---
        self.teams = [
            Team(id="team-123-abc", display_name="Test Team", description="A team for testing", is_archived=False, visibility="private"),
            Team(id="team-456-def", display_name="Another Team", description="Another team for testing", is_archived=False, visibility="public"),
            Team(id="archived-team-789-ghi", display_name="Archived Team", description="An archived team for testing", is_archived=True, visibility="private")
        ]
        self.potentialTeams = []

        # --- Channels ---
        self.channels = {
            "team-123-abc": [
                Channel(id="19:123123@thread.tacv2", name="Something", is_general=False),
                Channel(id="19:999999@thread.tacv2", name="Development", is_general=False),
            ],
        }

        # --- Messages (Channel) ---
        self.messages = {
            "19:123123@thread.tacv2": [
                Message(id="msg-001", content="Hello, team!", content_type="text", sender=MessageFrom(user_id="user-123-abc", display_name="Alice"), created_date_time="2024-01-01T10:00:00Z", reply_count=0),
                Message(id="msg-002", content="Don't forget the meeting at 3 PM.", content_type="text", sender=MessageFrom(user_id="user-456-def", display_name="Bob"), created_date_time="2024-01-01T11:00:00Z", reply_count=2),
            ],
        }

        # --- Replies ---
        self.replies = {
            "msg-002": [
                Message(id="msg-002-reply-001", content="Thanks for the reminder!", content_type="text", sender=MessageFrom(user_id="user-789-ghi", display_name="Charlie"), created_date_time="2024-01-01T12:00:00Z", reply_count=0),
                Message(id="msg-002-reply-002", content="I'll be there.", content_type="text", sender=MessageFrom(user_id="user-123-abc", display_name="Alice"), created_date_time="2024-01-01T12:30:00Z", reply_count=0),
            ],
        }

        # --- Members (Channel) ---
        self.members = {
            "team-123-abc": {
                "19:123123@thread.tacv2": [
                    Member(id="user-123-abc", user_id="user-123-abc", display_name="Alice", role="owner", email="alice@example.com"),
                    Member(id="user-456-def", user_id="user-456-def", display_name="Bob", role="member", email="bob@example.com"),
                ],
            }
        }

        # --- Users ---
        self.users = [
            Member(id="user-123-abc", user_id="user-123-abc", display_name="Alice", role="owner", email="alice@example.com"),
            Member(id="user-456-def", user_id="user-456-def", display_name="Bob", role="member", email="bob@example.com"),
        ]
        self.me = Member(id="user-me-001", user_id="user-me-001", display_name="Current User", role="member", email="me@example.com")

        # --- Chats & Chat Members/Messages ---
        self.group_chats = [
            Chat(id="chat-123-abc", type=ChatType.GROUP, is_hidden=False, topic="Project Discussion"),
            Chat(id="chat-456-def", type=ChatType.GROUP, is_hidden=True, topic="Secret Plans"),
        ]
        self.oneonone_chats = [
            Chat(id="chat-789-ghi", type=ChatType.ONE_ON_ONE, is_hidden=False, topic=""),
        ]

        self.group_chat_members = {
            "chat-123-abc": [
                Member(id="user-123-abc", user_id="user-123-abc", display_name="Alice", role="owner", email="alice@example.com"),
                Member(id="user-456-def", user_id="user-456-def", display_name="Bob", role="member", email="bob@example.com"),
            ],
        }

        self.chat_messages = {
            "chat-123-abc": [
                Message(id="msg-001", content="Hello, team!", content_type="text", sender=MessageFrom(user_id="user-123-abc", display_name="Alice"), created_date_time="2024-01-01T10:00:00Z", reply_count=0),
                Message(id="msg-002", content="Don't forget the meeting at 3 PM.", content_type="text", sender=MessageFrom(user_id="user-456-def", display_name="Bob"), created_date_time="2024-01-01T11:00:00Z", reply_count=2),
            ],
        }

        # --- State Variables ---
        self.newGroupID = "group-789-ghi"
        self.newTeamName = "New Team"
        self.newGroupMailNickname = "new-team-nickname"
        self.newTeamVisibility = "private"
        self.newTeamID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"

        # Init Templates (re-assigning to ensure freshness if needed, though default_factory handles it)
        self.newChannelName = "New Channel"
        self.newChannelID = "19:newchannelid@thread.tacv2"
        self.updatedGroupChatTopic = "Updated Chat Topic"

        # Initialize templates manually to match original structure exactly if factories behave differently
        self.newMessageTemplate = Message(
            id="new-message-id", content="This is a new message.", content_type="text",
            sender=MessageFrom(user_id="user-new-001", display_name="New User"),
            created_date_time="2024-01-02T10:00:00Z", reply_count=0
        )
        self.newMemberTemplate = Member(
            id="user-new-002", user_id="new-user-002", display_name="New Member",
            role="owner", email="newmember@example.com"
        )
        self.newChatTemplate = Chat(
            id="new-chat-001", type=ChatType.GROUP, is_hidden=False, topic="New Chat Topic"
        )

    # --- Helpers ---
    def _find_team(self, team_id: str) -> Optional[Team]:
        return next((t for t in self.teams if t.id == team_id), None)

    def _find_channel(self, team_id: str, channel_id: str) -> Optional[Channel]:
        return next((c for c in self.channels.get(team_id, []) if c.id == channel_id), None)

    # ==========================================
    #               TEAMS & GROUPS
    # ==========================================

    def get_myJoinedTeams_response(self) -> dict:
        return {
            "value": [
                {
                    "id": team.id,
                    "displayName": team.display_name,
                    "description": team.description,
                    "isArchived": team.is_archived,
                    "visibility": team.visibility,
                }
                for team in self.teams
            ],
        }

    def get_team_response(self, team_id: str) -> Optional[dict]:
        team = self._find_team(team_id)
        if not team:
            return None
        return {
            "id": team.id,
            "displayName": team.display_name,
            "description": team.description,
            "isArchived": team.is_archived,
            "visibility": team.visibility,
        }

    def get_updateTeam_response(self, team_id: str, update_json: dict) -> Optional[dict]:
        team = self._find_team(team_id)
        if not team:
            return None

        if "displayName" in update_json:
            team.display_name = update_json["displayName"]
        if "description" in update_json:
            team.description = update_json["description"]
        if "visibility" in update_json:
            team.visibility = update_json["visibility"]

        return {
            "id": team.id,
            "displayName": team.display_name,
            "description": team.description,
            "isArchived": team.is_archived,
            "visibility": team.visibility,
        }

    def get_createGroup_response(self, request_json: dict) -> dict:
        visibility = request_json.get("visibility", "").lower()
        if visibility not in ("private", "public"):
            visibility = "private"

        self.potentialTeams.append(
            Team(
                id=self.newGroupID,
                display_name=request_json.get("displayName"),
                description=request_json.get("description"),
                is_archived=False,
                visibility=visibility,
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
        team = next((t for t in self.potentialTeams if t.id == group_id), None)
        if not team:
            return {}

        self.teams.append(team)

        return {
            "id": team.id,
            "displayName": team.display_name,
            "description": team.description,
            "isArchived": team.is_archived,
            "visibility": team.visibility,
        }

    def get_createTeamFromTemplate_response(self, request: request.Request) -> Response:
        request_json = request.json
        new_team = Team(
            id=self.newTeamID,
            display_name=request_json.get("displayName"),
            description=request_json.get("description"),
            is_archived=False,
            visibility="private",
        )
        self.teams.append(new_team)

        # self.newTeamID == "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        op_id = "00000000-0000-0000-0000-000000000000"

        return Response(
            status= 202,
            headers= {
                "Location": f"/teams('{self.newTeamID}')/operations('{op_id}')",
                "Content-Location": f"/teams('{self.newTeamID}')",
                "Content-Type": "application/json",
                "Content-Length": "0"
            },
            response= ""
        )

    # def create_team_handler(self, req):
    #     result = self.get_createTeamFromTemplate_response(req.json)

    #     base_url = "https://graph.microsoft.com/v1.0"
    #     loc_header = f"/teams/{TEAM_ID}/operations/{OP_ID}"
    #     content_loc_header = f"/teams/{TEAM_ID}"

    #     return Response(
    #         response=result["body"],
    #         status=result["status"],
    #         headers={
    #             "Location": full_location,
    #             "Content-Location": full_content_loc,
    #             "Content-Type": result["headers"]["Content-Type"],
    #             "Content-Length": result["headers"]["Content-Length"]
    #         }
    #     )

    def get_archiveTeam_response(self, team_id: str) -> dict:
        team = self._find_team(team_id)
        if not team:
            return {"success": False}
        team.is_archived = True
        return {"success": True}

    def get_unarchiveTeam_response(self, team_id: str) -> dict:
        team = self._find_team(team_id)
        if not team:
            return {"success": False}
        team.is_archived = False
        return {"success": True}

    def get_deleteTeam_response(self, team_id: str) -> dict:
        team = self._find_team(team_id)
        if not team:
            return {"success": False}
        self.teams.remove(team)
        return {"success": True}

    def get_restoreTeam_response(self, team_id: str) -> dict:
        archived_team = next((t for t in self.teams if t.id == team_id and t.is_archived), None)
        if not archived_team:
            return {"success": False}

        archived_team.is_archived = False
        return {
            "id": archived_team.id,
            "displayName": archived_team.display_name,
            "description": archived_team.description,
            "isArchived": archived_team.is_archived,
            "visibility": archived_team.visibility,
            "mailNickname": self.newGroupMailNickname
        }

    # ==========================================
    #                 CHANNELS
    # ==========================================

    def get_listChannels_response(self, team_id: str) -> dict:
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#teams('{team_id}')/channels",
            "value": [
                {
                    ODATA_TYPE: "#microsoft.graph.channel",
                    "id": channel.id,
                    "displayName": channel.name,
                    "isGeneral": channel.is_general,
                    "membershipType": "standard",
                    "email": ""
                }
                for channel in self.channels.get(team_id, [])
            ],
        }

    def get_channel_response(self, team_id: str, channel_id: str) -> Optional[dict]:
        channel = self._find_channel(team_id, channel_id)
        if not channel:
            return None
        return {
            "id": channel.id,
            "displayName": channel.name,
            "isGeneral": channel.is_general,
        }

    def get_create_channel_response(self, team_id: str, request_json: dict) -> dict:
        display_name = request_json.get("displayName")
        description = request_json.get("description", display_name)

        new_channel = Channel(
            id=self.newChannelID,
            name=display_name,
            is_general=False,
        )

        if team_id not in self.channels:
            self.channels[team_id] = []
        self.channels[team_id].append(new_channel)

        return {
            "id": new_channel.id,
            "displayName": new_channel.name,
            "description": description,
            "isGeneral": new_channel.is_general,
            "membershipType": "standard"
        }

    def get_delete_channel_response(self, team_id: str, channel_id: str) -> dict:
        channel = self._find_channel(team_id, channel_id)
        if not channel:
            return {"success": False}
        self.channels[team_id].remove(channel)
        return {"success": True}

    # ==========================================
    #             MESSAGES (CHANNEL)
    # ==========================================

    def get_list_messages_response(self, team_id: str, channel_id: str) -> dict:
        return {
            "value": [
                {
                    "id": message.id,
                    "body": {
                        "content": message.content,
                        "contentType": message.content_type,
                    },
                    "from": {
                        "user": {
                            "id": message.sender.user_id,
                            "displayName": message.sender.display_name,
                        }
                    },
                    "createdDateTime": message.created_date_time,
                    "replies": [{"id": f"dummy-reply-{i}"} for i in range(message.reply_count)]
                }
                for message in self.messages.get(channel_id, [])
            ],
        }

    def get_message_response(self, team_id: str, channel_id: str, message_id: str) -> Optional[dict]:
        message = next((m for m in self.messages.get(channel_id, []) if m.id == message_id), None)
        if not message:
            return None

        return {
            "id": message.id,
            "body": {
                "content": message.content,
                "contentType": message.content_type,
            },
            "from": {
                "user": {
                    "id": message.sender.user_id,
                    "displayName": message.sender.display_name,
                }
            },
            "createdDateTime": message.created_date_time,
            "replies": [{"id": f"dummy-reply-{i}"} for i in range(message.reply_count)]
        }

    def get_send_message_response(self, team_id: str, channel_id: str, request_json: dict) -> dict:
        return {
            "id": self.newMessageTemplate.id,
            "body": {
                "content": request_json.get("body", {}).get("content"),
                "contentType": request_json.get("body", {}).get("contentType"),
            },
            "from": {
                "user": {
                    "id": self.newMessageTemplate.sender.user_id,
                    "displayName": self.newMessageTemplate.sender.display_name,
                }
            },
            "createdDateTime": self.newMessageTemplate.created_date_time,
        }

    def get_list_replies_response(self, team_id: str, channel_id: str, message_id: str) -> dict:
        return {
            "value": [
                {
                    "id": reply.id,
                    "body": {
                        "content": reply.content,
                        "contentType": reply.content_type,
                    },
                    "from": {
                        "user": {
                            "id": reply.sender.user_id,
                            "displayName": reply.sender.display_name,
                        }
                    },
                    "createdDateTime": reply.created_date_time,
                }
                for reply in self.replies.get(message_id, [])
            ],
        }

    def get_reply_response(self, team_id: str, channel_id: str, message_id: str, reply_id: str) -> Optional[dict]:
        reply = next((r for r in self.replies.get(message_id, []) if r.id == reply_id), None)
        if not reply:
            return None
        return {
            "id": reply.id,
            "body": {
                "content": reply.content,
                "contentType": reply.content_type,
            },
            "from": {
                "user": {
                    "id": reply.sender.user_id,
                    "displayName": reply.sender.display_name,
                }
            },
            "createdDateTime": reply.created_date_time,
        }

    # ==========================================
    #             MEMBERS (CHANNEL)
    # ==========================================

    def get_list_members_response(self, team_id: str, channel_id: str) -> dict:
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#teams('{team_id}')/channels('{channel_id}')/members",
            "value": [
                {
                    ODATA_TYPE: "#microsoft.graph.aadUserConversationMember",
                    "id": member.id,
                    "userId": member.user_id,
                    "displayName": member.display_name,
                    "roles": [member.role] if member.role == "owner" else [],
                    "email": member.email,
                }
                for member in self.members.get(team_id, {}).get(channel_id, [])
            ],
        }

    def get_add_member_response(self, team_id: str, request_json: dict) -> dict:
        roles = ["owner"] if self.newMemberTemplate.role == "owner" else []
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#teams('{team_id}')/members/$entity",
            ODATA_TYPE: "#microsoft.graph.aadUserConversationMember",
            "id": self.newMemberTemplate.id,
            "roles": roles,
            "displayName": self.newMemberTemplate.display_name,
            "userId": self.newMemberTemplate.user_id,
            "email": self.newMemberTemplate.email,
        }

    def get_update_member_role_response(self, team_id: str, channel_id: str, member_id: str, request_json: dict) -> Optional[dict]:
        channel_members = self.members.get(team_id, {}).get(channel_id, [])
        member = next((m for m in channel_members if m.id == member_id), None)
        if not member:
            return None

        if "roles" in request_json:
            member.role = "owner" if "owner" in request_json["roles"] else "member"

        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#teams('{team_id}')/channels('{channel_id}')/members/$entity",
            ODATA_TYPE: "#microsoft.graph.aadUserConversationMember",
            "id": member.id,
            "userId": member.user_id,
            "displayName": member.display_name,
            "roles": [member.role] if member.role == "owner" else [],
            "email": member.email,
        }

    def get_remove_member_response(self, team_id: str, channel_id: str, member_id: str) -> dict:
        channel_members = self.members.get(team_id, {}).get(channel_id, [])
        member = next((m for m in channel_members if m.id == member_id), None)
        if not member:
            return {"success": False}
        channel_members.remove(member)
        return {"success": True}

    # ==========================================
    #                 CHATS
    # ==========================================

    def get_list_chats_response(self, chat_type: ChatType) -> dict:
        chats = self.oneonone_chats if chat_type == ChatType.ONE_ON_ONE else self.group_chats
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#chats",
            ODATA_COUNT: len(chats),
            "value": [
                {
                    "id": chat.id,
                    "chatType": "oneOnOne" if chat.type == ChatType.ONE_ON_ONE else "group",
                    "isHiddenForAllMembers": chat.is_hidden,
                    "topic": chat.topic,
                }
                for chat in chats
            ],
        }

    def get_create_chat_response(self, request_json: dict) -> dict:
        is_one_on_one = request_json["chatType"] == "oneOnOne"
        response = {
            ODATA_CONTEXT: f"{GRAPH_URL}#chats/$entity",
            "id": self.newChatTemplate.id,
            "chatType": "oneOnOne" if is_one_on_one else "group",
            "isHiddenForAllMembers": self.newChatTemplate.is_hidden,
            "topic": None if is_one_on_one else self.newChatTemplate.topic,
        }
        return response

    def get_update_group_chat_topic_response(self, chat_id: str, request_json: dict) -> dict:
        chat = next((c for c in self.group_chats if c.id == chat_id), None)
        if not chat:
            return {}

        chat.topic = request_json.get("topic", chat.topic)
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#chats('{chat_id}')",
            "id": chat.id,
            "chatType": "group",
            "isHiddenForAllMembers": chat.is_hidden,
            "topic": chat.topic,
        }

    # ==========================================
    #           CHAT MEMBERS
    # ==========================================

    def get_list_group_chat_members_response(self, chat_id: str) -> dict:
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#chats('{chat_id}')/members",
            "value": [
                {
                    ODATA_TYPE: "#microsoft.graph.aadUserConversationMember",
                    "id": member.id,
                    "userId": member.user_id,
                    "displayName": member.display_name,
                    "roles": [member.role] if member.role == "owner" else [],
                    "email": member.email,
                }
                for member in self.group_chat_members.get(chat_id, [])
            ],
        }

    def get_add_member_to_group_chat_response(self, chat_id: str, request_json: dict) -> dict:
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#chats('{chat_id}')/members/$entity",
            ODATA_TYPE: "#microsoft.graph.aadUserConversationMember",
            "id": self.newMemberTemplate.id,
            "roles": [self.newMemberTemplate.role] if self.newMemberTemplate.role == "owner" else [],
            "displayName": self.newMemberTemplate.display_name,
            "userId": self.newMemberTemplate.user_id,
            "email": self.newMemberTemplate.email,
        }

    def get_remove_member_from_group_chat_response(self, chat_id: str, member_id: str) -> dict:
        return {"success": True}

    # ==========================================
    #           CHAT MESSAGES
    # ==========================================

    def get_list_messages_in_chat_response(self, chat_id: str) -> dict:
        return {
            "value": [
                {
                    "id": message.id,
                    "body": {
                        "content": message.content,
                        "contentType": message.content_type,
                    },
                    "from": {
                        "user": {
                            "id": message.sender.user_id,
                            "displayName": message.sender.display_name,
                        }
                    },
                    "createdDateTime": message.created_date_time,
                    "replies": [{"id": f"dummy-reply-{i}"} for i in range(message.reply_count)]
                }
                for message in self.chat_messages.get(chat_id, [])
            ],
        }

    def get_get_message_in_chat_response(self, chat_id: str, message_id: str) -> Optional[dict]:
        message = next((m for m in self.chat_messages.get(chat_id, []) if m.id == message_id), None)
        if not message:
            return None

        return {
            "id": message.id,
            "body": {
                "content": message.content,
                "contentType": message.content_type,
            },
            "from": {
                "user": {
                    "id": message.sender.user_id,
                    "displayName": message.sender.display_name,
                }
            },
            "createdDateTime": message.created_date_time,
            "replies": [{"id": f"dummy-reply-{i}"} for i in range(message.reply_count)]
        }

    def get_send_message_in_chat_response(self, chat_id: str, request_json: dict) -> dict:
        return {
            "id": self.newMessageTemplate.id,
            "body": {
                "content": request_json.get("body", {}).get("content"),
                "contentType": request_json.get("body", {}).get("contentType"),
            },
            "from": {
                "user": {
                    "id": self.newMessageTemplate.sender.user_id,
                    "displayName": self.newMessageTemplate.sender.display_name,
                }
            },
            "createdDateTime": self.newMessageTemplate.created_date_time,
        }

    def get_all_messeges_in_chats_response(self) -> dict:
        target_chat_id = self.group_chats[0].id
        return {
            ODATA_CONTEXT: f"{GRAPH_URL}#Collection(chatMessage)",
            ODATA_COUNT: len(self.chat_messages),
            "value": [
                {
                    ODATA_TYPE: "#microsoft.graph.chatMessage",
                    "id": message.id,
                    "etag": message.id,
                    "messageType": "message",
                    "chatId": target_chat_id,
                    "body": {
                        "content": message.content,
                        "contentType": message.content_type,
                    },
                    "from": {
                        "user": {
                            "id": message.sender.user_id,
                            "displayName": message.sender.display_name,
                        }
                    },
                    "createdDateTime": message.created_date_time,
                    "lastModifiedDateTime": message.created_date_time,
                }
                for message in self.chat_messages[target_chat_id]
            ],
        }

    def get_list_pinned_messages_in_chat_response(self, chat_id: str) -> dict:
        return {
            "value": [
                {
                    "id": message.id,
                    "message": {
                    "id": message.id,
                    "etag": message.id,
                    "messageType": "message",
                    "chatId": chat_id,
                    "body": {
                        "content": message.content,
                        "contentType": message.content_type,
                    },
                    "from": {
                        "user": {
                            "id": message.sender.user_id,
                            "displayName": message.sender.display_name,
                        }
                    },
                    "createdDateTime": message.created_date_time,
                    "lastModifiedDateTime": message.created_date_time,
                    }
                }
                for message in self.chat_messages.get(chat_id, [])
            ],
        }

    # ==========================================
    #                 USERS
    # ==========================================

    def get_me_response(self) -> dict:
        return {
            "id": self.me.id,
            "displayName": self.me.display_name,
            "email": self.me.email,
        }