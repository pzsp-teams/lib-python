from dataclasses import dataclass
from enum import Enum


class ChatType(Enum):
    """Represents the type of chat in Microsoft Teams.

    Attributes:
        ONE_ON_ONE: Represents a direct conversation between two users.
        GROUP: Represents a conversation with multiple participants.
    """

    ONE_ON_ONE = "one-on-one"
    GROUP = "group"


@dataclass
class Chat:
    """Represents a chat in Microsoft Teams.

    Attributes:
        id (str): The unique identifier of the chat.
        chat_type (ChatType): The type of the conversation (One-on-One or Group).
        is_hidden (bool): Indicates whether the chat is hidden for the user.
        topic (Optional[str]): The subject or topic of the chat.
            This is typically None for one-on-one chats.
    """

    id: str
    type: ChatType
    is_hidden: bool
    topic: str | None


@dataclass
class ChatRef:
    """Represents a polymorphic reference to a chat used for API lookups.

    This class corresponds to `GroupChatRef` and `OneOnOneChatRef` in the Go library.
    The interpretation of the `ref` field depends on the `chat_type`.

    Attributes:
        ref (str): The identifier string.
            * If **chat_type is GROUP**: Can be a unique Chat ID or a Chat Topic.
              **Note**: Using a topic may lead to ambiguities if multiple group chats
              share the same name.
            * If **chat_type is ONE_ON_ONE**: Can be a unique Chat ID or the
              Recipient's reference (User ID or Email).
              **Note**: For resolution by User ID/Email to work, the chat must
              already exist between the logged-in user and the recipient.
        chat_type (ChatType): Determines how the `ref` string is interpreted.
    """
    ref: str
    type: ChatType
