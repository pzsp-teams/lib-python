from teams_lib_pzsp2_z1.client import TeamsClient
from tests.init_fake_client import init_fake_client
from tests.fake_server.setup import setup_fake_server
from teams_lib_pzsp2_z1.model.chat import ChatType


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
        assert chats[0].ID == data.group_chats[0].ID
        assert chats[0].Type == data.group_chats[0].Type
        assert chats[0].Topic == data.group_chats[0].Topic
        assert chats[0].IsHidden == data.group_chats[0].IsHidden

        assert chats[1].ID == data.group_chats[1].ID
        assert chats[1].Type == data.group_chats[1].Type
        assert chats[1].Topic == data.group_chats[1].Topic
        assert chats[1].IsHidden == data.group_chats[1].IsHidden

    finally:
        client.close()

def test_list_my_one_on_one_chats_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chats = client.chats.list_my_joined(ChatType.ONEONONE)

        assert len(chats) == len(data.oneonone_chats)
        assert chats[0].ID == data.oneonone_chats[0].ID
        assert chats[0].Type == data.oneonone_chats[0].Type
        assert chats[0].Topic == data.oneonone_chats[0].Topic
        assert chats[0].IsHidden == data.oneonone_chats[0].IsHidden

    finally:
        client.close()


def test_create_group_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chat = client.chats.create_group_chat(
            topic=data.newChatTemplate.Topic,
            recipient_refs=[
                data.users[0].Email,
                data.users[1].Email,
            ],
            include_me=True,
        )

        assert chat.ID == data.newChatTemplate.ID
        assert chat.Type == ChatType.GROUP
        assert chat.Topic == data.newChatTemplate.Topic
        assert chat.IsHidden == data.newChatTemplate.IsHidden

    finally:
        client.close()

def test_create_one_on_one_chat_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        chat = client.chats.create_one_on_one(
            recipient_ref=data.users[0].Email,
        )

        assert chat.ID == data.newChatTemplate.ID
        assert chat.Type == ChatType.ONEONONE
        assert chat.Topic == None
        assert chat.IsHidden == data.newChatTemplate.IsHidden

    finally:
        client.close()


def test_list_group_chat_members_integration(httpserver):

    data = setup_fake_server(httpserver)

    client = TeamsClient(auto_init=False)
    try:
        init_fake_client(client, httpserver.url_for(""))

        members = client.chats.list_group_chat_members(data.group_chats[0].Topic)

        assert len(members) == len(data.group_chat_members[data.group_chats[0].ID])

        assert members[0].ID == data.group_chat_members[data.group_chats[0].ID][0].ID
        assert members[0].UserID == data.group_chat_members[data.group_chats[0].ID][0].UserID
        assert members[0].DisplayName == data.group_chat_members[data.group_chats[0].ID][0].DisplayName
        if data.group_chat_members[data.group_chats[0].ID][0].Role == "owner":
            assert members[0].Role == "owner"
        assert members[0].Email == data.group_chat_members[data.group_chats[0].ID][0].Email

        assert members[1].ID == data.group_chat_members[data.group_chats[0].ID][1].ID
        assert members[1].UserID == data.group_chat_members[data.group_chats[0].ID][1].UserID
        assert members[1].DisplayName == data.group_chat_members[data.group_chats[0].ID][1].DisplayName
        if data.group_chat_members[data.group_chats[0].ID][1].Role == "owner":
            assert members[1].Role == "owner"
        assert members[1].Email == data.group_chat_members[data.group_chats[0].ID][1].Email

    finally:
        client.close()