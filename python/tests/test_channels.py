from teams_lib_pzsp2_z1.client import TeamsClient
from tests.init_fake_client import init_fake_client
from tests.fake_server.setup import setup_fake_server


def test_list_channels_integration(httpserver):
    """
    Integration test: Python -> Go Binary -> Fake HTTP -> Python Mock Server
    """

    data = setup_fake_server(httpserver)

    # Init fake client
    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channels = client.channels.list_channels(data.teams[0].DisplayName)

        assert len(channels) == len(data.channels[data.teams[0].ID])

        assert channels[0].Name == data.channels[data.teams[0].ID][0].Name
        assert channels[0].ID == data.channels[data.teams[0].ID][0].ID
        assert channels[0].IsGeneral == data.channels[data.teams[0].ID][0].IsGeneral

        assert channels[1].Name == data.channels[data.teams[0].ID][1].Name
        assert channels[1].ID == data.channels[data.teams[0].ID][1].ID
        assert channels[1].IsGeneral == data.channels[data.teams[0].ID][1].IsGeneral

    finally:
        client.close()
