from abc import ABC, abstractmethod


class IFeedbackRepository(ABC):

    @abstractmethod
    def like_article(self, user_id: int, article_id: int):
        pass

    @abstractmethod
    def dislike_article(self, user_id: int, article_id: int):
        pass
