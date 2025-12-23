from tests.fake_server.data import FakeServerData

def setup_fake_server(httpserver) -> FakeServerData:
    """
    Sets up a fake HTTP server to simulate Microsoft Graph API responses.
    """

    data = FakeServerData()

    httpserver.expect_request(
        "/v1.0/users/me-token-to-replace/joinedTeams", method="GET"
    ).respond_with_json(data.get_myJoinedTeams_response())

    httpserver.expect_request(
        f"/v1.0/teams/{data.teams[0].ID}/channels", method="GET"
    ).respond_with_json(data.get_listChannels_response(data.teams[0].ID))

    httpserver.expect_request(
        f"/v1.0/teams/{data.teams[1].ID}/channels", method="GET"
    ).respond_with_json(data.get_listChannels_response(data.teams[1].ID))

    httpserver.expect_request(
        f"/v1.0/teams/{data.teams[0].ID}", method="GET"
    ).respond_with_json(data.get_team_response(data.teams[0].ID))

    httpserver.expect_request(
        f"/v1.0/teams/{data.teams[1].ID}", method="GET"
    ).respond_with_json(data.get_team_response(data.teams[1].ID))

    return data

