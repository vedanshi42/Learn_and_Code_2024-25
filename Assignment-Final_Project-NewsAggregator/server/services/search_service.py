from server.repositories.search_article_repository import SearchArticleRepository
from server.interfaces.services_interfaces.i_search_service_interface import ISearchService


class SearchService(ISearchService):
    def __init__(self, repo=None):
        self.repo = repo or SearchArticleRepository()

    def search_by_category(self, category: str):
        return self.repo.search_by_category(category)

    def search_by_keyword(self, keyword: str):
        return self.repo.search_by_keyword(keyword)

    def search_by_date(self, date: str):
        return self.repo.search_by_date(date)
