from typing import Any
from teams_lib_pzsp2_z1 import config
from teams_lib_pzsp2_z1.client import TeamsClient

def init_fake_client(client: TeamsClient, mock_server_url: str) -> Any:
    """
    Helper function to initialize the Go client in FAKE mode.
    It injects the mockServerUrl.
    """

    return client.execute(
        cmd_type="init",
        params={
            "mockServerUrl": mock_server_url,
        }
    )