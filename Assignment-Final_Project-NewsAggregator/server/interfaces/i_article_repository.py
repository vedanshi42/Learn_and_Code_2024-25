from abc import ABC, abstractmethod
from server.models.article import Article
from typing import List


class IArticleRepository(ABC):
    @abstractmethod
    def insert_if_new(self, article: Article) -> bool:
        pass

    @abstractmethod
    def overwrite_articles(self, articles: List[Article]) -> int:
        pass
