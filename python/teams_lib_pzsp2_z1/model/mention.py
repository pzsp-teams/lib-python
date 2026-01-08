from dataclasses import dataclass
from enum import Enum


class MentionKind(Enum):
    """Represents the kind of mention in a Microsoft Teams message.

    Attributes:
        USER: Represents a mention of a specific user.
        CHANNEL: Represents a mention of the current channel.
        TEAM: Represents a mention of the entire team.
        EVERYONE: Represents a mention of all participants.
            **Note:** This is applicable to Group Chats only.
    """

    USER = "user"
    CHANNEL = "channel"
    TEAM = "team"
    EVERYONE = "everyone"


@dataclass
class Mention:
    """Represents a mention entity within a Microsoft Teams message.

    This object maps a specific entity (User, Channel, etc.) to a placeholder
    in the message content. Can be obtained by get_mentions() method in the Chats and Channels service.

    Attributes:
        kind (MentionKind): The type of the mention.
        at_id (int): The internal identifier used to link this mention to the
            message content.
            *Example:* If the message body contains `<at id="0">@John</at>`,
            this field should be `0`.
        text (str): The text to display in the message (e.g., "@John Doe").
        target_id (str): The unique identifier (UUID) of the entity being mentioned
            (User ID, Channel ID, or Team ID).
    """

    kind: MentionKind
    at_id: int
    text: str
    target_id: str
