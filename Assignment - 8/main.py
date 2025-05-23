from clients.google_geocoding_client import GoogleGeocodingClient
from api_tests.geocoding_learning_tests import run_learning_test
from services.location_service import LocationService
from app.location_app import LocationApp


if __name__ == "__main__":

    api_key = input('Enter user specific API key').strip()

    try:
        run_learning_test("Geneva", api_key)
    except Exception as e:
        print(f"Learning test failed: {e}")
        exit(1)  # Stop the app if the API is not behaving as expected

    geocoding_client = GoogleGeocodingClient(api_key)
    location_service = LocationService(geocoding_client)
    app = LocationApp(location_service)

    app.run()
