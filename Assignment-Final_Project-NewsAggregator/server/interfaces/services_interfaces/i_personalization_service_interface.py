from abc import ABC, abstractmethod


class IPersonalizationService(ABC):
    @abstractmethod
    def get_and_score_recommended_articles(self, user_id):
        pass
