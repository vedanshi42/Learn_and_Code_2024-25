from server.repositories.search_article_repository import SearchArticleRepository
from server.repositories.keyword_repository import KeywordRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.user_repository import UserRepository
from server.repositories.notification_repository import NotificationRepository
from server.config.logging_config import news_agg_logger
from server.interfaces.services_interfaces.i_notification_updater_interface import INotificationUpdater


class NotificationsUpdater(INotificationUpdater):
    def __init__(self):
        self.search_article_repo = SearchArticleRepository()
        self.keyword_repo = KeywordRepository()
        self.category_repo = CategoryRepository()
        self.user_repo = UserRepository()
        self.notification_repo = NotificationRepository()

    def update_notifications_for_all_users(self):
        try:
            users = self.user_repo.get_all_users()
            for user in users:
                try:
                    keywords = self.keyword_repo.get_keywords_for_user(user["user_id"])
                    categories = self.category_repo.get_user_categories(user["user_id"])
                    matched_articles = (
                        self.search_article_repo.find_articles_by_category_or_keyword(
                            categories, keywords
                        )
                    )
                    self.notification_repo.replace_notifications_for_user(
                        user["user_id"], matched_articles
                    )
                except Exception as e:
                    news_agg_logger(
                        40,
                        f"Failed to update notifications for user {user['email']}: {e}",
                    )
            news_agg_logger(20, "Notifications updated for all users.")
        except Exception as e:
            news_agg_logger(40, f"Failed to update notifications for all users: {e}")
            raise
