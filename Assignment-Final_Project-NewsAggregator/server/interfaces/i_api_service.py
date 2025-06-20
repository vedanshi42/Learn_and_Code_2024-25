from abc import ABC, abstractmethod


class IAPIService(ABC):
    @abstractmethod
    def fetch_articles(self, from_date=None, to_date=None):
        pass
