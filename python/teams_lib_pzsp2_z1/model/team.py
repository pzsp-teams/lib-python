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
    displayName: str | None = None
    description: str | None = None
    visibility: str | None = None
