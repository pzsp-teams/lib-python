from teams_lib_pzsp2_z1.model.team import MSTeamsUpdate
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

    data = setup_fake_server(httpserver)

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


def test_update_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        updated_description = "Updated team description"
        team = client.teams.update(
            teamRef=data.teams[0].DisplayName,
            update=MSTeamsUpdate(
                Description=updated_description,
            ),
        )

        assert team.DisplayName == data.teams[0].DisplayName
        assert team.ID == data.teams[0].ID
        assert team.Description == updated_description
        assert team.IsArchived == data.teams[0].IsArchived
        assert team.Visibility == data.teams[0].Visibility

    finally:
        client.close()


def test_create_team_via_group_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        team = client.teams.create_via_group(
            display_name=data.newTeamName,
            mail_nickname=data.newGroupMailNickname,
            visibility=data.newTeamVisibility,
        )

        assert team.ID == data.newGroupID
        assert team.DisplayName == data.newTeamName
        assert team.Visibility == data.newTeamVisibility

    finally:
        client.close()


def test_create_team_from_template_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        msg = client.teams.create_from_template(
            display_name=data.newTeamName,
            description="A team created from a template",
            owners=["user-123-abc"],
        )

        assert msg == "id will be given later (async)"

    finally:
        client.close()


def test_archive_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.teams.archive(
            teamRef=data.teams[0].DisplayName,
            spo_read_only_from_members=True,
        )

        assert success is True

    finally:
        client.close()


def test_unarchive_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.teams.unarchive(
            teamRef=data.teams[2].DisplayName,
        )

        assert success is True

    finally:
        client.close()


def test_delete_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.teams.delete(
            teamRef=data.teams[0].DisplayName,
        )

        assert success is True

    finally:
        client.close()


def test_restore_deleted_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        msg = client.teams.restore_deleted(
            deleted_team_ID=data.teams[2].ID,
        )

        assert msg == data.teams[2].ID

    finally:
        client.close()


def test_error_handling_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        try:
            client.teams.get("non-existent-team")
            assert False, "Expected an exception for non-existent team"
        except Exception as e:
            assert "Go Error" in str(e)

    finally:
        client.close()