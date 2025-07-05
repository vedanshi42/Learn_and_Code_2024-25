from abc import ABC, abstractmethod


class IPersonalizationService(ABC):
    @abstractmethod
    def get_personalized_feed(self, user_id):
        pass
