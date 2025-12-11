from typing import Any

from teams_lib_pzsp2_z1.services.base_service import BaseService


class ChannelsService(BaseService):
    def list_channels(self, teamRef: str) -> Any:
        return self.client.execute(
            cmd_type="request",
            method="listChannels",
            params={
                "teamRef": teamRef,
            },
        )
