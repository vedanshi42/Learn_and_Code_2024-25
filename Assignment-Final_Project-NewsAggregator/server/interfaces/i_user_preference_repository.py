from abc import ABC, abstractmethod


class IUserPreferenceRepository(ABC):
    @abstractmethod
    def get_liked_categories(self, user_id: int) -> set[str]:
        pass

    @abstractmethod
    def get_enabled_keywords(self, user_id: int) -> list[str]:
        pass

    @abstractmethod
    def get_disliked_keywords_and_urls(self, user_id: int) -> tuple[set[str], list[str]]:
        pass
