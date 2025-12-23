from teams_lib_pzsp2_z1.client import TeamsClient
from tests.init_fake_client import init_fake_client
from tests.fake_server.setup import setup_fake_server


def test_list_my_teams_integration(httpserver):
    """
    Integration test: Python -> Go Binary -> Fake HTTP -> Python Mock Server
    """

    data = setup_fake_server(httpserver)

    # Init fake client
    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        teams = client.teams.list_my_joined()

        assert len(teams) == len(data.teams)

        assert teams[0].DisplayName == data.teams[0].DisplayName
        assert teams[0].ID == data.teams[0].ID
        assert teams[0].Description == data.teams[0].Description
        assert teams[0].IsArchived == data.teams[0].IsArchived
        assert teams[0].Visibility == data.teams[0].Visibility

        assert teams[1].DisplayName == data.teams[1].DisplayName
        assert teams[1].ID == data.teams[1].ID
        assert teams[1].Description == data.teams[1].Description
        assert teams[1].IsArchived == data.teams[1].IsArchived
        assert teams[1].Visibility == data.teams[1].Visibility

    finally:
        client.close()

def test_get_team_integration(httpserver):
    """
    Integration test: Python -> Go Binary -> Fake HTTP -> Python Mock Server
    """

    data = setup_fake_server(httpserver)

    # Init fake client
    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        team = client.teams.get(data.teams[0].DisplayName)

        print(data.get_team_response(data.teams[0].ID))

        assert team.DisplayName == data.teams[0].DisplayName
        assert team.ID == data.teams[0].ID
        assert team.Description == data.teams[0].Description
        assert team.IsArchived == data.teams[0].IsArchived
        assert team.Visibility == data.teams[0].Visibility

    finally:
        client.close()
