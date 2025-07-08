from abc import ABC, abstractmethod


class IKeywordRepository(ABC):

    @abstractmethod
    def add_keyword_for_user(self, user_id: int, keyword: str):
        pass

    @abstractmethod
    def toggle_keyword(self, user_id: int, keyword: str):
        pass

    @abstractmethod
    def get_keywords_for_user(self, user_id: int):
        pass

    @abstractmethod
    def get_all_keywords_with_status(self):
        pass

    @abstractmethod
    def disable_keyword_globally(self, word: str):
        pass
