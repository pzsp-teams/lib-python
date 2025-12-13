from teams_lib_pzsp2_z1.model.channel import Channel
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
