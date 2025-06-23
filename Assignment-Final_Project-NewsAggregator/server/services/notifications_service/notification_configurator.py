from server.repositories.keyword_repository import KeywordRepository
from server.repositories.category_repository import CategoryRepository


class NotificationsConfigurator:
    def __init__(self):
        self.keyword_repo = KeywordRepository()
        self.category_repo = CategoryRepository()

    def add_keyword_for_user(self, email: str, keyword: str):
        self.keyword_repo.add_keyword_for_user(email, keyword)

    def add_category_for_user(self, email: str, category: str):
        self.category_repo.subscribe_user_to_category(email, category)

    def toggle_category(self, email: str, category: str):
        self.category_repo.toggle_category(email, category)

    def toggle_keyword(self, email: str, keyword: str):
        self.keyword_repo.toggle_keyword(email, keyword)

    def get_user_keywords(self, email: str):
        return self.keyword_repo.get_keywords_for_user(email)

    def get_user_categories(self, email: str):
        return self.category_repo.get_user_categories(email)
