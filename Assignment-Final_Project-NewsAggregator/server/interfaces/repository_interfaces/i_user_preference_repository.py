from abc import ABC, abstractmethod


class IUserPreferenceRepository(ABC):
    @abstractmethod
    def get_liked_categories(self, user_id: int):
        pass

    @abstractmethod
    def get_disliked_categories(self, user_id: int):
        pass

    @abstractmethod
    def get_liked_keywords(self, user_id: int):
        pass

    @abstractmethod
    def get_disliked_keywords(self, user_id: int):
        pass
