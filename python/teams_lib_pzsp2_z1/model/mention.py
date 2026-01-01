from dataclasses import dataclass
from enum import Enum


class MentionKind(Enum):
    USER = "user"
    CHANNEL = "channel"
    TEAM = "team"
    EVERYONE = "everyone"

@dataclass
class Mention:
    Kind: MentionKind
    AtID: int
    Text: str
    TargetID: str
