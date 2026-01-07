from teams_lib_pzsp2_z1.client import TeamsClient
from tests.init_fake_client import init_fake_client
from tests.fake_server.setup import setup_fake_server
from teams_lib_pzsp2_z1.model.message import MessageContentType, MessageBody
from teams_lib_pzsp2_z1.model.mention import MentionKind


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
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][1].Name,
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
            team_ref=data.teams[0].DisplayName,
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
            team_ref=data.teams[0].DisplayName,
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
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][1].Name,
        )

        assert success is True

    finally:
        client.close()


def test_send_message_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        message = client.channels.send_message(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
            body=MessageBody(
                Content=data.newMessageTemplate.Content,
                ContentType=MessageContentType.TEXT,
                Mentions=[],
            )
        )

        assert message.ID == data.newMessageTemplate.ID
        assert message.Content == data.newMessageTemplate.Content
        assert message.ContentType == MessageContentType(data.newMessageTemplate.ContentType)
        assert message.From.UserID == data.newMessageTemplate.From.UserID
        assert message.From.DisplayName == data.newMessageTemplate.From.DisplayName
        assert message.ReplyCount == data.newMessageTemplate.ReplyCount
        assert message.CreatedDateTime == data.newMessageTemplate.CreatedDateTime

    finally:
        client.close()


def test_list_messages_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        collection = client.channels.list_messages(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
        )

        assert len(collection.Messages) == len(data.messages[data.channels[data.teams[0].ID][0].ID])
        assert collection.Messages[0].ID == data.messages[data.channels[data.teams[0].ID][0].ID][0].ID
        assert collection.Messages[0].Content == data.messages[data.channels[data.teams[0].ID][0].ID][0].Content
        assert collection.Messages[0].ContentType == MessageContentType(data.messages[data.channels[data.teams[0].ID][0].ID][0].ContentType)
        assert collection.Messages[0].From.UserID == data.messages[data.channels[data.teams[0].ID][0].ID][0].From.UserID
        assert collection.Messages[0].From.DisplayName == data.messages[data.channels[data.teams[0].ID][0].ID][0].From.DisplayName
        assert collection.Messages[0].ReplyCount == data.messages[data.channels[data.teams[0].ID][0].ID][0].ReplyCount
        assert collection.Messages[0].CreatedDateTime == data.messages[data.channels[data.teams[0].ID][0].ID][0].CreatedDateTime

        assert collection.Messages[1].ID == data.messages[data.channels[data.teams[0].ID][0].ID][1].ID
        assert collection.Messages[1].Content == data.messages[data.channels[data.teams[0].ID][0].ID][1].Content
        assert collection.Messages[1].ContentType == MessageContentType(data.messages[data.channels[data.teams[0].ID][0].ID][1].ContentType)
        assert collection.Messages[1].From.UserID == data.messages[data.channels[data.teams[0].ID][0].ID][1].From.UserID
        assert collection.Messages[1].From.DisplayName == data.messages[data.channels[data.teams[0].ID][0].ID][1].From.DisplayName
        assert collection.Messages[1].ReplyCount == data.messages[data.channels[data.teams[0].ID][0].ID][1].ReplyCount
        assert collection.Messages[1].CreatedDateTime == data.messages[data.channels[data.teams[0].ID][0].ID][1].CreatedDateTime
    finally:
        client.close()


def test_get_message_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        message = client.channels.get_message(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
            message_id=data.messages[data.channels[data.teams[0].ID][0].ID][0].ID,
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


def test_list_replies_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        replies = client.channels.list_message_replies(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
            message_id=data.messages[data.channels[data.teams[0].ID][0].ID][1].ID,
        )

        assert len(replies.Messages) == len(data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID])
        assert replies.Messages[0].ID == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].ID
        assert replies.Messages[0].Content == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].Content
        assert replies.Messages[0].ContentType == MessageContentType(data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].ContentType)
        assert replies.Messages[0].From.UserID == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].From.UserID
        assert replies.Messages[0].From.DisplayName == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].From.DisplayName
        assert replies.Messages[0].CreatedDateTime == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].CreatedDateTime

        assert replies.Messages[1].ID == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][1].ID
        assert replies.Messages[1].Content == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][1].Content
        assert replies.Messages[1].ContentType == MessageContentType(data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][1].ContentType)
        assert replies.Messages[1].From.UserID == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][1].From.UserID
        assert replies.Messages[1].From.DisplayName == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][1].From.DisplayName
        assert replies.Messages[1].CreatedDateTime == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][1].CreatedDateTime

    finally:
        client.close()


