from tests.fake_server.data import FakeServerData
import json
import re
import sys
from werkzeug.wrappers import Response
from teams_lib_pzsp2_z1.model.chat import ChatType

def setup_fake_server(httpserver) -> FakeServerData:
    """
    Sets up a fake HTTP server to simulate Microsoft Graph API responses.
    Includes stdout logging for debugging.
    """

    data = FakeServerData()

    def make_log_response(request, data_dict: dict, context_msg: str = "") -> Response:
        print(f"\n[MOCK SERVER] 🟢 REQUEST: {request.method} {request.path}", file=sys.stdout)
        if context_msg:
            print(f"[MOCK SERVER]    Context: {context_msg}", file=sys.stdout)

        if request.content_type == "application/json":
            try:
                req_data = request.json
                if req_data:
                    print(f"[MOCK SERVER]    Body: {req_data}", file=sys.stdout)
            except Exception as e:
                print(f"[MOCK SERVER]    ⚠️ Body Error: {e}", file=sys.stdout)

        status_code = 200 if data_dict else 404
        if request.method in ["POST", "PUT"] and data_dict:
            status_code = 201

        print(f"[MOCK SERVER]    👉 Response: {status_code}", file=sys.stdout)

        return Response(
            json.dumps(data_dict),
            mimetype="application/json",
            status=status_code
        )

    # GET /users/me/joinedTeams
    httpserver.expect_request(
        "/v1.0/users/me-token-to-replace/joinedTeams", method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req, data.get_myJoinedTeams_response(), "List Joined Teams"
    ))

    def handle_chats_request(req):
        filter_param = req.args.get('$filter', '')
        chat_type = None
        match = re.search(r"chatType\s+eq\s+'([^']+)'", filter_param)

        if match:
            chat_type = match.group(1)

        print(f"DEBUG: Parsowanie filtra: '{filter_param}' -> Typ: '{chat_type}'")

        if chat_type == "oneOnOne":
            chat_type = ChatType.ONEONONE
        elif chat_type == "group":
            chat_type = ChatType.GROUP

        return make_log_response(
            req,
            data.get_list_chats_response(chat_type),
            f"List Chats ({chat_type})"
        )

    # GET /users/me/chats
    httpserver.expect_request(
        "/v1.0/users/me-token-to-replace/chats",
        method="GET"
    ).respond_with_handler(handle_chats_request)

    # GET /users/me
    httpserver.expect_request(
        "/v1.0/users/me-token-to-replace",
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_me_response(),
        "Get Users"
    ))

    #POST /chats
    httpserver.expect_request(
        "/v1.0/chats",
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_create_chat_response(req.json),
        "Create Chat"
    ))

    #GET /chats/{chat_id}/members
    httpserver.expect_request(
        re.compile(r"^/v1.0/chats/([^/]+)/members"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_list_group_chat_members_response(
            re.search(r"/chats/([^/]+)/members", req.path).group(1)
        ),
        "List Chat Members"
    ))

    #POST /teams/{team_id}/channels/{channel_id}/members
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/members"),
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_add_member_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members", req.path).group(1),
            req.json
        ),
        "Add member to channel"
    ))


    # PATCH /teams/{tid}/channels/{cid}/members/{mid}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/members/([^/]+)"),
        method="PATCH"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_update_member_role_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members/([^/]+)", req.path).group(1), # team_id
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members/([^/]+)", req.path).group(2), # channel_id
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members/([^/]+)", req.path).group(3), # member_id
            req.json
        ),
        "Update Member Role"
    ))

    # DELETE /teams/{team_id}/channels/{channel_id}/members/{member_id}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/members/([^/]+)"),
        method="DELETE"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_remove_member_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members/([^/]+)", req.path).group(1), # team_id
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members/([^/]+)", req.path).group(2), # channel_id
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members/([^/]+)", req.path).group(3)  # member_id
        ),
        "Remove Member from Channel"
    ))

    #GET /teams/{team_id}/channels/{channel_id}/members
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/members"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_list_members_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/members", req.path).group(2)
        ),
        "List channel members"
    ))


    #POST /teams/{team_id}/channels/{channel_id}/messages
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/messages"),
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_send_message_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages", req.path).group(2),
            req.json
        ),
        "Create Channel Message"
    ))


    # GET /teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies/{reply_id}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies/([^/]+)"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_reply_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies/([^/]+)", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies/([^/]+)", req.path).group(2),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies/([^/]+)", req.path).group(3),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies/([^/]+)", req.path).group(4)
        ),
        "Get Message Reply"
    ))

    # GET /teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_list_replies_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies", req.path).group(2),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)/replies", req.path).group(3)
        ),
        "List Message Replies"
    ))

    # GET /teams/{team_id}/channels/{channel_id}/messages/{message_id}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_message_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)", req.path).group(2),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages/([^/]+)", req.path).group(3)
        ),
        "Get Channel Message"
    ))

    # GET /teams/{team_id}/channels/{channel_id}/messages
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)/messages"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_list_messages_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)/messages", req.path).group(2)
        ),
        "List Channel Messages"
    ))

    # GET /teams/{team_id}/channels/{channel_id}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_channel_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)", req.path).group(2)
        ),
        "Get Channel Details"
    ))

    # GET /teams/{id}/channels
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_listChannels_response(re.search(r"/teams/([^/]+)/channels", req.path).group(1)),
        "List Channels"
    ))

    # POST /groups
    httpserver.expect_request(
        "/v1.0/groups",
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_createGroup_response(req.json),
        "Create Group"
    ))

    # PUT /groups/{id}/team
    httpserver.expect_request(
        re.compile(r"^/v1.0/groups/([^/]+)/team"),
        method="PUT"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_createTeamViaGroup_response(re.search(r"/groups/([^/]+)/team", req.path).group(1)),
        "Teamify Group (PUT)"
    ))

    # GET /teams/{id}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)(?:$|\?)"),
        method="GET"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_team_response(re.search(r"/teams/([^/?]+)", req.path).group(1)),
        "Get Team Details"
    ))

    # PATCH /teams/{id}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)"),
        method="PATCH"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_updateTeam_response(
            re.search(r"/teams/([^/]+)", req.path).group(1),
            req.json
        ),
        "Update Team (PATCH)"
    ))

    # POST /teams
    httpserver.expect_request(
        "/v1.0/teams",
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_createTeamFromTemplate_response(req.json),
        "Create Team from Template (POST)"
    ))

    # POST /teams/{id}/archive
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/archive"),
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_archiveTeam_response(re.search(r"/teams/([^/]+)/archive", req.path).group(1)),
        "Archive Team (POST)"
    ))

    # POST /teams/{id}/unarchive
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/unarchive"),
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_unarchiveTeam_response(re.search(r"/teams/([^/]+)/unarchive", req.path).group(1)),
        "Unarchive Team (POST)"
    ))

    # DELETE /teams/{id}/delete
    httpserver.expect_request(
        re.compile(r"^/v1.0/groups/([^/]+)"),
        method="DELETE"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_deleteTeam_response(re.search(r"/groups/([^/]+)", req.path).group(1)),
        "Delete Team (DELETE)"
    ))

    # POST /teams/{id}/restore
    httpserver.expect_request(
        re.compile(r"^/v1.0/directory/deletedItems/([^/]+)/restore"),
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_restoreTeam_response(re.search(r"/directory/deletedItems/([^/]+)/restore", req.path).group(1)),
        "Restore Deleted Team (POST)"
    ))

    # POST /teams/{id}/channels
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels"),
        method="POST"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_create_channel_response(
            re.search(r"/teams/([^/]+)/channels", req.path).group(1),
            req.json
        ),
        "Create Channel (POST)"
    ))

    # DELETE /teams/{team_id}/channels/{channel_id}
    httpserver.expect_request(
        re.compile(r"^/v1.0/teams/([^/]+)/channels/([^/]+)"),
        method="DELETE"
    ).respond_with_handler(lambda req: make_log_response(
        req,
        data.get_delete_channel_response(
            re.search(r"/teams/([^/]+)/channels/([^/]+)", req.path).group(1),
            re.search(r"/teams/([^/]+)/channels/([^/]+)", req.path).group(2)
        ),
        "Delete Channel (DELETE)"
    ))



    # Fallback for unmatched routes
    httpserver.expect_request(re.compile(".*")).respond_with_handler(
        lambda req: Response(
            json.dumps({"error": f"Route not matched in Mock: {req.method} {req.path}"}),
            status=404,
            mimetype="application/json"
        )
    )

    return data