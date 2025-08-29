from uuid import UUID
from typing import Optional, List, Dict, Any

from neurohub.base import BaseClient
from src.neurohub.types import ChecklistCriteriaGroupLink


class Checklists():
    def __init__(self, base: BaseClient):
        self._base = base

    def upsert(self, client_uuid: Optional[UUID | str], checklist_uuid: Optional[UUID | str], checklist_name: str) -> UUID | str:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid) if checklist_uuid else None,
            'checklist_name': checklist_name
        }
        resp = self._base.make_request('checklist', 'POST', body=body)
        return UUID(resp['checklist_uuid'])

    def delete(self, checklist_uuid: UUID | str, client_uuid: Optional[UUID | str]) -> bool:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid)
        }
        resp = self._base.make_request('checklist', 'DELETE', params=params)
        return resp['success']

    def get_by_uuid(self, checklist_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> Dict[str, Any]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid)
        }
        resp = self._base.make_request('checklist', 'GET', params=params)
        return resp

    def get_by_client(self, client_uuid: Optional[UUID | str] = None) -> List[Dict[str, Any]]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {'client_uuid': client_uuid}
        resp = self._base.make_request('checklist', 'GET', params=params)
        return resp


    def link_criteria_group(self, checklist_uuid: UUID | str, criteria_group_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> bool:
        """POST /checklist-criteria-group"""
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid),
            'criteria_group_uuid': str(criteria_group_uuid)
        }
        resp = self._base.make_request('checklist-criteria-group', 'POST', body=body)
        return resp['success']

    def unlink_criteria_group(self, checklist_uuid: UUID | str, criteria_group_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> bool:
        """DELETE /checklist-criteria-group"""
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid),
            'criteria_group_uuid': str(criteria_group_uuid)
        }
        resp = self._base.make_request('checklist-criteria-group', 'DELETE', params=params)
        return resp['success']

    def get_linked_criteria_groups(self, checklist_uuid: UUID | str, client_uuid: Optional[UUID | str] = None):
        """GET /checklist-criteria-group"""
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'checklist_uuid': str(checklist_uuid)
        }
        resp = self._base.make_request('checklist-criteria-group', 'GET', params=params)
        return [self._parse_link(item) for item in resp]
    def _parse_link(self, data: dict) -> ChecklistCriteriaGroupLink:
        return ChecklistCriteriaGroupLink(
            checklist_uuid=data['checklist_uuid'],
            checklist_name=data['checklist_name'],
            criteria_group_uuid=data['criteria_group_uuid'],
            criteria_group_name=data['criteria_group_name']
        )
