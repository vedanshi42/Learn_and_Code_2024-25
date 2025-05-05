from interfaces.geocoding_client_interface import GeocodingClientInterface


class LocationService:
    def __init__(self, geocoding_client: GeocodingClientInterface):
        self.geocoding_client = geocoding_client

    def get_coordinates_for_place(self, place_name: str):
        if not place_name or not place_name.strip():
            raise ValueError("Place name cannot be empty.")

        return self.geocoding_client.get_coordinates(place_name.strip())
