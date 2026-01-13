"""
This module contains the service for managing Microsoft Teams chats via the Go backend.
"""

from datetime import datetime

from teams_lib_pzsp2_z1.model.chat import Chat, ChatRef, ChatType
from teams_lib_pzsp2_z1.model.member import Member
from teams_lib_pzsp2_z1.model.mention import Mention
from teams_lib_pzsp2_z1.model.message import (
    Message,
    MessageBody,
    MessageCollection,
    MessageContentType,
    MessageFrom,
)
from teams_lib_pzsp2_z1.model.search import (
    SearchConfig,
    SearchMessagesOptions,
    SearchResult,
    SearchResults,
)
from teams_lib_pzsp2_z1.services.base_service import BaseService


class ChatsService(BaseService):
    """Service for managing Microsoft Teams chats via the Go backend.

    This class acts as a high-level wrapper, delegating operations to the
    underlying Go library. It handles One-on-One chats, Group chats, messages,
    and membership management.

    **Concepts:**
    * **Chat Types**: Chats are distinct entities, either **One-on-One** (between two users)
      or **Group** (multiple users, has a topic).
    * **References**:
        * `recipient_ref` / `user_ref`: Can be a User ID (UUID) or an Email.
        * `group_chat_ref`: Can be the Chat ID or the Group Topic (if unique).
        * `chat_ref` (Object): A specific model `ChatRef` containing the ID/Name and the `ChatType`.
    * **Permissions**: Some operations (like `list_all_messages`) require Application Permissions
      and will not work in Delegated (user context) mode.
    """

    def create_one_on_one(self, recipient_ref: str) -> Chat:
        """Creates a One-on-One chat with a specific user.

        The authenticated user is automatically added to the chat.

        Args:
            recipient_ref (str): The reference to the other user (User ID or Email).

        Returns:
            Chat: The created chat object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="createOneOnOneChat",
            params={
                "recipientRef": recipient_ref,
            },
        )

        return Chat(
            id=response["ID"],
            type=ChatType(response["Type"]),
            is_hidden=(True if response["IsHidden"] else False),
            topic=response["Topic"],
        )

    def create_group_chat(
        self, recipient_refs: list[str], topic: str, include_me: bool
    ) -> Chat:
        """Creates a Group Chat with multiple participants.

        Args:
            recipient_refs (list[str]): A list of user references (IDs or Emails) to include.
            topic (str): The subject/topic of the group chat.
            include_me (bool): If True, the authenticated user is added to the group.

        Returns:
            Chat: The created group chat object.
        """
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
            id=response["ID"],
            type=ChatType(response["Type"]),
            is_hidden=(True if response["IsHidden"] else False),
            topic=response["Topic"],
        )

    def get_chat(self, chat_ref: ChatRef) -> Chat:
        """
        Retrieves a chat by its reference.

        Args:
            chat_ref (ChatRef): The chat reference object containing the ID/Name and ChatType.

        Returns:
            Chat: The requested chat object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="getChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
            },
        )

        return Chat(
            id=response["ID"],
            type=ChatType(response["Type"]),
            is_hidden=(True if response["IsHidden"] else False),
            topic=response["Topic"],
        )

    def add_member_to_group_chat(self, group_chat_ref: str, user_ref: str) -> Member:
        """Adds a user to an existing Group Chat.

        Args:
            group_chat_ref (str): The reference to the group chat (ID or Topic).
            user_ref (str): The user to add (User ID or Email).

        Returns:
            Member: The newly added member details.
        """
        member = self.client.execute(
            cmd_type="request",
            method="addMemberToGroupChat",
            params={
                "groupChatRef": group_chat_ref,
                "userRef": user_ref,
            },
        )

        return Member(
            id=member["ID"],
            display_name=member["DisplayName"],
            user_id=member["UserID"],
            role=member["Role"],
            email=member["Email"],
        )

    def remove_member_from_group_chat(
        self, group_chat_ref: str, member_ref: str
    ) -> bool:
        """Removes a member from a Group Chat.

        Args:
            group_chat_ref (str): The reference to the group chat (ID or Topic).
            member_ref (str): The user reference to remove (User ID or Email).

        Returns:
            bool: True if the member was successfully removed.
        """
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
        """Lists all members of a Group Chat.

        Args:
            group_chat_ref (str): The reference to the group chat (ID or Topic).

        Returns:
            list[Member]: A list of members in the chat.
        """
        members = self.client.execute(
            cmd_type="request",
            method="listMembersInGroupChat",
            params={
                "groupChatRef": group_chat_ref,
            },
        )

        return [
            Member(
                id=member["ID"],
                display_name=member["DisplayName"],
                user_id=member["UserID"],
                role=member["Role"],
                email=member["Email"],
            )
            for member in members
        ]

    def update_group_chat_topic(self, group_chat_ref: str, new_topic: str) -> Chat:
        """Updates the topic of a Group Chat.

        Args:
            group_chat_ref (str): The reference to the group chat (ID or old Topic).
            new_topic (str): The new topic string.

        Returns:
            Chat: The updated chat object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="updateGroupChatTopic",
            params={
                "groupChatRef": group_chat_ref,
                "topic": new_topic,
            },
        )

        return Chat(
            id=response["ID"],
            type=ChatType(response["Type"]),
            is_hidden=(True if response["IsHidden"] else False),
            topic=response["Topic"],
        )

    def list_messages(
        self,
        chat_ref: ChatRef,
        include_system_messages: bool = False,
        next_link: str | None = None,
    ) -> list[Message]:
        """Retrieves messages from a specific chat.

        Args:
            chat_ref (ChatRef): The chat reference object containing the ID/Name and ChatType.
            include_system_messages (bool): If True, includes system-generated messages. Defaults to False.
            next_link (str | None): A link for pagination to fetch the next set of messages. Defaults to None.

        Returns:
            list[Message]: A list of messages from the chat history.
        """
        messages = self.client.execute(
            cmd_type="request",
            method="listMessagesInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "includeSystem": include_system_messages,
                "nextLink": next_link,
            },
        )

        return MessageCollection(
            messages=[
                Message(
                    id=msg["ID"],
                    content=msg["Content"],
                    content_type=MessageContentType(msg["ContentType"]),
                    created_date_time=msg["CreatedDateTime"],
                    sender=MessageFrom(
                        user_id=msg["From"]["UserID"],
                        display_name=msg["From"]["DisplayName"],
                    ),
                    reply_count=msg["ReplyCount"],
                )
                for msg in messages["Messages"]
            ],
            next_link=messages.get("NextLink"),
        )

    def send_message(self, chat_ref: ChatRef, body: MessageBody) -> Message:
        """Sends a message to a chat.

        Args:
            chat_ref (ChatRef): The chat reference object.
            body (MessageBody): The message payload (content, type, mentions).

        Returns:
            Message: The created message object.
        """
        message = self.client.execute(
            cmd_type="request",
            method="sendMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "body": {
                    "content": body.content,
                    "contentType": body.content_type.value,
                },
            },
        )

        return Message(
            id=message["ID"],
            content=message["Content"],
            content_type=MessageContentType(message["ContentType"]),
            sender=MessageFrom(
                user_id=message["From"]["UserID"],
                display_name=message["From"]["DisplayName"],
            ),
            created_date_time=message["CreatedDateTime"],
            reply_count=message["ReplyCount"],
        )

    def delete_message(self, chat_ref: ChatRef, message_id: str) -> bool:
        """Soft-deletes a message from a chat.

        This action is reversible via the Graph API (though not exposed here).

        Args:
            chat_ref (ChatRef): The chat reference object.
            message_id (str): The unique identifier of the message to delete.

        Returns:
            bool: True if the message was successfully deleted.
        """
        result = self.client.execute(
            cmd_type="request",
            method="deleteMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return result == "deleted"

    def get_message(self, chat_ref: ChatRef, message_id: str) -> Message:
        """Retrieves a single message by its ID.

        Args:
            chat_ref (ChatRef): The chat reference object.
            message_id (str): The unique identifier of the message.

        Returns:
            Message: The requested message object.
        """
        message = self.client.execute(
            cmd_type="request",
            method="getMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return Message(
            id=message["ID"],
            content=message["Content"],
            content_type=MessageContentType(message["ContentType"]),
            sender=MessageFrom(
                user_id=message["From"]["UserID"],
                display_name=message["From"]["DisplayName"],
            ),
            created_date_time=message["CreatedDateTime"],
            reply_count=message["ReplyCount"],
        )

    def list_my_joined(self, chat_type: ChatType | None = None) -> list[Chat]:
        """Lists all chats the authenticated user is part of.

        Args:
            chat_type (ChatType | None, optional): Filter by chat type (e.g., only OneOnOne).
                Defaults to None (return all).

        Returns:
            list[Chat]: A list of chat objects.
        """
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
                id=chat["ID"],
                type=ChatType(chat["Type"]),
                is_hidden=(True if chat["IsHidden"] else False),
                topic=chat["Topic"],
            )
            for chat in chats
        ]

    def list_all_messages(
        self, start_time: datetime, end_time: datetime, top: int
    ) -> list[Message]:
        """Retrieves messages across ALL chats within a time range.

        Note:
            This operation typically requires **Application Permissions** and may not
            work with standard Delegated (User) credentials depending on the organization's policy.

        Args:
            start_time (datetime): The start of the time range.
            end_time (datetime): The end of the time range.
            top (int): Maximum number of messages to retrieve.

        Returns:
            list[Message]: A list of messages from all chats.
        """
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
                id=message["ID"],
                content=message["Content"],
                content_type=MessageContentType(message["ContentType"]),
                sender=MessageFrom(
                    user_id=message["From"]["UserID"],
                    display_name=message["From"]["DisplayName"],
                ),
                created_date_time=message["CreatedDateTime"],
                reply_count=message["ReplyCount"],
            )
            for message in messages
        ]

    def list_pinned_messages(self, chat_ref: ChatRef) -> list[Message]:
        """Lists all pinned messages in a specific chat.

        Args:
            chat_ref (ChatRef): The chat reference object.

        Returns:
            list[Message]: A list of pinned messages.
        """
        messages = self.client.execute(
            cmd_type="request",
            method="listPinnedMessagesInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
            },
        )

        return [
            Message(
                id=message["ID"],
                content=message["Content"],
                content_type=MessageContentType(message["ContentType"]),
                sender=MessageFrom(
                    user_id=message["From"]["UserID"],
                    display_name=message["From"]["DisplayName"],
                ),
                created_date_time=message["CreatedDateTime"],
                reply_count=message["ReplyCount"],
            )
            for message in messages
        ]

    def pin_message(self, chat_ref: ChatRef, message_id: str) -> bool:
        """Pins a message in the chat.

        Args:
            chat_ref (ChatRef): The chat reference object.
            message_id (str): The ID of the message to pin.

        Returns:
            bool: True if the message was successfully pinned.
        """
        result = self.client.execute(
            cmd_type="request",
            method="pinMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return result == "pinned"

    def unpin_message(self, chat_ref: ChatRef, message_id: str) -> bool:
        """Unpins a message in the chat.

        Args:
            chat_ref (ChatRef): The chat reference object.
            message_id (str): The ID of the message to unpin.

        Returns:
            bool: True if the message was successfully unpinned.
        """
        result = self.client.execute(
            cmd_type="request",
            method="unpinMessageInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "messageID": message_id,
            },
        )

        return result == "unpinned"

    def get_mentions(self, chat_ref: ChatRef, raw_mentions: list[str]) -> list[Mention]:
        """Resolves raw mention strings into formal Mention objects.

        This helps in processing @mentions within message content before sending.

        Args:
            chat_ref (ChatRef): The chat reference object.
            raw_mentions (list[str]): A list of raw strings to resolve.
                Supported formats:
                * **Email/User ID**: Resolves to a specific user.
                * **'Everyone'**: Mentions all members (Group Chats only).

        Returns:
            list[Mention]: A list of resolved Mention objects.
        """
        mentions = self.client.execute(
            cmd_type="request",
            method="getMentionsInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "rawMentions": raw_mentions,
            },
        )

        return [
            Mention(
                kind=mention["Kind"],
                at_id=mention["AtID"],
                text=mention["Text"],
                target_id=mention["TargetID"],
            )
            for mention in mentions
        ]

    def search_messages(self, chat_ref: ChatRef, options: SearchMessagesOptions, config: SearchConfig) -> SearchResults:
        """Searches for messages in a chat based on various criteria.

        Args:
            chat_ref (ChatRef): The chat reference object.
            options (SearchMessagesOptions): The search options and filters.
            config (SearchConfig): Configuration for the search operation.

        Returns:
            SearchResults: The results of the search operation.
        """
        response = self.client.execute(
            cmd_type="request",
            method="searchMessagesInChat",
            params={
                "chatRef": {
                    "ref": chat_ref.ref,
                    "type": chat_ref.type.value,
                },
                "searchMessagesOptions": options.__dict__(),
                "searchConfig": config.__dict__(),
            },
        )

        return SearchResults(
            messages=[
                SearchResult(
                    message=Message(
                        id=msg["Message"]["ID"],
                        content=msg["Message"]["Content"],
                        content_type=MessageContentType(msg["Message"]["ContentType"]),
                        created_date_time=msg["Message"]["CreatedDateTime"],
                        sender=MessageFrom(
                            user_id=msg["Message"]["From"]["UserID"],
                            display_name=msg["Message"]["From"]["DisplayName"],
                        ),
                        reply_count=msg["Message"]["ReplyCount"],
                    ),
                    channel_id=msg.get("ChannelID"),
                    team_id=msg.get("TeamID"),
                    chat_id=msg.get("ChatID"),
                )
                for msg in response["Messages"]
            ] if response.get("Messages") else [],
            next_from=response.get("NextFrom"),
        )
