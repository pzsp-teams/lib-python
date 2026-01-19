from dataclasses import dataclass


@dataclass
class Member:
    """Represents a member of a Microsoft Teams channel, direct chat, or team.

    Attributes:
        id (str): The unique identifier of the membership object itself.
            **Note:** This is distinct from the `user_id`.
        user_id (str): The unique Azure Active Directory (AAD) identifier of the user.
        display_name (str): The visible name of the user.
        role (str): The role of the user within the specific context
            (e.g., "owner", "member").
        email (str): The email address of the user.
    """

    id: str
    user_id: str
    display_name: str
    role: str
    email: str
