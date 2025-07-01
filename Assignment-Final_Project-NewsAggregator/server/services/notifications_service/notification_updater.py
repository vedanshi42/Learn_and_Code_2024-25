from server.repositories.search_article_repository import SearchArticleRepository
from server.repositories.keyword_repository import KeywordRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.user_repository import UserRepository
from server.repositories.notification_repository import NotificationRepository


class NotificationsUpdater:
    def __init__(self):
        self.search_article_repo = SearchArticleRepository()
        self.keyword_repo = KeywordRepository()
        self.category_repo = CategoryRepository()
        self.user_repo = UserRepository()
        self.notification_repo = NotificationRepository()

    def update_notifications_for_all_users(self):
        users = self.user_repo.get_all_users()
        for user in users:
            keywords = self.keyword_repo.get_keywords_for_user(user['email'])
            categories = self.category_repo.get_user_categories(user['email'])
            matched_articles = self.search_article_repo.find_articles_by_category_or_keyword(categories, keywords)
            self.notification_repo.replace_notifications_for_user(user['user_id'], matched_articles)
