from typing import Optional
from uuid import UUID
import httpx

from neurohub.errors import MissingClientUUID
class BaseClient():
    base_url = 'https://v2.api.voiceai.neuro-hub.ru/'
    def __init__(self, secret_key: str, client_uuid: Optional[UUID]):
        self.secret_key = secret_key
        self.headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }
        self.client = httpx.Client(headers=self.headers, base_url=self.base_url)
        self.client_uuid = client_uuid

    def _make_request(self, endpoint: str, method: str, body=None, params=None):
        if method == 'GET':
            response = self.client.get(endpoint, params=params)
        elif method == 'DELETE':
            response = self.client.delete(endpoint, params=params)
        else:
            response = self.client.post(endpoint, json=body)
        # TODO: custom exception handling
        response.raise_for_status()
        resp_body = response.json()
        return resp_body

    def _handle_client_uuid(self, arg: Optional[UUID]):
        if arg:
            return arg
        if self.client_uuid:
            return self.client_uuid
        raise MissingClientUUID()
