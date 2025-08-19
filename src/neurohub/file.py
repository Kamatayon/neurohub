from typing import Literal
from typing_extensions import Optional
from neurohub.base import BaseClient
from uuid import UUID


CallType = Literal['Outgoing', 'Incoming', 'IncomingRedirection', 'Callback']


class Files():
    def __init__(self, base: BaseClient):
        self._base = base
    def post(self, manager_uuid: UUID | str, file_name: str, checklist_uuid: UUID | str, call_type: Optional[CallType], client_uuid: Optional[UUID | str] = None):
        # TODO: add audio_channels and file_params to args
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'manager_uuid': manager_uuid,
            'file_name': file_name,
            'checklist_uuid': checklist_uuid,
            'call_type': call_type
        }
        resp = self._base.make_request('file', 'POST', body=body)
        return UUID(resp['resp_uuid'])
