"""
This module provides the ChannelsService class for managing Microsoft Teams channels.
"""

from teams_lib_pzsp2_z1.model.channel import Channel
from teams_lib_pzsp2_z1.model.member import Member
from teams_lib_pzsp2_z1.model.mention import Mention
from teams_lib_pzsp2_z1.model.message import (
    Message,
    MessageBody,
    MessageCollection,
    MessageContentType,
    MessageFrom,
)
from teams_lib_pzsp2_z1.services.base_service import BaseService


class ChannelsService(BaseService):
    """Service for managing Microsoft Teams channels via the Go backend.

    This class acts as a high-level Python wrapper. It delegates logical operations
    to the underlying Go library through the `self.client.execute` bridge.

    **Architecture & Caching:**
    The decision to use caching or direct API calls is handled internally by the
    compiled Go library, based on the configuration provided during Client initialization.
    This Python class provides a unified interface regardless of the underlying mode.

    **Concepts:**
    * **References**: Arguments like `team_ref` or `channel_ref` accept either UUIDs
        or Display Names. The Go backend resolves these automatically.
    * **Identity**: Users are identified by UUID or Email.
    """

    def list_channels(self, team_ref: str) -> list[Channel]:
        """Retrieves all channels associated with a specific team.

        Args:
            team_ref (str): The reference to the team (UUID or Display Name).
        Returns:
            List[Channel]: A list of channel objects found in the team.
        """
        response = self.client.execute(
            cmd_type="request",
            method="listChannels",
            params={
                "teamRef": team_ref,
            },
        )
        return [
            Channel(
                ID=channel["ID"],
                Name=channel["Name"],
                IsGeneral=(True if channel["IsGeneral"] else False),
            )
            for channel in response
        ]

    def get(self, team_ref: str, channel_ref: str) -> Channel:
        """Retrieves a specific channel by its reference within a team.

        Args:
            team_ref (str): The reference to the team (UUID or Display Name).
            channel_ref (str): The reference to the channel (ID or Display Name).

        Returns:
            Channel: The requested channel object.

        Raises:
            Exception: If the reference is ambiguous or not found (propagated from Go).
        """
        response = self.client.execute(
            cmd_type="request",
            method="getChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
            },
        )

        return Channel(
            ID=response["ID"],
            Name=response["Name"],
            IsGeneral=(True if response["IsGeneral"] else False),
        )

    def create_standard(self, team_ref: str, display_name: str) -> Channel:
        """Creates a standard (public) channel within a team.

        Args:
            team_ref (str): The reference to the team.
            display_name (str): The display name for the new channel.

        Returns:
            Channel: The newly created channel object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="createStandardChannel",
            params={
                "teamRef": team_ref,
                "name": display_name,
            },
        )

        return Channel(
            ID=response["ID"],
            Name=response["Name"],
            IsGeneral=(True if response["IsGeneral"] else False),
        )

    def create_private(
        self,
        team_ref: str,
        display_name: str,
        member_refs: list[str],
        owner_refs: list[str],
    ) -> Channel:
        """Creates a private channel restricted to specific members.

        Args:
            team_ref (str): The reference to the team.
            display_name (str): The display name for the new private channel.
            member_refs (list[str]): List of user references (IDs or emails) to add as members.
            owner_refs (list[str]): List of user references to add as owners.
                At least one owner is required.

        Returns:
            Channel: The newly created private channel object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="createPrivateChannel",
            params={
                "teamRef": team_ref,
                "name": display_name,
                "memberRefs": member_refs,
                "ownerRefs": owner_refs,
            },
        )

        return Channel(
            ID=response["ID"],
            Name=response["Name"],
            IsGeneral=(True if response["IsGeneral"] else False),
        )

    def delete(self, team_ref: str, channel_ref: str) -> bool:
        """Removes a channel from a team.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel to be deleted.

        Returns:
            bool: True if the operation was successful.
        """
        response = self.client.execute(
            cmd_type="request",
            method="deleteChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
            },
        )
        return response == "deleted"

    def send_message(
        self, team_ref: str, channel_ref: str, body: MessageBody
    ) -> Message:
        """Sends a new message to a channel.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            body (MessageBody): The message payload containing content, content type
                (Text/HTML), and optional mentions.

        Returns:
            Message: The created message object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="sendMessageToChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "body": dict(body),
            },
        )

        return Message(
            ID=response["ID"],
            Content=response["Content"],
            ContentType=MessageContentType(response["ContentType"]),
            CreatedDateTime=response["CreatedDateTime"],
            From=MessageFrom(
                UserID=response["From"]["UserID"],
                DisplayName=response["From"]["DisplayName"],
            ),
            ReplyCount=response["ReplyCount"],
        )

    def list_messages(  # noqa: PLR0913
        self,
        team_ref: str,
        channel_ref: str,
        top: int | None = 10,
        expand_replies: bool = False,
        include_system_messages: bool = False,
        next_link: str | None = None,
    ) -> MessageCollection:
        """Retrieves messages from a channel.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            top (Optional[int]): The maximum number of messages to retrieve. Defaults to 10.
            expand_replies (bool): If True, system fetches replies for each message. Defaults to False.
            include_system_messages (bool): If True, includes system-generated messages. Defaults to False.
            next_link (Optional[str]): A link for pagination to fetch the next set of messages.

        Returns:
            MessageCollection: An object containing the list of messages and a next link for pagination.
        """
        response = self.client.execute(
            cmd_type="request",
            method="listMessagesInChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "options": {
                    "top": top,
                    "expandReplies": expand_replies,
                    "includeSystem": include_system_messages,
                    "nextLink": next_link,
                },
            },
        )

        return MessageCollection(
            Messages=[
                Message(
                    ID=msg["ID"],
                    Content=msg["Content"],
                    ContentType=MessageContentType(msg["ContentType"]),
                    CreatedDateTime=msg["CreatedDateTime"],
                    From=MessageFrom(
                        UserID=msg["From"]["UserID"],
                        DisplayName=msg["From"]["DisplayName"],
                    ),
                    ReplyCount=msg["ReplyCount"],
                )
                for msg in response["Messages"]
            ],
            NextLink=response.get("NextLink"),
        )

    def get_message(self, team_ref: str, channel_ref: str, message_id: str) -> Message:
        """Retrieves a specific message by its ID.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            message_id (str): The unique identifier of the message.

        Returns:
            Message: The requested message object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="getMessageInChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "messageID": message_id,
            },
        )

        return Message(
            ID=response["ID"],
            Content=response["Content"],
            ContentType=MessageContentType(response["ContentType"]),
            CreatedDateTime=response["CreatedDateTime"],
            From=MessageFrom(
                UserID=response["From"]["UserID"],
                DisplayName=response["From"]["DisplayName"],
            ),
            ReplyCount=response["ReplyCount"],
        )

    def list_message_replies(  # noqa: PLR0913
        self,
        team_ref: str,
        channel_ref: str,
        message_id: str,
        top: int | None = 10,
        include_system_messages: bool = False,
        next_link: str | None = None,
    ) -> MessageCollection:
        """Retrieves all replies to a specific message thread.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            message_id (str): The ID of the parent message.
            top (Optional[int]): Max number of replies to fetch. Defaults to 10.
            include_system_messages (bool): If True, includes system-generated messages. Defaults to False.
            next_link (Optional[str]): A link for pagination to fetch the next set of replies.

        Returns:
            MessageCollection: An object containing the list of replies and a next link for pagination.
        """
        response = self.client.execute(
            cmd_type="request",
            method="listMessageRepliesInChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "messageID": message_id,
                "top": top,
                "includeSystem": include_system_messages,
                "nextLink": next_link,
            },
        )

        return MessageCollection(
            Messages=[
                Message(
                    ID=msg["ID"],
                    Content=msg["Content"],
                    ContentType=MessageContentType(msg["ContentType"]),
                    CreatedDateTime=msg["CreatedDateTime"],
                    From=MessageFrom(
                        UserID=msg["From"]["UserID"],
                        DisplayName=msg["From"]["DisplayName"],
                    ),
                    ReplyCount=msg["ReplyCount"],
                )
                for msg in response["Messages"]
            ],
            NextLink=response.get("NextLink"),
        )

    def get_message_reply(
        self,
        team_ref: str,
        channel_ref: str,
        message_id: str,
        reply_id: str,
    ) -> Message:
        """Retrieves a specific reply from a thread.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            message_id (str): The ID of the parent message.
            reply_id (str): The ID of the reply to retrieve.

        Returns:
            Message: The requested reply object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="getMessageReplyInChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "messageID": message_id,
                "replyID": reply_id,
            },
        )

        return Message(
            ID=response["ID"],
            Content=response["Content"],
            ContentType=MessageContentType(response["ContentType"]),
            CreatedDateTime=response["CreatedDateTime"],
            From=MessageFrom(
                UserID=response["From"]["UserID"],
                DisplayName=response["From"]["DisplayName"],
            ),
            ReplyCount=response["ReplyCount"],
        )

    def list_members(self, team_ref: str, channel_ref: str) -> list[Member]:
        """Lists all members of a channel.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.

        Returns:
            List[Member]: A list of channel members.
        """
        response = self.client.execute(
            cmd_type="request",
            method="listChannelMembers",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
            },
        )
        return [Member(**member) for member in response]

    def add_member(
        self, team_ref: str, channel_ref: str, user_ref: str, is_owner: bool
    ) -> Member:
        """Adds a user to a channel.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            user_ref (str): The user to add (User ID or Email).
            is_owner (bool): Whether to grant Owner privileges.

        Returns:
            Member: The newly added member object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="addMemberToChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "userRef": user_ref,
                "isOwner": is_owner,
            },
        )
        return Member(**response)

    def update_member_role(
        self, team_ref: str, channel_ref: str, user_ref: str, is_owner: bool
    ) -> Member:
        """Updates the role of an existing channel member.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            user_ref (str): The user reference (ID or Email).
            is_owner (bool): True for Owner role, False for Member role.

        Returns:
            Member: The updated member object.
        """
        response = self.client.execute(
            cmd_type="request",
            method="updateMemberRoleInChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "userRef": user_ref,
                "isOwner": is_owner,
            },
        )
        return Member(**response)

    def remove_member(self, team_ref: str, channel_ref: str, user_ref: str) -> bool:
        """Removes a user from a channel.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            user_ref (str): The user reference (ID or Email) to remove.

        Returns:
            bool: True if the operation was successful.
        """
        response = self.client.execute(
            cmd_type="request",
            method="removeMemberFromChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "userRef": user_ref,
            },
        )
        return response == "removed"

    def get_mentions(
        self, team_ref: str, channel_ref: str, raw_mentions: list[str]
    ) -> list[Mention]:
        """Resolves raw mention strings into formal Mention objects.

        This is used to construct the `mentions` field for messages before sending.

        Args:
            team_ref (str): The reference to the team.
            channel_ref (str): The reference to the channel.
            raw_mentions (List[str]): A list of raw strings to resolve.
                Supported formats:
                * **Email/User ID**: Resolves to a specific user.
                * **'channel'**: Mentions the current channel.
                * **'team'**: Mentions the parent team.

        Returns:
            List[Mention]: A list of resolved Mention objects ready for the API.
        """
        response = self.client.execute(
            cmd_type="request",
            method="getMentionsInChannel",
            params={
                "teamRef": team_ref,
                "channelRef": channel_ref,
                "rawMentions": raw_mentions,
            },
        )
        return [Mention(**mention) for mention in response]
