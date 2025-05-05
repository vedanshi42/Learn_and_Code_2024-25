from abc import ABC, abstractmethod


class GeocodingClientInterface(ABC):
    @abstractmethod
    def get_coordinates(self, place_name: str):
        "Returns the latitude and longitude for a given place name."
        pass
