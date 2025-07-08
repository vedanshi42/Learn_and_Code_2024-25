from abc import ABC, abstractmethod
from server.models.article import Article


class ICategoryPredictor(ABC):
    @abstractmethod
    def predict(self, article: Article):
        pass
