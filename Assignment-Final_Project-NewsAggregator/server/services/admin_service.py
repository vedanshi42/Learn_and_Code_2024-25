from server.repositories.external_api_repository import ExternalAPIRepository
from server.repositories.category_repository import CategoryRepository
from server.repositories.keyword_repository import KeywordRepository
from server.repositories.article_repository import ArticleRepository


class AdminService:
    def __init__(self, external_repo=None, category_repo=None, keyword_repo=None, article_repo=None):
        self.external_repo = external_repo or ExternalAPIRepository()
        self.category_repo = category_repo or CategoryRepository()
        self.keyword_repo = keyword_repo or KeywordRepository()
        self.article_repo = article_repo or ArticleRepository()

    def get_external_keys(self):
        return self.external_repo.get_all_keys()

    def update_api_key(self, api_name, api_key):
        return self.external_repo.update_api_key(api_name, api_key)

    def get_all_categories(self):
        try:
            return self.category_repo.get_all_categories_with_status()
        except Exception as e:
            raise e

    def add_category(self, name):
        try:
            return self.category_repo.add_category(name)
        except Exception as e:
            raise e

    def disable_category(self, category_name):
        try:
            return self.category_repo.disable_category(category_name)
        except Exception as e:
            raise e

    def get_all_keywords(self):
        try:
            return self.keyword_repo.get_all_keywords_with_status()
        except Exception as e:
            raise e

    def disable_keyword_globally(self, keyword):
        try:
            return self.keyword_repo.disable_keyword_globally(keyword)
        except Exception as e:
            raise e

    def get_reported_articles(self):
        try:
            return self.article_repo.get_reported_articles_with_counts()
        except Exception as e:
            raise e

    def delete_article(self, user_id, article_id):
        try:
            return self.article_repo.delete_article(user_id, article_id)
        except Exception as e:
            raise e

    def get_external_statuses(self):
        try:
            return self.external_repo.get_all_statuses()
        except Exception as e:
            raise e
