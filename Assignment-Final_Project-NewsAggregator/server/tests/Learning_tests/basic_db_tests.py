from server.services.auth_service import AuthService
from server.repositories.keyword_repository import KeywordRepository
from server.repositories.category_repository import CategoryRepository
from server.services.news_fetching_service import NewsFetcher
from server.repositories.article_repository import ArticleRepository
from server.config.settings import NEWS_API_KEY, THE_NEWS_API_KEY


class TestDBSetup:
    def setup_class(self):
        self.auth_service = AuthService()
        self.keyword_repo = KeywordRepository()
        self.category_repo = CategoryRepository()
        self.fetcher = NewsFetcher(NEWS_API_KEY, THE_NEWS_API_KEY)
        self.article_repo = ArticleRepository()

    def test_signup_user(self):
        user_id = self.auth_service.signup("testuser", "testuser@example.com", "testpass")
        print(f"User created: ID = {user_id}")
        assert user_id is not None

    def test_add_keyword_category(self):
        self.keyword_repo.add_keyword_for_user("testuser@example.com", "sports")
        self.category_repo.add_category("Politics")
        print("Keyword and Category added")

    def test_fetch_and_store_articles(self):
        articles = self.fetcher.fetch_all()
        print(f"Articles fetched: {len(articles)}")
        stored = 0
        for article in articles:
            if self.article_repo.insert_if_new(article):
                stored += 1
        print(f"Articles stored: {stored}")
        assert stored >= 0
