from typing import Any, Dict, Optional
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

    def _transform_body(self, body: Dict[str, Any]):
        result = {}
        for key, value in body.items():
            if value is None:
                continue
            if isinstance(value, UUID):
                result[key] = str(value)
                continue
            result[key] = value
        return result


    def make_request(self, endpoint: str, method: str, body: Optional[Dict[str, Any]]=None, params=None):
        if method == 'GET':
            if params:
                params = self._transform_body(params)
            response = self.client.get(endpoint, params=params)
        elif method == 'DELETE':
            response = self.client.delete(endpoint, params=params)
        else:
            if not body:
                raise ValueError('Provide body when making POST request')
            transformed_body = self._transform_body(body)
            response = self.client.post(endpoint, json=transformed_body)
        # TODO: custom exception handling
        response.raise_for_status()
        resp_body = response.json()
        return resp_body

    def _handle_client_uuid(self, arg: Optional[str | UUID]):
        if arg:
            return str(arg)
        if self.client_uuid:
            return str(self.client_uuid)
        raise MissingClientUUID()
