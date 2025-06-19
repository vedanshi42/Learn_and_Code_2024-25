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
