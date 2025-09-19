from typing import Any, Dict, Optional
from uuid import UUID

import boto3
import httpx

from neurohub.errors import MissingClientUUID


class BaseClient:
    base_url = "https://v2.api.voiceai.neuro-hub.ru/"

    def __init__(
        self,
        secret_key: str,
        client_uuid: Optional[UUID],
        s3_bucket: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        self.secret_key = secret_key
        self.headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }
        self.client = httpx.Client(headers=self.headers, base_url=self.base_url)
        self.client_uuid = client_uuid

        # Initialize S3 client if credentials provided
        self.s3_bucket = s3_bucket
        if s3_bucket and aws_access_key_id and aws_secret_access_key:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                endpoint_url="https://storage.yandexcloud.net/",
            )
            self.s3_client = s3_client

        else:
            self.s3_client = None

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

    def make_request(
        self,
        endpoint: str,
        method: str,
        body: Optional[Dict[str, Any]] = None,
        params=None,
    ):
        if method == "GET":
            if params:
                params = self._transform_body(params)
            response = self.client.get(endpoint, params=params)
        elif method == "DELETE":
            response = self.client.delete(endpoint, params=params)
        else:
            if not body:
                raise ValueError("Provide body when making POST request")
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
