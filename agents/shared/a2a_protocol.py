import json
import requests

class A2AClient:
    def __init__(self, agent_url, api_key=None):
        self.agent_url = agent_url
        self.api_key = api_key

    def send(self, message_type, payload):
        body = {
            "type": message_type,
            "payload": payload
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = requests.post(f"{self.agent_url}/a2a", data=json.dumps(body), headers=headers)
        return response.json()
