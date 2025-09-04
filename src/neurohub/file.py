from typing import Literal, Optional
from neurohub.base import BaseClient
from uuid import UUID
from typing import IO


CallType = Literal['Outgoing', 'Incoming', 'IncomingRedirection', 'Callback']


class Files():
    def __init__(self, base: BaseClient):
        self._base = base
    def post(self, manager_uuid: UUID | str, file_content: bytes | IO, checklist_uuid: UUID | str, call_id: str, call_type: Optional[CallType] = None, client_uuid: Optional[UUID | str] = None):
        if not self._base.s3_client:
            raise RuntimeError("S3 client is not configured. Please provide AWS credentials when initializing the client.")
        client_uuid = self._base._handle_client_uuid(client_uuid)

        file_name = f"{call_id}.mp3"
        s3_key = f"input/{file_name}"

        self._base.s3_client.put_object(
            Bucket=self._base.s3_bucket,
            Key=s3_key,
            Body=file_content
        )

        # TODO: add audio_channels and file_params to args
        body = {
            'client_uuid': client_uuid,
            'manager_uuid': manager_uuid,
            'file_name': file_name,
            'checklist_uuid': str(checklist_uuid),
            'call_type': call_type
        }
        resp = self._base.make_request('file', 'POST', body=body)
        return UUID(resp['file_uuid'])
