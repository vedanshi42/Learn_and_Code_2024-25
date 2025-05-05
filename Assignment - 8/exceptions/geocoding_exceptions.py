class GeocodingError(Exception):
    """
    Custom exception for geocoding failures.
    Raised when the geocoding service cannot resolve a location.
    """
    def __init__(self, message: str):
        super().__init__(message)
