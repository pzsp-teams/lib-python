from teams_lib_pzsp2_z1.client import TeamsClient
from tests.init_fake_client import init_fake_client


def test_list_channels_integration(httpserver):
    """
    Integration test: Python -> Go Binary -> Fake HTTP -> Python Mock Server
    """
    # Fake server config
    fake_team_name = "Test Team"
    fake_team_id = "team-123-abc"
    ms_graph_response_teams = {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#teams",
        "value": [
            {
                "id": fake_team_id,
                "displayName": fake_team_name,
                "description": "A team for testing",
            },
        ],
    }
    ms_graph_response_channels = {
        "@odata.context": f"https://graph.microsoft.com/v1.0/$metadata#teams('{fake_team_id}')/channels",
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
        "/v1.0/users/me-token-to-replace/joinedTeams", method="GET"
    ).respond_with_json(ms_graph_response_teams)
    httpserver.expect_request(
        f"/v1.0/teams/{fake_team_id}/channels", method="GET"
    ).respond_with_json(ms_graph_response_channels)

    # Init fake client
    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channels = client.channels.list_channels("Test Team")

        assert len(channels) == 2

        assert channels[0].Name == "General"
        assert channels[0].ID == "19:123123@thread.tacv2"
        assert channels[0].IsGeneral == True

        assert channels[1].Name == "Development"
        assert channels[1].ID == "19:999999@thread.tacv2"
        assert channels[1].IsGeneral == False

    finally:
        client.close()
