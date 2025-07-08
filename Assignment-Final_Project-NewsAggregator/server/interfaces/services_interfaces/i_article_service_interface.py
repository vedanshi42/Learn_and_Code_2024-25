from abc import ABC, abstractmethod


class IArticleService(ABC):
    @abstractmethod
    def get_headlines(self, filter_by=None, sort_by=None, user_id=None, from_date=None, to_date=None):
        pass

    @abstractmethod
    def save_article(self, user_id, article_id):
        pass

    @abstractmethod
    def like_article(self, user_id, article_id):
        pass

    @abstractmethod
    def dislike_article(self, user_id, article_id):
        pass

    @abstractmethod
    def insert_articles(self, articles):
        pass
