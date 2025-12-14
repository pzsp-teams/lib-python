from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from teams_lib_pzsp2_z1.client import TeamsClient

class BaseService:
    def __init__(self, client: TeamsClient):
        self.client = client
