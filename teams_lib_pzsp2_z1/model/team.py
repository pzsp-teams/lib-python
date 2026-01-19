from dataclasses import dataclass


@dataclass
class Team:
    """Represents a Microsoft Teams team.

    Attributes:
        id (str): The unique identifier (UUID) of the team.
        display_name (str): The name of the team.
        description (str): A description of the team's purpose.
        is_archived (bool): Indicates whether the team is in an archived state.
            Archived teams are read-only for members.
        visibility (str): The privacy setting of the team.
            Typically "public", "private".
    """

    id: str
    display_name: str
    description: str
    is_archived: bool
    visibility: str


@dataclass
class UpdateTeam:
    """Represents the subset of Team fields that can be updated.

    This class is used as a payload for patch/update operations.
    Only fields that are not None will be sent to the API.

    Attributes:
        display_name (Optional[str]): The new name for the team.
        description (Optional[str]): The new description.
        visibility (Optional[str]): The new visibility setting (e.g., "private").
    """

    display_name: str | None = None
    description: str | None = None
    visibility: str | None = None
