from uuid import UUID
import httpx

class NeuroHubClient:
    base_url = 'https://v2.api.voiceai.neuro-hub.ru/'
    def __init__(self, secret_key: str, client_uuid: str):
        """
        Initialize the NeuroHub API client.

        Args:
            base_url (str): The base URL of the API (e.g., "https://v2.api.voiceai.neuro-hub.ru")
            secret_key (str): The secret key for Bearer token authorization
        """
        self.secret_key = secret_key
        self.headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }
        self.client_uuid = client_uuid

    def _make_request(self, endpoint: str, method: str, body = None):
        url = f"{self.base_url}{endpoint}"
        if method == 'GET':
            response = requests.get(url, headers=self.headers)
        else:
            response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        resp_body = response.json()
        return resp_body

    def create_department(self, department_name: str) -> UUID:
        print('Client uuid', self.client_uuid)
        payload = {
            "client_uuid": self.client_uuid,
            "department_name": department_name
        }
        print('Payload', payload)
        resp = self._make_request("department", "POST", body=payload)
        return UUID(resp['department_uuid'])
    def get_department(self, department_name: str):
        resp = self._make_request('department', 'GET')
        return {
            'department_uuid': resp['department_uuid'],
            'department_name': resp['department_name']
        }
    def create_manager(self, department_uuid: UUID, name: str) -> UUID:
        payload = {
            'client_uuid': self.client_uuid,
            'manager_name': name,
            'department_uuid': str(department_uuid)
        }
        resp = self._make_request('manager', 'POST', body=payload)
        return UUID(resp['manager_uuid'])
    def send_file(self, manager_uuid: UUID, file_name: str):
        payload = {
            'client_uuid': self.client_uuid,
            'manager_uuid': str(manager_uuid),
            'file_name': file_name,
            # TODO: do something about hardcoded checklist
            'checklist_uuid': 'efb12a3e-1dd6-4fa0-b0b0-465a104267de'
        }
        resp = self._make_request('file', 'POST', body=payload)
        print('Response from send file', resp)
        return UUID(resp['file_uuid'])
