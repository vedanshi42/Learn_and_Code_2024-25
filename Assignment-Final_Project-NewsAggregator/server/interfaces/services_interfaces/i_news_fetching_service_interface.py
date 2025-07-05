from abc import ABC, abstractmethod


class INewsFetchingService(ABC):
    @abstractmethod
    def fetch_all(self):
        pass
