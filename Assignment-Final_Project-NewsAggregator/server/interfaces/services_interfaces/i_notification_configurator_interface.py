from abc import ABC, abstractmethod


class INotificationConfigurator(ABC):
    @abstractmethod
    def add_keyword_for_user(self, user_id: int, keyword: str):
        pass

    @abstractmethod
    def add_category_for_user(self, user_id: int, category: str):
        pass

    @abstractmethod
    def toggle_category(self, user_id: int, category: str):
        pass

    @abstractmethod
    def toggle_keyword(self, user_id: int, keyword: str):
        pass

    @abstractmethod
    def get_user_keywords(self, user_id: int):
        pass

    @abstractmethod
    def get_user_categories(self, user_id: int):
        pass

    @abstractmethod
    def get_user_notifications(self, user_id: int):
        pass
