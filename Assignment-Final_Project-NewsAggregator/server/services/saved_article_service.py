from server.repositories.user_saved_article_repository import UserSavedArticleRepository
from server.interfaces.services_interfaces.i_saved_article_service_interface import ISavedArticleService


class SavedArticleService(ISavedArticleService):
    def __init__(self, repo=None):
        self.repo = repo or UserSavedArticleRepository()

    def get_saved_articles(self, user_id: int):
        return self.repo.get_saved_articles(user_id)

    def delete_saved_article(self, user_id: int, article_id: int):
        return self.repo.delete_by_id(user_id, article_id)
