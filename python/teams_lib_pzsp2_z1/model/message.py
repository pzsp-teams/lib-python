from dataclasses import dataclass
from enum import Enum
from time import datetime


class MessageContentType(Enum):
    TEXT = "text"
    HTML = "html"

@dataclass
class MessageFrom:
    UserID: str
    UserDisplayName: str

@dataclass
class Message:
    ID: str
    Content: str
    ContentType: MessageContentType
    CreateDateTime: datetime.datetime
    From: MessageFrom
    ReplyCount: int

