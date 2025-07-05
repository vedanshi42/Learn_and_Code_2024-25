from abc import ABC, abstractmethod


class ISearchArticleRepository(ABC):

    @abstractmethod
    def find_articles_by_category_or_keyword(self, category: str, keyword: str):
        pass

    @abstractmethod
    def search_by_keyword(self, keyword: str):
        pass

    @abstractmethod
    def search_by_category(self, category: str):
        pass

    @abstractmethod
    def search_by_date(self, date: str):
        pass
