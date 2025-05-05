from abc import ABC, abstractmethod


class GeocodingClientInterface(ABC):
    @abstractmethod
    def get_coordinates_from_place_name(self, place_name: str):
        "Returns the latitude and longitude for a given place name."
        pass
