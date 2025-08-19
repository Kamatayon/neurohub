from neurohub.base import BaseClient
from typing import Optional
from uuid import UUID

from neurohub.checklists import Checklists
from neurohub.clients import Clients
from neurohub.critera_groups import CriteriaGroups
from neurohub.departments import Departments
from neurohub.managers import Managers
from neurohub.file import Files


class RootAPI():
    def __init__(self, secret_key: str, client_uuid: Optional[UUID]):
        self.base = BaseClient(secret_key, client_uuid)

    @property
    def client_uuid(self) -> Optional[UUID]:
        return self.base.client_uuid
    @client_uuid.setter
    def client_uuid(self, value: UUID):
        self.base.client_uuid = value

    @property
    def managers(self):
        return Managers(self.base)
    @property
    def clients(self):
        return Clients(self.base)
    @property
    def departments(self):
        return Departments(self.base)
    @property
    def checklists(self):
        return Checklists(self.base)
    @property
    def criteria_groups(self):
        return CriteriaGroups(self.base)
    @property
    def files(self):
        return Files(self.base)
