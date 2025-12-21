from dataclasses import dataclass


@dataclass
class Channel:
    ID: str
    Name: str
    IsGeneral: bool
