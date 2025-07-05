from server.repositories.keyword_repository import KeywordRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.notification_repository import NotificationRepository
from server.config.logging_config import news_agg_logger


class NotificationsConfigurator:
    def __init__(self):
        self.keyword_repo = KeywordRepository()
        self.category_repo = CategoryRepository()
        self.notification_repo = NotificationRepository()

    def add_keyword_for_user(self, user_id: int, keyword: str):
        try:
            self.keyword_repo.add_keyword_for_user(user_id, keyword)
        except Exception as e:
            news_agg_logger(
                40, f"Failed to add keyword '{keyword}' for user {user_id}: {e}"
            )
            raise

    def add_category_for_user(self, user_id: int, category: str):
        try:
            self.category_repo.subscribe_user_to_category(user_id, category)
        except Exception as e:
            news_agg_logger(
                40, f"Failed to add category '{category}' for user {user_id}: {e}"
            )
            raise

    def toggle_category(self, user_id: int, category: str):
        try:
            self.category_repo.toggle_category(user_id, category)
        except Exception as e:
            news_agg_logger(
                40, f"Failed to toggle category '{category}' for user {user_id}: {e}"
            )
            raise

    def toggle_keyword(self, user_id: int, keyword: str):
        try:
            self.keyword_repo.toggle_keyword(user_id, keyword)
        except Exception as e:
            news_agg_logger(
                40, f"Failed to toggle keyword '{keyword}' for user {user_id}: {e}"
            )
            raise

    def get_user_keywords(self, user_id: int):
        try:
            return self.keyword_repo.get_keywords_for_user(user_id)
        except Exception as e:
            news_agg_logger(40, f"Failed to get keywords for user {user_id}: {e}")
            raise

    def get_user_categories(self, user_id: int):
        try:
            return self.category_repo.get_user_categories(user_id)
        except Exception as e:
            news_agg_logger(40, f"Failed to get categories for user {user_id}: {e}")
            raise

    def get_user_notifications(self, user_id: int):
        try:
            return self.notification_repo.get_notifications_for_user(user_id)
        except Exception as e:
            news_agg_logger(40, f"Failed to get notifications for user {user_id}: {e}")
            raise
