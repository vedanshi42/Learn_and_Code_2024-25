from abc import ABC, abstractmethod
from typing import List, Dict


class ICategoryRepository(ABC):

    @abstractmethod
    def add_category(self, name: str):
        pass

    @abstractmethod
    def get_all_categories_with_status(self) -> List[Dict]:
        pass

    @abstractmethod
    def add_if_not_exists(self, category_name: str):
        pass

    @abstractmethod
    def subscribe_user_to_category(self, user_id: int, category: str):
        pass

    @abstractmethod
    def toggle_category(self, user_id: int, category: str):
        pass

    @abstractmethod
    def get_user_categories(self, user_id: int) -> List[Dict]:
        pass

    @abstractmethod
    def disable_category(self, name: str):
        pass
