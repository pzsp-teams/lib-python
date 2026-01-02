from dataclasses import dataclass
from enum import Enum


class ChatType(Enum):
    ONEONONE = "one-on-one"
    GROUP = "group"


@dataclass
class Chat:
    ID: str
    Type: ChatType
    IsHidden: bool
    Topic: str


@dataclass
class ChatRef:
    Ref: str
    Type: ChatType
