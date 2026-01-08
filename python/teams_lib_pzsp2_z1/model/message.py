from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from teams_lib_pzsp2_z1.model.mention import Mention


class MessageContentType(Enum):
    """Represents the type of content in a Microsoft Teams message.

    Attributes:
        TEXT: Plain text content.
        HTML: HTML formatted content.
    """

    TEXT = "text"
    HTML = "html"


@dataclass
class MessageFrom:
    """Represents the sender of a message in Microsoft Teams.

    Attributes:
        user_id (str): The unique Azure Active Directory (AAD) identifier of the sender.
        display_name (str): The visible name of the sender.
    """

    user_id: str
    display_name: str


@dataclass
class Message:
    """Represents a Microsoft Teams chat message.

    Used in both direct chats and channels.

    Attributes:
        id (str): The unique identifier of the message.
        content (str): The actual body text or HTML of the message.
        content_type (MessageContentType): The format of the content (Text or HTML).
        created_date_time (datetime): The timestamp when the message was created.
        sender (MessageFrom): The user who sent the message.
            **Note:** Mapped from the `From` field in the API/Go model to avoid
            conflict with the Python `from` keyword.
        reply_count (int): The number of replies to this message.
    """

    id: str
    content: str
    content_type: MessageContentType
    created_date_time: datetime
    sender: MessageFrom
    reply_count: int


@dataclass
class MessageBody:
    """Represents the body of a message to be sent.

    This class contains the payload structure required to send a new message
    or reply.

    Attributes:
        content_type (MessageContentType): The format of the content.
        content (str): The text or HTML content.
        mentions (List[Mention]): A list of mentions to include in the message.
    """

    content_type: MessageContentType
    content: str
    mentions: list[Mention]

    def __dict__(self):
        """Serializes the object keys to PascalCase for the Go backend."""

        return {
            "ContentType": self.content_type.value,
            "Content": self.content,
        }

    def __iter__(self):
        """Allows iteration over fields with PascalCase keys."""

        yield "ContentType", self.content_type.value
        yield "Content", self.content


@dataclass
class ListMessagesOptions:
    """Contains options for listing messages (pagination and expansion).

    Attributes:
        top (Optional[int]): The maximum number of messages to return in one page.
            Defaults to None (server default).
        expand_replies (bool): If True, the response will include replies
            nested within the messages. Defaults to False.
    """

    top: int | None = None
    expand_replies: bool = False


@dataclass
class MessageCollection:
    """Represents a paginated collection of messages.

    Attributes:
        messages (List[Message]): The list of message objects in the current page.
        next_link (Optional[str]): The URL to retrieve the next page of results.
            If None, there are no more messages.
    """

    messages: list[Message]
    next_link: str | None = None
