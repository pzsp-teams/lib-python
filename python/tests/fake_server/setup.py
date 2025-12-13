from tests.fake_server.data import FakeServerData

def setup_fake_server(httpserver) -> FakeServerData:
    """
    Sets up a fake HTTP server to simulate Microsoft Graph API responses.
    """

    data = FakeServerData()

    # Mock response for listing joined teams
    httpserver.expect_request(
        "/v1.0/users/me-token-to-replace/joinedTeams", method="GET"
    ).respond_with_json(data.get_myJoinedTeams_response())

    # Mock response for listing channels in the fake team
    httpserver.expect_request(
        f"/v1.0/teams/{data.teams[0].ID}/channels", method="GET"
    ).respond_with_json(data.get_listChannels_response(data.teams[0].ID))

    return data

