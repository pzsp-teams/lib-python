from teams_lib_pzsp2_z1.model.team import UpdateTeam
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

        assert teams[0].display_name == data.teams[0].display_name
        assert teams[0].id == data.teams[0].id
        assert teams[0].description == data.teams[0].description
        assert teams[0].is_archived == data.teams[0].is_archived
        assert teams[0].visibility == data.teams[0].visibility

        assert teams[1].display_name == data.teams[1].display_name
        assert teams[1].id == data.teams[1].id
        assert teams[1].description == data.teams[1].description
        assert teams[1].is_archived == data.teams[1].is_archived
        assert teams[1].visibility == data.teams[1].visibility

    finally:
        client.close()

def test_get_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        team = client.teams.get(data.teams[0].display_name)

        print(data.get_team_response(data.teams[0].id))

        assert team.display_name == data.teams[0].display_name
        assert team.id == data.teams[0].id
        assert team.description == data.teams[0].description
        assert team.is_archived == data.teams[0].is_archived
        assert team.visibility == data.teams[0].visibility

    finally:
        client.close()


def test_update_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        updated_description = "Updated team description"
        team = client.teams.update(
            team_ref=data.teams[0].display_name,
            update=UpdateTeam(
                description=updated_description,
            ),
        )

        assert team.display_name == data.teams[0].display_name
        assert team.id == data.teams[0].id
        assert team.description == updated_description
        assert team.is_archived == data.teams[0].is_archived
        assert team.visibility == data.teams[0].visibility

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

        assert team.id == data.newGroupID
        assert team.display_name == data.newTeamName
        assert team.visibility == data.newTeamVisibility

    finally:
        client.close()


def test_archive_team_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.teams.archive(
            team_ref=data.teams[0].display_name,
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
            team_ref=data.teams[2].display_name,
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
            team_ref=data.teams[0].display_name,
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
            deleted_team_ID=data.teams[2].id,
        )

        assert msg == data.teams[2].id

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