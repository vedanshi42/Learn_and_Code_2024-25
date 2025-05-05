from services.location_service import LocationService
from exceptions.geocoding_exceptions import GeocodingError


class LocationApp:
    def __init__(self, location_service: LocationService):
        self.location_service = location_service

    def run(self):
        place = input("Enter a place name: ").strip()

        try:
            place_name, latitude, longitude = self.location_service.get_coordinates_for_place(place)
            print(f"\nResult for '{place_name}':")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except GeocodingError as ge:
            print(f"Geocoding Error: {ge}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
