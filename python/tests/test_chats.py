from teams_lib_pzsp2_z1.client import TeamsClient
from tests.init_fake_client import init_fake_client
from tests.fake_server.setup import setup_fake_server
from teams_lib_pzsp2_z1.model.chat import ChatType, ChatRef
from teams_lib_pzsp2_z1.model.message import MessageContentType, MessageBody
from teams_lib_pzsp2_z1.model.mention import MentionKind
from datetime import datetime


def test_list_my_group_chats_integration(httpserver):
    """
    Integration test: Python -> Go Binary -> Fake HTTP -> Python Mock Server
    """

    data = setup_fake_server(httpserver)

    # Init fake client
    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chats = client.chats.list_my_joined(ChatType.GROUP)

        assert len(chats) == len(data.group_chats)
        assert chats[0].id == data.group_chats[0].id
        assert chats[0].type == data.group_chats[0].type
        assert chats[0].topic == data.group_chats[0].topic
        assert chats[0].is_hidden == data.group_chats[0].is_hidden

        assert chats[1].id == data.group_chats[1].id
        assert chats[1].type == data.group_chats[1].type
        assert chats[1].topic == data.group_chats[1].topic
        assert chats[1].is_hidden == data.group_chats[1].is_hidden

    finally:
        client.close()

def test_list_my_one_on_one_chats_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chats = client.chats.list_my_joined(ChatType.ONE_ON_ONE)

        assert len(chats) == len(data.oneonone_chats)
        assert chats[0].id == data.oneonone_chats[0].id
        assert chats[0].type == data.oneonone_chats[0].type
        assert chats[0].topic == data.oneonone_chats[0].topic
        assert chats[0].is_hidden == data.oneonone_chats[0].is_hidden

    finally:
        client.close()


def test_create_group_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chat = client.chats.create_group_chat(
            topic=data.newChatTemplate.topic,
            recipient_refs=[
                data.users[0].email,
                data.users[1].email,
            ],
            include_me=True,
        )

        assert chat.id == data.newChatTemplate.id
        assert chat.type == ChatType.GROUP
        assert chat.topic == data.newChatTemplate.topic
        assert chat.is_hidden == data.newChatTemplate.is_hidden

    finally:
        client.close()

def test_create_one_on_one_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chat = client.chats.create_one_on_one(
            recipient_ref=data.users[0].email,
        )

        assert chat.id == data.newChatTemplate.id
        assert chat.type == ChatType.ONE_ON_ONE
        assert chat.topic == None
        assert chat.is_hidden == data.newChatTemplate.is_hidden

    finally:
        client.close()


def test_list_group_chat_members_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        members = client.chats.list_group_chat_members(data.group_chats[0].topic)

        assert len(members) == len(data.group_chat_members[data.group_chats[0].id])

        assert members[0].id == data.group_chat_members[data.group_chats[0].id][0].id
        assert members[0].user_id == data.group_chat_members[data.group_chats[0].id][0].user_id
        assert members[0].display_name == data.group_chat_members[data.group_chats[0].id][0].display_name
        if data.group_chat_members[data.group_chats[0].id][0].role == "owner":
            assert members[0].role == "owner"
        assert members[0].email == data.group_chat_members[data.group_chats[0].id][0].email

        assert members[1].id == data.group_chat_members[data.group_chats[0].id][1].id
        assert members[1].user_id == data.group_chat_members[data.group_chats[0].id][1].user_id
        assert members[1].display_name == data.group_chat_members[data.group_chats[0].id][1].display_name
        if data.group_chat_members[data.group_chats[0].id][1].role == "owner":
            assert members[1].role == "owner"
        assert members[1].email == data.group_chat_members[data.group_chats[0].id][1].email

    finally:
        client.close()


