from clients.google_geocoding_client import GoogleGeocodingClient
from services.location_service import LocationService
from app.location_app import LocationApp


if __name__ == "__main__":
    api_key = "68143920d1bc7751750433gslb68b02"  # Only a sample API Key

    geocoding_client = GoogleGeocodingClient(api_key)
    location_service = LocationService(geocoding_client)
    app = LocationApp(location_service)

    app.run()
