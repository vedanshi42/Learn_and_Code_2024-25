from abc import ABC, abstractmethod
from server.models.article import Article


class IArticleRepository(ABC):
    @abstractmethod
    def insert_if_new(self, article: Article):
        pass
