from server.repositories.article_repository import ArticleRepository
from server.repositories.search_article_repository import SearchArticleRepository
from server.repositories.user_saved_article_repository import UserSavedArticleRepository
from server.repositories.feedback_repository import FeedbackService
from server.repositories.reporting_repository import ReportingService
from server.exceptions.repository_exception import RepositoryException
from server.interfaces.services_interfaces.i_article_service_interface import IArticleService


class ArticleService(IArticleService):
    def __init__(self):
        self.article_repo = ArticleRepository()
        self.search_repo = SearchArticleRepository()
        self.save_repo = UserSavedArticleRepository()
        self.feedback_repo = FeedbackService()
        self.report_repo = ReportingService()

    def get_headlines(
        self, filter_by=None, sort_by=None, user_id=None, from_date=None, to_date=None
    ):
        try:
            return self.article_repo.get_filtered_articles(
                filter_by, sort_by, user_id, from_date, to_date
            )
        except RepositoryException as e:
            raise e

    def save_article(self, user_id, article_id):
        try:
            self.save_repo.save_by_id(user_id, article_id)
        except RepositoryException as e:
            raise e

    def like_article(self, user_id, article_id):
        try:
            self.feedback_repo.like_article(user_id, article_id)
        except RepositoryException as e:
            raise e

    def dislike_article(self, user_id, article_id):
        try:
            self.feedback_repo.dislike_article(user_id, article_id)
        except RepositoryException as e:
            raise e

    def report_article(self, user_id, article_id):
        try:
            self.report_repo.report_article(user_id, article_id)
        except RepositoryException as e:
            raise e

    def get_recommended_articles(self, user_id):
        try:
            return self.article_repo.get_recommended_articles(user_id)
        except RepositoryException as e:
            raise e
