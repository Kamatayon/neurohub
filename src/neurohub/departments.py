from uuid import UUID
from typing import Optional, List, Dict, Any

from neurohub.base import BaseClient


class Departments():
    def __init__(self, base: BaseClient):
        self._base = base

    def upsert(self, client_uuid: Optional[UUID], department_uuid: Optional[UUID], department_name: str,
               latitude: Optional[float] = None, longitude: Optional[float] = None) -> UUID:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'department_uuid': str(department_uuid) if department_uuid else None,
            'department_name': department_name,
            'latitude': latitude,
            'longitude': longitude
        }
        resp = self._base._make_request('department', 'POST', body=body)
        return UUID(resp['department_uuid'])

    def delete(self, department_uuid: UUID, client_uuid: Optional[UUID]) -> bool:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'department_uuid': str(department_uuid)
        }
        resp = self._base._make_request('department', 'DELETE', params=params)
        return resp['success']

    def get_by_uuid(self, department_uuid: UUID, client_uuid: Optional[UUID]) -> Dict[str, Any]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'department_uuid': str(department_uuid)
        }
        resp = self._base._make_request('department', 'GET', params=params)
        return resp

    def get_by_client(self, client_uuid: Optional[UUID] = None) -> List[Dict[str, Any]]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {'client_uuid': client_uuid}
        resp = self._base._make_request('department', 'GET', params=params)
        return resp
