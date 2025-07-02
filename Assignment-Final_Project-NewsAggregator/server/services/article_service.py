from server.repositories.article_repository import ArticleRepository
from server.repositories.search_article_repository import SearchArticleRepository
from server.repositories.user_saved_article_repository import UserSavedArticleRepository
from server.repositories.feedback_repository import FeedbackService
from server.repositories.reporting_repository import ReportingService


class ArticleService:
    def __init__(self):
        self.article_repo = ArticleRepository()
        self.search_repo = SearchArticleRepository()
        self.save_repo = UserSavedArticleRepository()
        self.feedback_repo = FeedbackService()
        self.report_repo = ReportingService()

    def get_headlines(self, filter_by=None, sort_by=None, user_id=None):
        return self.article_repo.get_filtered_articles(filter_by, sort_by, user_id)

    def save_article(self, user_id, article_id):
        self.save_repo.save_by_id(user_id, article_id)

    def like_article(self, user_id, article_id):
        self.feedback_repo.like_article(user_id, article_id)

    def dislike_article(self, user_id, article_id):
        self.feedback_repo.dislike_article(user_id, article_id)

    def report_article(self, user_id, article_id):
        self.report_repo.report_article(user_id, article_id)

    def get_recommended_articles(self, user_id):
        return self.article_repo.get_recommended_articles(user_id)
