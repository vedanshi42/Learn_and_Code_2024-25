import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, payload):
        try:
            return requests.post(f"{self.base_url}{endpoint}", json=payload).json()
        except requests.exceptions.RequestException:
            return {"error": "Failed to connect"}
