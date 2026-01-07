from dataclasses import dataclass


@dataclass
class Team:
    ID: str
    DisplayName: str
    Description: str
    IsArchived: bool
    Visibility: str


@dataclass
class UpdateTeam:
    DisplayName: str | None = None
    Description: str | None = None
    Visibility: str | None = None
