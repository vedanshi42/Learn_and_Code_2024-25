import requests
import time
import json


class RequestHandler:
    def __init__(self):
        self.max_retries = 5

    def make_request(self, url, params=None):
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # If there are errors in response from website, an exception will be raised with the status code.
                return response
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    return self.handle_rate_limit(response)
                else:
                    self.handle_http_error(e)
                    break
            except requests.exceptions.RequestException as e:
                self.handle_request_exception(e)
                break
        return None

    def handle_rate_limit(self, response):
        retry_after = int(response.headers.get("Retry-After", 1))  # To retry after a sleep if there are too many requests
        print(f"Rate limit reached. Retrying after {retry_after} seconds...")
        time.sleep(retry_after)
        return None

    def handle_http_error(self, error):
        print(f"HTTP Error: {error}")

    def handle_request_exception(self, error):
        print(f"Request failed: {error}")

    def parse_response(self, response_text):
        if not self._is_non_empty(response_text):
            print("Empty response received.")
            return None
        try:
            # json response looks like var tumblr_api_read = {"tumblelog":{blog_data}}; 
            # so we are fetching only the part between outer curly braces by using slicing
            json_data = response_text[response_text.find('{'):-2]
            return json.loads(json_data)
        except ValueError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def _is_non_empty(self, text):
        return bool(text.strip())
