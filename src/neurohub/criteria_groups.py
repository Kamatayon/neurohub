from uuid import UUID
from typing import Optional, List, Dict, Any

from .base import BaseClient
from .types import CriteriaGroup
from src.neurohub.types import CriteriaGroupCriteriaLink

class CriteriaGroups():
    def __init__(self, base: BaseClient):
        self._base = base

    def upsert(self,
               client_uuid: Optional[UUID | str],
               criteria_group_uuid: Optional[UUID | str],
               criteria_group_name: str,
               criteria_group_prompt_id: str,
               parent_criteria_group_uuid: Optional[UUID | str] = None,
               criteria_group_weight: float = 1.0,
               criteria_group_rules: Optional[Dict[str, Any]] = None,
               criteria_group_type: str = "default") -> UUID:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'criteria_group_uuid': str(criteria_group_uuid) if criteria_group_uuid else None,
            'criteria_group_name': criteria_group_name,
            'criteria_group_prompt_id': criteria_group_prompt_id,
            'parent_criteria_group_uuid': str(parent_criteria_group_uuid) if parent_criteria_group_uuid else None,
            'criteria_group_weight': criteria_group_weight,
            'criteria_group_rules': criteria_group_rules or {},
            'criteria_group_type': criteria_group_type
        }
        resp = self._base.make_request('criteria-group', 'POST', body=body)
        return UUID(resp['criteria_group_uuid'])

    def delete(self, criteria_group_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> bool:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'criteria_group_uuid': str(criteria_group_uuid)
        }
        resp = self._base.make_request('criteria-group', 'DELETE', params=params)
        return resp['success']

    def get_by_uuid(self, criteria_group_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> CriteriaGroup:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'criteria_group_uuid': str(criteria_group_uuid)
        }
        resp = self._base.make_request('criteria-group', 'GET', params=params)
        print('Resp', resp)
        return self._parse_criteria_group(resp)

    def get_list(self, client_uuid: Optional[UUID | str] = None) -> List[CriteriaGroup]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {'client_uuid': client_uuid}
        resp = self._base.make_request('criteria-group', 'GET', params=params)
        print('Resp', resp)
        return [self._parse_criteria_group(group) for group in resp]

    def _parse_criteria_group(self, data: Dict[str, Any]) -> CriteriaGroup:
        """Strict parsing into CriteriaGroup TypedDict"""
        return CriteriaGroup(
            criteria_group_uuid=data['criteria_group_uuid'],
            criteria_group_name=data['criteria_group_name'],
            criteria_group_prompt_id=data['criteria_group_prompt_id'],
            parent_criteria_group_uuid=data.get('parent_criteria_group_uuid'),
            criteria_group_weight=data['criteria_group_weight'],
            criteria_group_rules=data['criteria_group_rules'],
            criteria_group_type=data['criteria_group_type'],
            # criteria=[self._parse_criteria(c) for c in data['criteria']]
        )
    def add_criteria(self, criteria_group_uuid: UUID | str, criteria_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> bool:
        """POST /criteria-group-criteria"""
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'criteria_group_uuid': str(criteria_group_uuid),
            'criteria_uuid': str(criteria_uuid)
        }
        resp = self._base.make_request('criteria-group-criteria', 'POST', body=body)
        return resp['success']

    def remove_criteria(self, criteria_group_uuid: UUID | str, criteria_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> bool:
        """DELETE /criteria-group-criteria"""
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'criteria_group_uuid': str(criteria_group_uuid),
            'criteria_uuid': str(criteria_uuid)
        }
        resp = self._base.make_request('criteria-group-criteria', 'DELETE', params=params)
        return resp['success']

    def list_criteria(self, criteria_group_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> List[CriteriaGroupCriteriaLink]:
        """GET /criteria-group-criteria"""
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'criteria_group_uuid': str(criteria_group_uuid)
        }
        resp = self._base.make_request('criteria-group-criteria', 'GET', params=params)
        return [self._parse_criteria_link(item) for item in resp]

    def _parse_criteria_link(self, data: dict) -> CriteriaGroupCriteriaLink:
        return CriteriaGroupCriteriaLink(
            criteria_group_uuid=data['criteria_group_uuid'],
            criteria_group_name=data['criteria_group_name'],
            criteria_uuid=data['criteria_uuid'],
            criteria_name=data['criteria_name']
        )
