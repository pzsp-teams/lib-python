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
        channels_data = response.get("channels", [])
        return [
            Channel(
                ID=channel["id"],
                Name=channel["displayName"],
                IsGeneral=(channel["displayName"].lower() == "general"),
            )
            for channel in channels_data
        ]
