from abc import ABC, abstractmethod


class ISavedArticleService(ABC):
    @abstractmethod
    def get_saved_articles(self, user_id: int):
        pass

    @abstractmethod
    def delete_saved_article(self, user_id: int, article_id: int):
        pass