def test_add_group_chat_member_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        member = client.chats.add_member_to_group_chat(
            group_chat_ref=data.group_chats[0].topic,
            user_ref=data.newMemberTemplate.email,
        )

        assert member.id == data.newMemberTemplate.id
        assert member.user_id == data.newMemberTemplate.user_id
        assert member.display_name == data.newMemberTemplate.display_name
        assert member.role == data.newMemberTemplate.role
        assert member.email == data.newMemberTemplate.email
    finally:
        client.close()


def test_remove_group_chat_member_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        result = client.chats.remove_member_from_group_chat(
            group_chat_ref=data.group_chats[0].topic,
            member_ref=data.group_chat_members[data.group_chats[0].id][0].email,
        )

        assert result is True

    finally:
        client.close()


def test_update_group_chat_topic_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chat = client.chats.update_group_chat_topic(
            group_chat_ref=data.group_chats[0].topic,
            new_topic=data.updatedGroupChatTopic,
        )

        assert chat.id == data.group_chats[0].id
        assert chat.type == data.group_chats[0].type
        assert chat.topic == data.updatedGroupChatTopic
        assert chat.is_hidden == data.group_chats[0].is_hidden

    finally:
        client.close()


def test_list_messeges_in_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        collection = client.chats.list_messages(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            )
        )

        assert len(collection.messages) == len(data.chat_messages[data.group_chats[0].id])

        assert collection.messages[0].id == data.chat_messages[data.group_chats[0].id][0].id
        assert collection.messages[0].content == data.chat_messages[data.group_chats[0].id][0].content
        assert collection.messages[0].content_type == MessageContentType(data.chat_messages[data.group_chats[0].id][0].content_type)
        assert collection.messages[0].sender.user_id == data.chat_messages[data.group_chats[0].id][0].sender.user_id
        assert collection.messages[0].sender.display_name == data.chat_messages[data.group_chats[0].id][0].sender.display_name
        assert collection.messages[0].reply_count == data.chat_messages[data.group_chats[0].id][0].reply_count
        assert collection.messages[0].created_date_time == data.chat_messages[data.group_chats[0].id][0].created_date_time

        assert collection.messages[1].id == data.chat_messages[data.group_chats[0].id][1].id
        assert collection.messages[1].content == data.chat_messages[data.group_chats[0].id][1].content
        assert collection.messages[1].content_type == MessageContentType(data.chat_messages[data.group_chats[0].id][1].content_type)
        assert collection.messages[1].sender.user_id == data.chat_messages[data.group_chats[0].id][1].sender.user_id
        assert collection.messages[1].sender.display_name == data.chat_messages[data.group_chats[0].id][1].sender.display_name
        assert collection.messages[1].reply_count == data.chat_messages[data.group_chats[0].id][1].reply_count
        assert collection.messages[1].created_date_time == data.chat_messages[data.group_chats[0].id][1].created_date_time

    finally:
        client.close()

def test_send_message_in_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        message = client.chats.send_message(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            ),
            body=MessageBody(
                content=data.newMessageTemplate.content,
                content_type=MessageContentType(data.newMessageTemplate.content_type),
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

def test_delete_message_in_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        result = client.chats.delete_message(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            ),
            message_id=data.chat_messages[data.group_chats[0].id][0].id,
        )

        assert result is True

    finally:
        client.close()

def test_get_message_in_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        message = client.chats.get_message(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            ),
            message_id=data.chat_messages[data.group_chats[0].id][0].id,
        )

        assert message.id == data.chat_messages[data.group_chats[0].id][0].id
        assert message.content == data.chat_messages[data.group_chats[0].id][0].content
        assert message.content_type == MessageContentType(data.chat_messages[data.group_chats[0].id][0].content_type)
        assert message.sender.user_id == data.chat_messages[data.group_chats[0].id][0].sender.user_id
        assert message.sender.display_name == data.chat_messages[data.group_chats[0].id][0].sender.display_name
        assert message.reply_count == data.chat_messages[data.group_chats[0].id][0].reply_count
        assert message.created_date_time == data.chat_messages[data.group_chats[0].id][0].created_date_time
    finally:
        client.close()


