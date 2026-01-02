from datetime import datetime

from teams_lib_pzsp2_z1.model.chat import Chat, ChatRef, ChatType
from teams_lib_pzsp2_z1.model.member import Member
from teams_lib_pzsp2_z1.model.mention import Mention
from teams_lib_pzsp2_z1.model.message import (
    Message,
    MessageBody,
    MessageContentType,
    MessageFrom,
)
from teams_lib_pzsp2_z1.services.base_service import BaseService


class ChatsService(BaseService):
    def create_one_on_one(self, recipient_ref: str) -> Chat:
        response = self.client.execute(
            cmd_type="request",
            method="createOneOnOneChat",
            params={
                "recipientRef": recipient_ref,
            },
        )

        return Chat(
            ID=response["ID"],
            Type=ChatType(response["Type"]),
            IsHidden=(True if response["IsHidden"] else False),
            Topic=response["Topic"],
        )

    def create_group_chat(
        self, recipient_refs: list[str], topic: str, include_me: bool
    ) -> Chat:
        response = self.client.execute(
            cmd_type="request",
            method="createGroupChat",
            params={
                "recipientRefs": recipient_refs,
                "topic": topic,
                "includeMe": include_me,
            },
        )

        return Chat(
            ID=response["ID"],
            Type=ChatType(response["Type"]),
            IsHidden=(True if response["IsHidden"] else False),
            Topic=response["Topic"],
        )

    def add_member_to_group_chat(self, group_chat_ref: str, user_ref: str) -> Member:
        member = self.client.execute(
            cmd_type="request",
            method="addMemberToGroupChat",
            params={
                "groupChatRef": group_chat_ref,
                "userRef": user_ref,
            },
        )

        return Member(
            ID=member["ID"],
            DisplayName=member["DisplayName"],
            UserID=member["UserID"],
            Role=member["Role"],
            Email=member["Email"],
        )

    def remove_member_from_group_chat(
        self, group_chat_ref: str, member_ref: str
    ) -> bool:
        result = self.client.execute(
            cmd_type="request",
            method="removeMemberFromGroupChat",
            params={
                "groupChatRef": group_chat_ref,
                "userRef": member_ref,
            },
        )

        return result == "removed"

    def list_group_chat_members(self, group_chat_ref: str) -> list[Member]:
        members = self.client.execute(
            cmd_type="request",
            method="listMembersInGroupChat",
            params={
                "groupChatRef": group_chat_ref,
            },
        )

        return [
            Member(
                ID=member["ID"],
                DisplayName=member["DisplayName"],
                UserID=member["UserID"],
                Role=member["Role"],
                Email=member["Email"],
            )
            for member in members
        ]

    def update_group_chat_topic(self, group_chat_ref: str, new_topic: str) -> Chat:
        response = self.client.execute(
            cmd_type="request",
            method="updateGroupChatTopic",
            params={
                "groupChatRef": group_chat_ref,
                "topic": new_topic,
            },
        )

        return Chat(
            ID=response["ID"],
            Type=ChatType(response["Type"]),
            IsHidden=(True if response["IsHidden"] else False),
            Topic=response["Topic"],
        )

    def list_messages(self, chat_ref: str) -> list[Message]:
        messages = self.client.execute(
            cmd_type="request",
            method="listMessagesInChat",
            params={
                "chatRef": chat_ref,
            },
        )

        return [
            Message(
                ID=message["ID"],
                Body=MessageBody(
                    Content=message["Body"]["Content"],
                    ContentType=MessageContentType(message["Body"]["ContentType"]),
                ),
                From=MessageFrom(
                    UserID=message["From"]["UserID"],
                    DisplayName=message["From"]["DisplayName"],
                ),
                CreatedDateTime=message["CreatedDateTime"],
            )
            for message in messages
        ]

    def send_message(self, chat_ref: ChatRef, body: MessageBody) -> Message:
        message = self.client.execute(
            cmd_type="request",
            method="sendMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.Ref,
                    "type": chat_ref.type.value,
                },
                "body": {
                    "content": body.Content,
                    "contentType": body.ContentType.value,
                },
            },
        )

        return Message(
            ID=message["ID"],
            Body=MessageBody(
                Content=message["Body"]["Content"],
                ContentType=MessageContentType(message["Body"]["ContentType"]),
            ),
            From=MessageFrom(
                UserID=message["From"]["UserID"],
                DisplayName=message["From"]["DisplayName"],
            ),
            CreatedDateTime=message["CreatedDateTime"],
        )

    def delete_message(self, chat_ref: ChatRef, message_id: str) -> bool:
        result = self.client.execute(
            cmd_type="request",
            method="deleteMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.Ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return result == "deleted"

    def get_message(self, chat_ref: ChatRef, message_id: str) -> Message:
        message = self.client.execute(
            cmd_type="request",
            method="getMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.Ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return Message(
            ID=message["ID"],
            Body=MessageBody(
                Content=message["Body"]["Content"],
                ContentType=MessageContentType(message["Body"]["ContentType"]),
            ),
            From=MessageFrom(
                UserID=message["From"]["UserID"],
                DisplayName=message["From"]["DisplayName"],
            ),
            CreatedDateTime=message["CreatedDateTime"],
        )

    def list_my_joined(self, chat_type: ChatType | None = None) -> list[Chat]:
        params = {}
        if chat_type:
            params["chatType"] = chat_type.value

        chats = self.client.execute(
            cmd_type="request",
            method="listMyChats",
            params=params,
        )

        return [
            Chat(
                ID=chat["ID"],
                Type=ChatType(chat["Type"]),
                IsHidden=(True if chat["IsHidden"] else False),
                Topic=chat["Topic"],
            )
            for chat in chats
        ]

    def list_all_messages(
        self, start_time: datetime, end_time: datetime, top: int
    ) -> list[Message]:
        messages = self.client.execute(
            cmd_type="request",
            method="listMyChatMessages",
            params={
                "startTime": start_time.isoformat(),
                "endTime": end_time.isoformat(),
                "top": top,
            },
        )

        return [
            Message(
                ID=message["ID"],
                Body=MessageBody(
                    Content=message["Body"]["Content"],
                    ContentType=MessageContentType(message["Body"]["ContentType"]),
                ),
                From=MessageFrom(
                    UserID=message["From"]["UserID"],
                    DisplayName=message["From"]["DisplayName"],
                ),
                CreatedDateTime=message["CreatedDateTime"],
            )
            for message in messages
        ]

    def list_pinned_messages(self, chat_ref: ChatRef) -> list[Message]:
        messages = self.client.execute(
            cmd_type="request",
            method="listPinnedMessagesInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.Ref,
                    "type": chat_ref.type.value,
                },
            },
        )

        return [
            Message(
                ID=message["ID"],
                Body=MessageBody(
                    Content=message["Body"]["Content"],
                    ContentType=MessageContentType(message["Body"]["ContentType"]),
                ),
                From=MessageFrom(
                    UserID=message["From"]["UserID"],
                    DisplayName=message["From"]["DisplayName"],
                ),
                CreatedDateTime=message["CreatedDateTime"],
            )
            for message in messages
        ]

    def pin_message(self, chat_ref: ChatRef, message_id: str) -> bool:
        result = self.client.execute(
            cmd_type="request",
            method="pinMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.Ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return result == "pinned"


    def unpin_message(self, chat_ref: ChatRef, message_id: str) -> bool:
        result = self.client.execute(
            cmd_type="request",
            method="unpinMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.Ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return result == "unpinned"

    def get_mentions(self, chat_ref: ChatRef, raw_mentions: list[str]) -> list[Mention]:
        mentions = self.client.execute(
            cmd_type="request",
            method="getMentionsInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.Ref,
                    "type": chat_ref.type.value,
                },
                "rawMentions": raw_mentions,
            },
        )

        return [
            Mention(
                ID=mention["ID"],
                Mentioned=mention["Mentioned"],
                MentionText=mention["MentionText"],
            )
            for mention in mentions
        ]
