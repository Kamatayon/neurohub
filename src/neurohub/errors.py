from typing import Optional
from uuid import UUID


class MissingClientUUID(Exception):
    def __init__(self):
        super().__init__()
        self.message = 'Client UUID is missing. Either pass it as argument or in constructor of the client.'

def handle_client_uuid(class_uuid: Optional[UUID], arg_uuid: Optional[UUID]):
    if arg_uuid:
        return arg_uuid
    if class_uuid:
        return class_uuid
    raise MissingClientUUID()