def test_get_reply_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        reply = client.channels.get_message_reply(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
            message_id=data.messages[data.channels[data.teams[0].ID][0].ID][1].ID,
            reply_id=data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].ID,
        )

        assert reply.ID == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].ID
        assert reply.Content == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].Content
        assert reply.ContentType == MessageContentType(data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].ContentType)
        assert reply.From.UserID == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].From.UserID
        assert reply.From.DisplayName == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].From.DisplayName
        assert reply.CreatedDateTime == data.replies[data.messages[data.channels[data.teams[0].ID][0].ID][1].ID][0].CreatedDateTime

    finally:
        client.close()


def test_list_members_integration(httpserver):
    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        team_id = data.teams[0].ID
        channel = data.channels[team_id][0]
        channel_id = channel.ID

        members = client.channels.list_members(
            team_ref=data.teams[0].DisplayName,
            channel_ref=channel.Name,
        )

        expected_members = data.members[team_id][channel_id]

        assert len(members) == len(expected_members)

        assert members[0].UserID == expected_members[0].UserID
        assert members[0].DisplayName == expected_members[0].DisplayName
        expected_role_0 = "owner" if expected_members[0].Role == "owner" else ""
        assert members[0].Role == expected_role_0
        assert members[0].Email == expected_members[0].Email
        assert members[0].ID == expected_members[0].ID

        assert members[1].UserID == expected_members[1].UserID
        assert members[1].DisplayName == expected_members[1].DisplayName
        expected_role_1 = "owner" if expected_members[1].Role == "owner" else ""
        assert members[1].Role == expected_role_1
        assert members[1].Email == expected_members[1].Email
        assert members[1].ID == expected_members[1].ID

    finally:
        client.close()


def test_add_member_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        member = client.channels.add_member(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][1].Name,
            user_ref=data.newMemberTemplate.DisplayName,
            is_owner=True if data.newMemberTemplate.Role == "owner" else False,
        )

        assert member.UserID == data.newMemberTemplate.UserID
        assert member.DisplayName == data.newMemberTemplate.DisplayName
        assert member.Role == data.newMemberTemplate.Role
        assert member.Email == data.newMemberTemplate.Email
        assert member.ID == data.newMemberTemplate.ID

    finally:
        client.close()


def test_update_member_role_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        member = client.channels.update_member_role(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
            user_ref=data.members[data.teams[0].ID][data.channels[data.teams[0].ID][0].ID][1].Email,
            is_owner=True
        )

        assert member.UserID == data.members[data.teams[0].ID][data.channels[data.teams[0].ID][0].ID][1].UserID
        assert member.DisplayName == data.members[data.teams[0].ID][data.channels[data.teams[0].ID][0].ID][1].DisplayName
        assert member.Role == "owner"
        assert member.Email == data.members[data.teams[0].ID][data.channels[data.teams[0].ID][0].ID][1].Email
        assert member.ID == data.members[data.teams[0].ID][data.channels[data.teams[0].ID][0].ID][1].ID
    finally:
        client.close()


def test_remove_member_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.channels.remove_member(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
            user_ref=data.members[data.teams[0].ID][data.channels[data.teams[0].ID][0].ID][1].Email,
        )

        assert success is True

    finally:
        client.close()

def test_get_mention_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        mention = client.channels.get_mentions(
            team_ref=data.teams[0].DisplayName,
            channel_ref=data.channels[data.teams[0].ID][0].Name,
            raw_mentions=MentionKind.TEAM.value,
        )

        assert mention[0].Kind == MentionKind.TEAM.value
        assert mention[0].AtID == 0
        assert mention[0].Text == data.teams[0].DisplayName
        assert mention[0].TargetID == data.teams[0].ID

    finally:
        client.close()





