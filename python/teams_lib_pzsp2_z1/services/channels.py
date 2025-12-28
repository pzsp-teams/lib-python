from teams_lib_pzsp2_z1.model.channel import Channel
from teams_lib_pzsp2_z1.model.message import (
    Message,
    MessageBody,
    MessageContentType,
    MessageFrom,
)
from teams_lib_pzsp2_z1.services.base_service import BaseService


class ChannelsService(BaseService):
    def list_channels(self, teamRef: str) -> list[Channel]:
        response = self.client.execute(
            cmd_type="request",
            method="listChannels",
            params={
                "teamRef": teamRef,
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

    def get(self, teamRef: str, channelRef: str) -> Channel:
        response = self.client.execute(
            cmd_type="request",
            method="getChannel",
            params={
                "teamRef": teamRef,
                "channelRef": channelRef,
            },
        )

        return Channel(
            ID=response["ID"],
            Name=response["Name"],
            IsGeneral=(True if response["IsGeneral"] else False),
        )

    def create_standard(self, teamRef: str, display_name: str) -> Channel:
        response = self.client.execute(
            cmd_type="request",
            method="createStandardChannel",
            params={
                "teamRef": teamRef,
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
            teamRef: str,
            display_name: str,
            member_refs: list[str],
            owner_refs: list[str]
    ) -> Channel:
        response = self.client.execute(
            cmd_type="request",
            method="createPrivateChannel",
            params={
                "teamRef": teamRef,
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

    def delete(self, teamRef: str, channelRef: str) -> bool:
        response = self.client.execute(
            cmd_type="request",
            method="deleteChannel",
            params={
                "teamRef": teamRef,
                "channelRef": channelRef,
            },
        )
        return response == "deleted"

    def send_message(self, teamRef: str, channelRef: str, body: MessageBody) -> Message:
        response = self.client.execute(
            cmd_type="request",
            method="sendChannelMessage",
            params={
                "teamRef": teamRef,
                "channelRef": channelRef,
                "body": dict(body),
            },
        )

        return Message(
            ID=response["ID"],
            Content=response["Content"],
            ContentType=MessageContentType(response["ContentType"]),
            CreateDateTime=response["CreateDateTime"],
            From=MessageFrom(
                UserID=response["From"]["UserID"],
                DisplayName=response["From"]["DisplayName"],
            ),
            ReplyCount=response["ReplyCount"],
        )

    def list_messages_in_channel(
            self,
            teamRef: str,
            channelRef: str,
            top: int | None = 10,
            expand_replies: bool = False,
    ):
        response = self.client.execute(
            cmd_type="request",
            method="listChannelMessages",
            params={
                "teamRef": teamRef,
                "channelRef": channelRef,
                "options": {
                    "top": top,
                    "expandReplies": expand_replies,
                },
            },
        )

        return [
            Message(
                ID=message["ID"],
                Content=message["Content"],
                ContentType=MessageContentType(message["ContentType"]),
                CreateDateTime=message["CreateDateTime"],
                From=MessageFrom(
                    UserID=message["From"]["UserID"],
                    DisplayName=message["From"]["DisplayName"],
                ),
                ReplyCount=message["ReplyCount"],
            )
            for message in response
        ]

    def get_message(self, teamRef: str, channelRef: str, messageID: str) -> Message:
        response = self.client.execute(
            cmd_type="request",
            method="getChannelMessage",
            params={
                "teamRef": teamRef,
                "channelRef": channelRef,
                "messageID": messageID,
            },
        )

        return Message(
            ID=response["ID"],
            Content=response["Content"],
            ContentType=MessageContentType(response["ContentType"]),
            CreateDateTime=response["CreateDateTime"],
            From=MessageFrom(
                UserID=response["From"]["UserID"],
                DisplayName=response["From"]["DisplayName"],
            ),
            ReplyCount=response["ReplyCount"],
        )

    def list_message_replies(
            self,
            teamRef: str,
            channelRef: str,
            messageID: str,
            top: int | None = 10,
    ):
        response = self.client.execute(
            cmd_type="request",
            method="listChannelMessageReplies",
            params={
                "teamRef": teamRef,
                "channelRef": channelRef,
                "messageID": messageID,
                "top": top,
            },
        )

        return [
            Message(
                ID=message["ID"],
                Content=message["Content"],
                ContentType=MessageContentType(message["ContentType"]),
                CreateDateTime=message["CreateDateTime"],
                From=MessageFrom(
                    UserID=message["From"]["UserID"],
                    DisplayName=message["From"]["DisplayName"],
                ),
                ReplyCount=message["ReplyCount"],
            )
            for message in response
        ]

    def get_message_reply(
            self,
            teamRef: str,
            channelRef: str,
            messageID: str,
            replyID: str,
    ) -> Message:
        response = self.client.execute(
            cmd_type="request",
            method="getChannelMessageReply",
            params={
                "teamRef": teamRef,
                "channelRef": channelRef,
                "messageID": messageID,
                "replyID": replyID,
            },
        )

        return Message(
            ID=response["ID"],
            Content=response["Content"],
            ContentType=MessageContentType(response["ContentType"]),
            CreateDateTime=response["CreateDateTime"],
            From=MessageFrom(
                UserID=response["From"]["UserID"],
                DisplayName=response["From"]["DisplayName"],
            ),
            ReplyCount=response["ReplyCount"],
        )

    
