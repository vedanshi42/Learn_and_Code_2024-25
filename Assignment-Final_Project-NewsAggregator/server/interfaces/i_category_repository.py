from abc import ABC, abstractmethod


class ICategoryRepository(ABC):
    @abstractmethod
    def ensure_category_exists(self, name: str):
        pass

    @abstractmethod
    def get_all_categories(self):
        pass

    @abstractmethod
    def subscribe_user(self, email: str, category: str):
        pass

    @abstractmethod
    def get_user_categories(self, user_id: int):
        pass
