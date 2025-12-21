from dataclasses import dataclass


@dataclass
class Team:
    ID: str
    DisplayName: str
    Description: str
    IsArchived: bool
    Visibility: str
