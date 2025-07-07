from abc import ABC, abstractmethod


class ISearchService(ABC):
    @abstractmethod
    def search_by_category(self, category: str):
        pass

    @abstractmethod
    def search_by_keyword(self, keyword: str):
        pass

    @abstractmethod
    def search_by_date(self, date: str):
        pass
