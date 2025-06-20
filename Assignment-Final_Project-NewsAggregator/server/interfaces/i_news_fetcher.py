from abc import ABC, abstractmethod


class INewsFetcher(ABC):
    @abstractmethod
    def fetch_all(self):
        pass
