import requests
from interfaces.geocoding_client_interface import GeocodingClientInterface
from exceptions.geocoding_exceptions import GeocodingError


class GoogleGeocodingClient(GeocodingClientInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_coordinates_from_place_name(self, place_name: str):

        try:
            params = {
                "address": place_name,
                "key": self.api_key
            }

            response = requests.get(f"https://geocode.maps.co/search?q={params['address']}&api_key={params['key']}")
            response.raise_for_status()
        except requests.RequestException as e:
            raise GeocodingError(f"Failed to connect to geocoding service: {str(e)}")

        data = response.json()

        if not data:
            raise GeocodingError(f"Could not find location for '{place_name}'.")

        location = (data[0]['display_name'], data[0]['lat'], data[0]['lon'])
        return location
