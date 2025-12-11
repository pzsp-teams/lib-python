from teams_lib_pzsp2_z1.client import TeamsClient


def test_list_channels_integration(httpserver):
    """
    Integration test: Python -> Go Binary -> Fake HTTP -> Python Mock Server
    """
    # Fake server config
    fake_team_id = "team-123-abc"
    ms_graph_response = {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#teams('team-123-abc')/channels",
        "value": [
            {
                "id": "19:123123@thread.tacv2",
                "displayName": "General",
                "description": "General discussions",
            },
            {
                "id": "19:999999@thread.tacv2",
                "displayName": "Development",
                "description": "Coding stuff",
            },
        ],
    }
    httpserver.expect_request(
        f"/v1.0/teams/{fake_team_id}/channels", method="GET"
    ).respond_with_json(ms_graph_response)

    # Init fake client
    client = TeamsClient()
    client.init_fake_client(httpserver.url_for(""))

    channels = client.channels.list_channels(fake_team_id)

    assert len(channels) == 2

    first_channel = channels[0]

    assert first_channel["displayName"] == "General"
    assert first_channel["id"] == "19:123123@thread.tacv2"
