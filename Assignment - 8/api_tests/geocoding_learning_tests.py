import requests


def run_learning_test(place: str, api_key: str):
    print(f"Running learning test for: {place}")

    url = "https://geocode.maps.co/search"
    params = {"q": place, "api_key": api_key}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"API did not return 200 OK. Got {response.status_code}")

    data = response.json()
    if not isinstance(data, list) or len(data) == 0:
        raise RuntimeError("Unexpected response format or empty result list.")

    first_result = data[0]

    required_keys = ["lat", "lon", "display_name"]
    for key in required_keys:
        if key not in first_result:
            raise RuntimeError(f"Key '{key}' missing in response.")

    print("Learning test passed.")
