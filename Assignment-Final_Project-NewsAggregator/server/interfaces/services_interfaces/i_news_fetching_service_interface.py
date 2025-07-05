from abc import ABC, abstractmethod


class INewsFetchingService(ABC):
    @abstractmethod
    def fetch_news(self):
        pass
