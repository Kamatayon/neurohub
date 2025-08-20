from uuid import UUID
from typing import Optional, List, Dict, Any

from .base import BaseClient
from .types import Criteria

class CriteriaClient():
    def __init__(self, base: BaseClient):
        self._base = base

    def upsert(self,
               client_uuid: Optional[UUID | str],
               criteria_uuid: Optional[UUID | str],
               criteria_name: str,
               criteria_prompt_id: str,
               criteria_group_uuid: UUID | str,
               criteria_parent_uuid: Optional[UUID | str] = None,
               criteria_examples: Optional[List[str]] = None,
               criteria_iterate: bool = False,
               criteria_weight: float = 1.0,
               criteria_actor: str = "default",
               criteria_description: Optional[str] = None) -> UUID:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        body = {
            'client_uuid': client_uuid,
            'criteria_uuid': str(criteria_uuid) if criteria_uuid else None,
            'criteria_name': criteria_name,
            'criteria_prompt_id': criteria_prompt_id,
            'criteria_parent_uuid': str(criteria_parent_uuid) if criteria_parent_uuid else None,
            'criteria_examples': criteria_examples or [],
            'criteria_iterate': criteria_iterate,
            'criteria_weight': criteria_weight,
            'criteria_actor': criteria_actor,
            'criteria_description': criteria_description or "",
            'criteria_group_uuid': str(criteria_group_uuid)
        }
        resp = self._base.make_request('criteria', 'POST', body=body)
        return UUID(resp['criteria_uuid'])

    def delete(self, criteria_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> bool:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'criteria_uuid': str(criteria_uuid)
        }
        resp = self._base.make_request('criteria', 'DELETE', params=params)
        return resp['success']

    def get_by_uuid(self, criteria_uuid: UUID | str, client_uuid: Optional[UUID | str] = None) -> Criteria:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {
            'client_uuid': client_uuid,
            'criteria_uuid': str(criteria_uuid)
        }
        resp = self._base.make_request('criteria', 'GET', params=params)
        return self._parse_criteria(resp)

    def get_list(self, client_uuid: Optional[UUID | str] = None) -> List[Criteria]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        params = {'client_uuid': client_uuid}
        resp = self._base.make_request('criteria', 'GET', params=params)
        print(resp)
        return [self._parse_criteria(c) for c in resp]

    def _parse_criteria(self, data: Dict[str, Any]) -> Criteria:
        return Criteria(
            criteria_uuid=data['criteria_uuid'],
            criteria_name=data['criteria_name'],
            criteria_prompt_id=data['criteria_prompt_id'],
            criteria_parent_uuid=data.get('criteria_parent_uuid'),
            criteria_examples=data['criteria_examples'],
            criteria_iterate=data['criteria_iterate'],
            criteria_weight=data['criteria_weight'],
            criteria_actor=data['criteria_actor'],
            criteria_description=data['criteria_description'],
        )
