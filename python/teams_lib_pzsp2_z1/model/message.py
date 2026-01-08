from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from teams_lib_pzsp2_z1.model.mention import Mention


class MessageContentType(Enum):
    TEXT = "text"
    HTML = "html"


@dataclass
class MessageFrom:
    user_id: str
    display_name: str


@dataclass
class Message:
    id: str
    content: str
    content_type: MessageContentType
    created_date_time: datetime
    sender: MessageFrom
    reply_count: int


@dataclass
class MessageBody:
    content_type: MessageContentType
    content: str
    mentions: list[Mention]

    def __dict__(self):
        return {
            "ContentType": self.content_type.value,
            "Content": self.content,
        }

    def __iter__(self):
        yield "ContentType", self.content_type.value
        yield "Content", self.content


@dataclass
class ListMessagesOptions:
    top: int | None = None
    expand_replies: bool = False


@dataclass
class MessageCollection:
    messages: list[Message]
    next_link: str | None = None
