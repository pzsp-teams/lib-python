from dataclasses import dataclass


@dataclass
class Member:
    ID: str
    UserID: str
    DisplayName: str
    Role: str
    Email: str
