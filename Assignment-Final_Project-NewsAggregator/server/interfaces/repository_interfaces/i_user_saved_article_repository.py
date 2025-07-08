from abc import ABC, abstractmethod


class IUserSavedArticleRepository(ABC):

    @abstractmethod
    def save_by_id(self, user_id: int, article_id: int):
        pass

    @abstractmethod
    def delete_by_id(self, user_id: int, article_id: int):
        pass

    @abstractmethod
    def get_saved_articles(self, user_id: int):
        pass
