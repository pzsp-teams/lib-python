"""
This module contains the service for managing Microsoft Teams via the Go backend.
"""

from teams_lib_pzsp2_z1.model.team import Team, UpdateTeam
from teams_lib_pzsp2_z1.services.base_service import BaseService


class TeamsService(BaseService):
    """Service for managing Microsoft Teams lifecycle and properties via the Go backend.

    This class acts as a high-level Python wrapper. It delegates logical operations
    to the underlying Go library.

    **Concepts:**
    * **References**: The `teamRef` argument accepts either the Team UUID or the
        Team Display Name. The Go backend resolves these automatically.
    * **Context**: Operations are executed on behalf of the authenticated user
        (derived from the MSAL context).
    * **Caching**: If the Go client was initialized with cache enabled, this service
        will transparently use cached team references to reduce API calls.
    """

    def get(self, team_ref: str) -> Team:
        """Retrieves a specific team by its reference.

        Args:
            team_ref (str): The reference to the team (UUID or Display Name).
        Returns:
            Team: The requested team object containing details like ID, DisplayName, and Visibility.
        """
        response = self.client.execute(
            cmd_type="request",
            method="getTeam",
            params={
                "teamRef": team_ref,
            },
        )

        return Team(
            id=response["ID"],
            display_name=response["DisplayName"],
            description=response["Description"],
            is_archived=(True if response["IsArchived"] else False),
            visibility=response["Visibility"],
        )

    def list_my_joined(self) -> list[Team]:
        """Lists all teams that the authenticated user has joined.

        Returns:
            list[Team]: A list of team objects the user is a member of.
        """
        response = self.client.execute(
            cmd_type="request",
            method="listMyJoined",
            params={},
        )
        return [
            Team(
                id=team["ID"],
                display_name=team["DisplayName"],
                description=team["Description"],
                is_archived=(True if team["IsArchived"] else False),
                visibility=team["Visibility"],
            )
            for team in response
        ]

    def update(self, team_ref: str, update: UpdateTeam) -> Team:
        """Applies updates to a team's properties.

        Only fields that are not None in the `update` object will be modified.

        Args:
            team_ref (str): The reference to the team (UUID or Display Name).
            update (UpdateTeam): An object containing the fields to update (e.g., DisplayName).

        Returns:
            Team: The updated team object.
        """
        params = {"teamRef": team_ref}
        # Filter out None values to perform a PATCH-like update
        update_dict = {k: v for k, v in update.__dict__.items() if v is not None}
        params["team"] = update_dict

        response = self.client.execute(
            cmd_type="request",
            method="updateTeam",
            params=params,
        )
        return Team(
            id=response["ID"],
            display_name=response["DisplayName"],
            description=response["Description"],
            is_archived=(True if response["IsArchived"] else False),
            visibility=response["Visibility"],
        )

    def create_via_group(
        self, display_name: str, mail_nickname: str, visibility: str
    ) -> Team:
        """Creates a new team associated with a standard Microsoft 365 group.

        Args:
            display_name (str): The name of the new team.
            mail_nickname (str): The mail alias for the underlying group.
            visibility (str): The privacy level ('Public' or 'Private').

        Returns:
            Team: The newly created team object.
        """
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
            id=response["ID"],
            display_name=response["DisplayName"],
            description=response["Description"],
            is_archived=(True if response["IsArchived"] else False),
            visibility=response["Visibility"],
        )

    def create_from_template(  # noqa: PLR0913
        self,
        display_name: str,
        description: str,
        owners: list[str],
        members: list[str] | None = None,
        visibility: str = "public",
        include_me: bool = True,
    ) -> str:
        """Creates a new team based on a template.

        This operation is often asynchronous.

        Args:
            display_name (str): The name of the team.
            description (str): A brief description of the team.
            owners (list[str]): A list of user references (IDs or emails) to be owners.
            members (list[str] | None, optional): A list of user references to be members. Defaults to None.
            visibility (str, optional): The privacy level ('public' or 'private'). Defaults to "public".
            include_me (bool, optional): Whether to add the authenticated user as an owner. Defaults to True.

        Returns:
            str: The ID of the newly created team (or the async operation ID).
        """
        response = self.client.execute(
            cmd_type="request",
            method="createTeamFromTemplate",
            params={
                "displayName": display_name,
                "description": description,
                "owners": owners,
                "members": members,
                "visibility": visibility,
                "includeMe": include_me,
            },
        )
        return response

    def archive(self, team_ref: str, spo_read_only_from_members: bool) -> bool:
        """Archives a team.

        Args:
            team_ref (str): The reference to the team (UUID or Display Name).
            spo_read_only_from_members (bool): If True, sets the associated SharePoint site
                to read-only for members.

        Returns:
            bool: True if the team was successfully archived.
        """
        response = self.client.execute(
            cmd_type="request",
            method="archiveTeam",
            params={
                "teamRef": team_ref,
                "spoReadOnlyFromMembers": spo_read_only_from_members,
            },
        )
        return response == "archived"

    def unarchive(self, team_ref: str) -> bool:
        """Restores an archived team to an active state.

        Args:
            team_ref (str): The reference to the team (UUID or Display Name).
        Returns:
            bool: True if the team was successfully unarchived.
        """
        response = self.client.execute(
            cmd_type="request",
            method="unarchiveTeam",
            params={
                "teamRef": team_ref,
            },
        )
        return response == "unarchived"

    def delete(self, team_ref: str) -> bool:
        """Deletes a team (soft delete).

        Args:
            team_ref (str): The reference to the team (UUID or Display Name).
        Returns:
            bool: True if the delete request was successful.
        """
        response = self.client.execute(
            cmd_type="request",
            method="deleteTeam",
            params={
                "teamRef": team_ref,
            },
        )
        return response == "deleted"

    def restore_deleted(self, deleted_team_ID: str) -> str:
        """Restores a previously deleted team.

        Args:
            deleted_team_ID (str): The ID of the deleted group/team.

        Returns:
            str: The ID of the restored team/group.
        """
        response = self.client.execute(
            cmd_type="request",
            method="restoreDeletedTeam",
            params={
                "deletedGroupID": deleted_team_ID,
            },
        )
        return response
