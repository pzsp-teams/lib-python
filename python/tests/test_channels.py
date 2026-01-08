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

        channels = client.channels.list_channels(data.teams[0].display_name)

        assert len(channels) == len(data.channels[data.teams[0].id])

        assert channels[0].name == data.channels[data.teams[0].id][0].name
        assert channels[0].id == data.channels[data.teams[0].id][0].id
        assert channels[0].is_general == data.channels[data.teams[0].id][0].is_general

        assert channels[1].name == data.channels[data.teams[0].id][1].name
        assert channels[1].id == data.channels[data.teams[0].id][1].id
        assert channels[1].is_general == data.channels[data.teams[0].id][1].is_general

    finally:
        client.close()


def test_get_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channel = client.channels.get(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][1].name,
        )

        assert channel.name == data.channels[data.teams[0].id][1].name
        assert channel.id == data.channels[data.teams[0].id][1].id
        assert channel.is_general == data.channels[data.teams[0].id][1].is_general

    finally:
        client.close()


def test_create_standard_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channel = client.channels.create_standard(
            team_ref=data.teams[0].display_name,
            display_name=data.newChannelName,
        )

        assert channel.name == data.newChannelName
        assert channel.id == data.newChannelID
        assert channel.is_general is False

    finally:
        client.close()


def test_create_private_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        channel = client.channels.create_private(
            team_ref=data.teams[0].display_name,
            display_name=data.newChannelName,
            member_refs=[],
            owner_refs=[],
        )

        assert channel.name == data.newChannelName
        assert channel.id == data.newChannelID
        assert channel.is_general is False

    finally:
        client.close()


def test_delete_channel_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.channels.delete(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][1].name,
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
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
            body=MessageBody(
                content=data.newMessageTemplate.content,
                content_type=MessageContentType.TEXT,
                mentions=[],
            )
        )

        assert message.id == data.newMessageTemplate.id
        assert message.content == data.newMessageTemplate.content
        assert message.content_type == MessageContentType(data.newMessageTemplate.content_type)
        assert message.sender.user_id == data.newMessageTemplate.sender.user_id
        assert message.sender.display_name == data.newMessageTemplate.sender.display_name
        assert message.reply_count == data.newMessageTemplate.reply_count
        assert message.created_date_time == data.newMessageTemplate.created_date_time

    finally:
        client.close()


def test_list_messages_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        collection = client.channels.list_messages(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
        )

        assert len(collection.messages) == len(data.messages[data.channels[data.teams[0].id][0].id])
        assert collection.messages[0].id == data.messages[data.channels[data.teams[0].id][0].id][0].id
        assert collection.messages[0].content == data.messages[data.channels[data.teams[0].id][0].id][0].content
        assert collection.messages[0].content_type == MessageContentType(data.messages[data.channels[data.teams[0].id][0].id][0].content_type)
        assert collection.messages[0].sender.user_id == data.messages[data.channels[data.teams[0].id][0].id][0].sender.user_id
        assert collection.messages[0].sender.display_name == data.messages[data.channels[data.teams[0].id][0].id][0].sender.display_name
        assert collection.messages[0].reply_count == data.messages[data.channels[data.teams[0].id][0].id][0].reply_count
        assert collection.messages[0].created_date_time == data.messages[data.channels[data.teams[0].id][0].id][0].created_date_time

        assert collection.messages[1].id == data.messages[data.channels[data.teams[0].id][0].id][1].id
        assert collection.messages[1].content == data.messages[data.channels[data.teams[0].id][0].id][1].content
        assert collection.messages[1].content_type == MessageContentType(data.messages[data.channels[data.teams[0].id][0].id][1].content_type)
        assert collection.messages[1].sender.user_id == data.messages[data.channels[data.teams[0].id][0].id][1].sender.user_id
        assert collection.messages[1].sender.display_name == data.messages[data.channels[data.teams[0].id][0].id][1].sender.display_name
        assert collection.messages[1].reply_count == data.messages[data.channels[data.teams[0].id][0].id][1].reply_count
        assert collection.messages[1].created_date_time == data.messages[data.channels[data.teams[0].id][0].id][1].created_date_time
    finally:
        client.close()


def test_get_message_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        message = client.channels.get_message(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
            message_id=data.messages[data.channels[data.teams[0].id][0].id][0].id,
        )

        assert message.id == data.messages[data.channels[data.teams[0].id][0].id][0].id
        assert message.content == data.messages[data.channels[data.teams[0].id][0].id][0].content
        assert message.content_type == MessageContentType(data.messages[data.channels[data.teams[0].id][0].id][0].content_type)
        assert message.sender.user_id == data.messages[data.channels[data.teams[0].id][0].id][0].sender.user_id
        assert message.sender.display_name == data.messages[data.channels[data.teams[0].id][0].id][0].sender.display_name
        assert message.reply_count == data.messages[data.channels[data.teams[0].id][0].id][0].reply_count
        assert message.created_date_time == data.messages[data.channels[data.teams[0].id][0].id][0].created_date_time

    finally:
        client.close()


