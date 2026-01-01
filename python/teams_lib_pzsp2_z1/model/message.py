from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from teams_lib_pzsp2_z1.model.mention import Mention


class MessageContentType(Enum):
    TEXT = "text"
    HTML = "html"


@dataclass
class MessageFrom:
    UserID: str
    DisplayName: str


@dataclass
class Message:
    ID: str
    Content: str
    ContentType: MessageContentType
    CreatedDateTime: datetime
    From: MessageFrom
    ReplyCount: int


@dataclass
class MessageBody:
    ContentType: MessageContentType
    Content: str
    Mentions: list[Mention]

    def __dict__(self):
        return {
            "ContentType": self.ContentType.value,
            "Content": self.Content,
        }

    def __iter__(self):
        yield "ContentType", self.ContentType.value
        yield "Content", self.Content


@dataclass
class ListMessagesOptions:
    Top: int | None = None
    ExpandReplies: bool = False
