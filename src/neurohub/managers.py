from uuid import UUID
from typing import Optional
import httpx

from neurohub.base import BaseClient
from neurohub.errors import handle_client_uuid


class Managers():
    def __init__(self, base: BaseClient):
        self.base = base
    def upsert(self, manager_uuid: UUID, manager_name: str, department_uuid: UUID, client_uuid: Optional[UUID]):
        client_uuid = self.base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'manager_uuid': manager_uuid,
            'manager_name': manager_name,
            'department_uuid': department_uuid
        }
        resp = self.base._make_request('manager', 'POST', body)
        return UUID(resp['manager_uuid'])
    def delete(self, manager_uuid: UUID, client_uuid: Optional[UUID]) -> bool:
        client_uuid = self.base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'manager_uuid': str(manager_uuid)
        }
        resp = self.base._make_request('manager', 'DELETE', params=params)
        return resp['success']
