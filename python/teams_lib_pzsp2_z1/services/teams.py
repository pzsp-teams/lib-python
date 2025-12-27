from teams_lib_pzsp2_z1.model.team import MSTeamsUpdate, Team
from teams_lib_pzsp2_z1.services.base_service import BaseService


class TeamsService(BaseService):
    def get(self, teamRef: str) -> Team:
        response = self.client.execute(
            cmd_type="request",
            method="getTeam",
            params={
                "teamRef": teamRef,
            },
        )

        return Team(
            ID=response["ID"],
            DisplayName=response["DisplayName"],
            Description=response["Description"],
            IsArchived=(True if response["IsArchived"] else False),
            Visibility=response["Visibility"],
        )

    def list_my_joined(self) -> list[Team]:
        response = self.client.execute(
            cmd_type="request",
            method="listMyJoined",
            params={},
        )
        return [
            Team(
                ID=team["ID"],
                DisplayName=team["DisplayName"],
                Description=team["Description"],
                IsArchived=(True if team["IsArchived"] else False),
                Visibility=team["Visibility"],
            )
            for team in response
        ]

    def update(self, teamRef: str, update: MSTeamsUpdate) -> Team:
        params = {"teamRef": teamRef}
        update_dict = {k: v for k, v in update.__dict__.items() if v is not None}
        params["team"] = update_dict

        response = self.client.execute(
            cmd_type="request",
            method="updateTeam",
            params=params,
        )
        return Team(
            ID=response["ID"],
            DisplayName=response["DisplayName"],
            Description=response["Description"],
            IsArchived=(True if response["IsArchived"] else False),
            Visibility=response["Visibility"],
        )

    def create_via_group(
        self, display_name: str, mail_nickname: str, visibility: str
    ) -> Team:
        response = self.client.execute(
            cmd_type="request",
            method="createTeamViaGroup",
            params={
                "displayName": display_name,
                "mailNickname": mail_nickname,
                "visibility": visibility,
            },
        )
        return Team(
            ID=response["ID"],
            DisplayName=response["DisplayName"],
            Description=response["Description"],
            IsArchived=(True if response["IsArchived"] else False),
            Visibility=response["Visibility"],
        )

    def create_from_template(
        self,
        display_name: str,
        description: str,
        owners: list[str],
    ) -> str:
        response = self.client.execute(
            cmd_type="request",
            method="createTeamFromTemplate",
            params={
                "displayName": display_name,
                "description": description,
                "owners": owners,
            },
        )
        return response

    def archive(self, teamRef: str, spo_read_only_from_members: bool) -> bool:
        response = self.client.execute(
            cmd_type="request",
            method="archiveTeam",
            params={
                "teamRef": teamRef,
                "spoReadOnlyFromMembers": spo_read_only_from_members,
            },
        )
        return response == "archived"

    def unarchive(self, teamRef: str) -> bool:
        response = self.client.execute(
            cmd_type="request",
            method="unarchiveTeam",
            params={
                "teamRef": teamRef,
            },
        )
        return response == "unarchived"

    def delete(self, teamRef: str) -> bool:
        response = self.client.execute(
            cmd_type="request",
            method="deleteTeam",
            params={
                "teamRef": teamRef,
            },
        )
        return response == "deleted"

    def restore_deleted(self, deleted_team_ID: str) -> str:
        response = self.client.execute(
            cmd_type="request",
            method="restoreDeletedTeam",
            params={
                "deletedGroupID": deleted_team_ID,
            },
        )
        return response
