from teams_lib_pzsp2_z1.model.chat import Chat, ChatType
from teams_lib_pzsp2_z1.model.member import Member
from teams_lib_pzsp2_z1.model.message import (
    Message,
    MessageBody,
    MessageContentType,
    MessageFrom,
)
from teams_lib_pzsp2_z1.services.base_service import BaseService


class ChatsService(BaseService):
    def list_my_joined(self) -> list[Chat]:
        response = self.client.execute(
            cmd_type="request",
            method="listMyJoinedChats",
            params={},
        )
        return [
            Chat(
                ID=chat["ID"],
                Type=ChatType(chat["Type"]),
                IsHidden=(True if chat["IsHidden"] else False),
                Topic=chat["Topic"],
            )
            for chat in response
        ]

    def create_one_on_one(self, user_id: str) -> Chat:
        response = self.client.execute(
            cmd_type="request",
            method="createOneOnOneChat",
            params={
                "userID": user_id,
            },
        )

        return Chat(
            ID=response["ID"],
            Type=ChatType(response["Type"]),
            IsHidden=(True if response["IsHidden"] else False),
            Topic=response["Topic"],
        )