def test_get_all_messages_in_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        messages = client.chats.list_all_messages(
            start_time=datetime.min,
            end_time=datetime.max,
            top=50,
        )

        assert len(messages) == len(data.chat_messages[data.group_chats[0].id])

        assert messages[0].id == data.chat_messages[data.group_chats[0].id][0].id
        assert messages[0].content == data.chat_messages[data.group_chats[0].id][0].content
        assert messages[0].content_type == MessageContentType(data.chat_messages[data.group_chats[0].id][0].content_type)
        assert messages[0].sender.user_id == data.chat_messages[data.group_chats[0].id][0].sender.user_id
        assert messages[0].sender.display_name == data.chat_messages[data.group_chats[0].id][0].sender.display_name
        assert messages[0].reply_count == 0
        assert messages[0].created_date_time == data.chat_messages[data.group_chats[0].id][0].created_date_time

        assert messages[1].id == data.chat_messages[data.group_chats[0].id][1].id
        assert messages[1].content == data.chat_messages[data.group_chats[0].id][1].content
        assert messages[1].content_type == MessageContentType(data.chat_messages[data.group_chats[0].id][1].content_type)
        assert messages[1].sender.user_id == data.chat_messages[data.group_chats[0].id][1].sender.user_id
        assert messages[1].sender.display_name == data.chat_messages[data.group_chats[0].id][1].sender.display_name
        assert messages[1].reply_count == 0
        assert messages[1].created_date_time == data.chat_messages[data.group_chats[0].id][1].created_date_time

    finally:
        client.close()


def test_list_pinned_messages_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        messages = client.chats.list_pinned_messages(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            )
        )

        assert len(messages) == len(data.chat_messages[data.group_chats[0].id])

        assert messages[0].id == data.chat_messages[data.group_chats[0].id][0].id
        assert messages[0].content == data.chat_messages[data.group_chats[0].id][0].content
        assert messages[0].content_type == MessageContentType(data.chat_messages[data.group_chats[0].id][0].content_type)
        assert messages[0].sender.user_id == data.chat_messages[data.group_chats[0].id][0].sender.user_id
        assert messages[0].sender.display_name == data.chat_messages[data.group_chats[0].id][0].sender.display_name
        assert messages[0].reply_count == 0
        assert messages[0].created_date_time == data.chat_messages[data.group_chats[0].id][0].created_date_time

        assert messages[1].id == data.chat_messages[data.group_chats[0].id][1].id
        assert messages[1].content == data.chat_messages[data.group_chats[0].id][1].content
        assert messages[1].content_type == MessageContentType(data.chat_messages[data.group_chats[0].id][1].content_type)
        assert messages[1].sender.user_id == data.chat_messages[data.group_chats[0].id][1].sender.user_id
        assert messages[1].sender.display_name == data.chat_messages[data.group_chats[0].id][1].sender.display_name
        assert messages[1].reply_count == 0
        assert messages[1].created_date_time == data.chat_messages[data.group_chats[0].id][1].created_date_time

    finally:
        client.close()


def test_pin_message_in_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        result = client.chats.pin_message(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            ),
            message_id=data.chat_messages[data.group_chats[0].id][0].id,
        )

        assert result is True

    finally:
        client.close()


def test_unpin_message_in_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        result = client.chats.unpin_message(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            ),
            message_id=data.chat_messages[data.group_chats[0].id][0].id,
        )

        assert result is True

    finally:
        client.close()


def test_get_mention_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        mention = client.chats.get_mentions(
            chat_ref=ChatRef(
                ref=data.group_chats[0].topic,
                type=ChatType.GROUP,
            ),
            raw_mentions=MentionKind.EVERYONE.value,
        )

        assert mention[0].kind == MentionKind.EVERYONE.value
        assert mention[0].at_id == 0
        assert mention[0].text == "Everyone"
        assert mention[0].target_id == data.group_chats[0].id

    finally:
        client.close()

