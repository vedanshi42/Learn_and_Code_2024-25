import requests
from server.exceptions.api_exception import ApiException, NetworkError, APIKeyError


class BaseAPIService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params=None):
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
            if response.status_code == 403:
                raise APIKeyError("API key is invalid or unauthorized.")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise NetworkError()
        except requests.exceptions.HTTPError as e:
            raise ApiException(f"API HTTP Error: {e}", status_code=response.status_code)