def test_list_replies_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        replies = client.channels.list_message_replies(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
            message_id=data.messages[data.channels[data.teams[0].id][0].id][1].id,
        )

        assert len(replies.messages) == len(data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id])
        assert replies.messages[0].id == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].id
        assert replies.messages[0].content == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].content
        assert replies.messages[0].content_type == MessageContentType(data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].content_type)
        assert replies.messages[0].sender.user_id == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].sender.user_id
        assert replies.messages[0].sender.display_name == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].sender.display_name
        assert replies.messages[0].created_date_time == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].created_date_time

        assert replies.messages[1].id == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][1].id
        assert replies.messages[1].content == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][1].content
        assert replies.messages[1].content_type == MessageContentType(data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][1].content_type)
        assert replies.messages[1].sender.user_id == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][1].sender.user_id
        assert replies.messages[1].sender.display_name == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][1].sender.display_name
        assert replies.messages[1].created_date_time == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][1].created_date_time

    finally:
        client.close()


def test_get_reply_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        reply = client.channels.get_message_reply(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
            message_id=data.messages[data.channels[data.teams[0].id][0].id][1].id,
            reply_id=data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].id,
        )

        assert reply.id == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].id
        assert reply.content == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].content
        assert reply.content_type == MessageContentType(data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].content_type)
        assert reply.sender.user_id == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].sender.user_id
        assert reply.sender.display_name == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].sender.display_name
        assert reply.created_date_time == data.replies[data.messages[data.channels[data.teams[0].id][0].id][1].id][0].created_date_time

    finally:
        client.close()


def test_list_members_integration(httpserver):
    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        team_id = data.teams[0].id
        channel = data.channels[team_id][0]
        channel_id = channel.id

        members = client.channels.list_members(
            team_ref=data.teams[0].display_name,
            channel_ref=channel.name,
        )

        expected_members = data.members[team_id][channel_id]

        assert len(members) == len(expected_members)

        assert members[0].user_id == expected_members[0].user_id
        assert members[0].display_name == expected_members[0].display_name
        expected_role_0 = "owner" if expected_members[0].role == "owner" else ""
        assert members[0].role == expected_role_0
        assert members[0].email == expected_members[0].email
        assert members[0].id == expected_members[0].id

        assert members[1].user_id == expected_members[1].user_id
        assert members[1].display_name == expected_members[1].display_name
        expected_role_1 = "owner" if expected_members[1].role == "owner" else ""
        assert members[1].role == expected_role_1
        assert members[1].email == expected_members[1].email
        assert members[1].id == expected_members[1].id

    finally:
        client.close()


def test_add_member_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        member = client.channels.add_member(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][1].name,
            user_ref=data.newMemberTemplate.display_name,
            is_owner=True if data.newMemberTemplate.role == "owner" else False,
        )

        assert member.user_id == data.newMemberTemplate.user_id
        assert member.display_name == data.newMemberTemplate.display_name
        assert member.role == data.newMemberTemplate.role
        assert member.email == data.newMemberTemplate.email
        assert member.id == data.newMemberTemplate.id

    finally:
        client.close()


def test_update_member_role_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        member = client.channels.update_member_role(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
            user_ref=data.members[data.teams[0].id][data.channels[data.teams[0].id][0].id][1].email,
            is_owner=True
        )

        assert member.user_id == data.members[data.teams[0].id][data.channels[data.teams[0].id][0].id][1].user_id
        assert member.display_name == data.members[data.teams[0].id][data.channels[data.teams[0].id][0].id][1].display_name
        assert member.role == "owner"
        assert member.email == data.members[data.teams[0].id][data.channels[data.teams[0].id][0].id][1].email
        assert member.id == data.members[data.teams[0].id][data.channels[data.teams[0].id][0].id][1].id
    finally:
        client.close()


def test_remove_member_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        success = client.channels.remove_member(
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
            user_ref=data.members[data.teams[0].id][data.channels[data.teams[0].id][0].id][1].email,
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
            team_ref=data.teams[0].display_name,
            channel_ref=data.channels[data.teams[0].id][0].name,
            raw_mentions=MentionKind.TEAM.value,
        )

        assert mention[0].kind == MentionKind.TEAM
        assert mention[0].at_id == 0
        assert mention[0].text == data.teams[0].display_name
        assert mention[0].target_id == data.teams[0].id

    finally:
        client.close()





