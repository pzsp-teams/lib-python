from teams_lib_pzsp2_z1.client import TeamsClient
from tests.init_fake_client import init_fake_client
from tests.fake_server.setup import setup_fake_server
from teams_lib_pzsp2_z1.model.message import MessageContentType


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


def test_get_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channel = client.channels.get(
            teamRef=data.teams[0].DisplayName,
            channelRef=data.channels[data.teams[0].ID][1].Name,
        )

        assert channel.Name == data.channels[data.teams[0].ID][1].Name
        assert channel.ID == data.channels[data.teams[0].ID][1].ID
        assert channel.IsGeneral == data.channels[data.teams[0].ID][1].IsGeneral

    finally:
        client.close()


def test_create_standard_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channel = client.channels.create_standard(
            teamRef=data.teams[0].DisplayName,
            display_name=data.newChannelName,
        )

        assert channel.Name == data.newChannelName
        assert channel.ID == data.newChannelID
        assert channel.IsGeneral is False

    finally:
        client.close()


def test_create_private_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channel = client.channels.create_private(
            teamRef=data.teams[0].DisplayName,
            display_name=data.newChannelName,
            member_refs=[],
            owner_refs=[],
        )

        assert channel.Name == data.newChannelName
        assert channel.ID == data.newChannelID
        assert channel.IsGeneral is False

    finally:
        client.close()


def test_delete_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.channels.delete(
            teamRef=data.teams[0].DisplayName,
            channelRef=data.channels[data.teams[0].ID][1].Name,
        )

        assert success is True

    finally:
        client.close()


def test_list_messages_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        messages = client.channels.list_messages(
            teamRef=data.teams[0].DisplayName,
            channelRef=data.channels[data.teams[0].ID][0].Name,
        )

        assert len(messages) == len(data.messages[data.channels[data.teams[0].ID][0].ID])
        assert messages[0].ID == data.messages[data.channels[data.teams[0].ID][0].ID][0].ID
        assert messages[0].Content == data.messages[data.channels[data.teams[0].ID][0].ID][0].Content
        assert messages[0].ContentType == MessageContentType(data.messages[data.channels[data.teams[0].ID][0].ID][0].ContentType)
        assert messages[0].From.UserID == data.messages[data.channels[data.teams[0].ID][0].ID][0].From.UserID
        assert messages[0].From.DisplayName == data.messages[data.channels[data.teams[0].ID][0].ID][0].From.DisplayName
        assert messages[0].ReplyCount == data.messages[data.channels[data.teams[0].ID][0].ID][0].ReplyCount
        assert messages[0].CreatedDateTime == data.messages[data.channels[data.teams[0].ID][0].ID][0].CreatedDateTime

        assert messages[1].ID == data.messages[data.channels[data.teams[0].ID][0].ID][1].ID
        assert messages[1].Content == data.messages[data.channels[data.teams[0].ID][0].ID][1].Content
        assert messages[1].ContentType == MessageContentType(data.messages[data.channels[data.teams[0].ID][0].ID][1].ContentType)
        assert messages[1].From.UserID == data.messages[data.channels[data.teams[0].ID][0].ID][1].From.UserID
        assert messages[1].From.DisplayName == data.messages[data.channels[data.teams[0].ID][0].ID][1].From.DisplayName
        assert messages[1].ReplyCount == data.messages[data.channels[data.teams[0].ID][0].ID][1].ReplyCount
        assert messages[1].CreatedDateTime == data.messages[data.channels[data.teams[0].ID][0].ID][1].CreatedDateTime

    finally:
        client.close()


def test_get_message_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        message = client.channels.get_message(
            teamRef=data.teams[0].DisplayName,
            channelRef=data.channels[data.teams[0].ID][0].Name,
            messageID=data.messages[data.channels[data.teams[0].ID][0].ID][0].ID,
        )

        assert message.ID == data.messages[data.channels[data.teams[0].ID][0].ID][0].ID
        assert message.Content == data.messages[data.channels[data.teams[0].ID][0].ID][0].Content
        assert message.ContentType == MessageContentType(data.messages[data.channels[data.teams[0].ID][0].ID][0].ContentType)
        assert message.From.UserID == data.messages[data.channels[data.teams[0].ID][0].ID][0].From.UserID
        assert message.From.DisplayName == data.messages[data.channels[data.teams[0].ID][0].ID][0].From.DisplayName
        assert message.ReplyCount == data.messages[data.channels[data.teams[0].ID][0].ID][0].ReplyCount
        assert message.CreatedDateTime == data.messages[data.channels[data.teams[0].ID][0].ID][0].CreatedDateTime

    finally:
        client.close()


