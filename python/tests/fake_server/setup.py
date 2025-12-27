from tests.fake_server.data import FakeServerData
import json
import re
import sys
from werkzeug.wrappers import Response

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

    # Fallback for unmatched routes
    httpserver.expect_request(re.compile(".*")).respond_with_handler(
        lambda req: Response(
            json.dumps({"error": f"Route not matched in Mock: {req.method} {req.path}"}),
            status=404,
            mimetype="application/json"
        )
    )

    return data