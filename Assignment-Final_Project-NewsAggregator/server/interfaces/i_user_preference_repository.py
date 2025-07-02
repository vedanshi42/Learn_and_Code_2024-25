from abc import ABC, abstractmethod


class IUserPreferenceRepository(ABC):
    @abstractmethod
    def get_liked_categories(self, user_id: int):
        pass

    @abstractmethod
    def get_enabled_keywords(self, user_id: int):
        pass

    @abstractmethod
    def get_disliked_keywords_and_urls(self, user_id: int):
        pass
