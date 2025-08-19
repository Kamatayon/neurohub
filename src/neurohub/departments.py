from typing import Optional, List
from uuid import UUID
from .types import Department

from neurohub.base import BaseClient


class Departments():
    def __init__(self, base: BaseClient):
        self._base = base

    def upsert(self, department_uuid: Optional[str], department_name: str,
               latitude: Optional[float] = None, longitude: Optional[float] = None, client_uuid: Optional[str] = None) -> str:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'department_uuid': department_uuid,
            'department_name': department_name,
            'latitude': latitude,
            'longitude': longitude
        }
        resp = self._base.make_request('department', 'POST', body=body)
        return str(resp['department_uuid'])

    def delete(self, department_uuid: str | UUID, client_uuid: Optional[str] = None) -> bool:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'department_uuid': department_uuid
        }
        resp = self._base.make_request('department', 'DELETE', params=params)
        return resp['success']

    def get_by_uuid(self, department_uuid: str, client_uuid: Optional[str] = None):
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'department_uuid': department_uuid
        }
        resp = self._base.make_request('department', 'GET', params=params)
        return self._parse_json_department(resp)

    def get_list(self, client_uuid: Optional[str] = None) -> List[Department]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {'client_uuid': client_uuid}
        resp = self._base.make_request('department', 'GET', params=params)
        parsed_resp = [self._parse_json_department(dept) for dept in resp]
        return parsed_resp

    def _parse_json_department(self, dict):
        return Department(
            department_uuid=str(dict['department_uuid']),
            department_name=dict['department_name'],
            client_uuid=str(dict['client_uuid']),
            latitude=dict['latitude'],
            longitude=dict['longitude']
        )
