from python.teams_lib_pzsp2_z1.client import TeamsClient


class BaseService:
    def __init__(self, client: 'TeamsClient'):
        self.client = client
