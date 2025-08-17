from uuid import UUID
from typing import Optional, List, Dict, Any

from neurohub.base import BaseClient


class Checklists():
    def __init__(self, base: BaseClient):
        self._base = base

    def upsert(self, client_uuid: Optional[UUID], checklist_uuid: Optional[UUID], checklist_name: str) -> UUID:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid) if checklist_uuid else None,
            'checklist_name': checklist_name
        }
        resp = self._base.make_request('checklist', 'POST', body=body)
        return UUID(resp['checklist_uuid'])

    def delete(self, checklist_uuid: UUID, client_uuid: Optional[UUID]) -> bool:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid)
        }
        resp = self._base.make_request('checklist', 'DELETE', params=params)
        return resp['success']

    def get_by_uuid(self, checklist_uuid: UUID, client_uuid: Optional[UUID]) -> Dict[str, Any]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid)
        }
        resp = self._base.make_request('checklist', 'GET', params=params)
        return resp

    def get_by_client(self, client_uuid: Optional[UUID]) -> List[Dict[str, Any]]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {'client_uuid': client_uuid}
        resp = self._base.make_request('checklist', 'GET', params=params)
        return resp['checklists']
