from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
    CreateDateTime: datetime
    From: MessageFrom
    ReplyCount: int

@dataclass
class MessageBody:
    ContentType: MessageContentType
    Content: str

    def __dict__(self):
        return {
            "ContentType": self.ContentType.value,
            "Content": self.Content,
        }

@dataclass
class ListMessagesOptions:
    Top: int | None = None
    ExpandReplies: bool = False

