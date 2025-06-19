from datetime import datetime, UTC, timedelta
from server.repositories.external_api_repository import ExternalAPIRepository
from server.repositories.category_repository import CategoryRepository
from server.exceptions.api_exception import ApiException
from server.services.api_server.news_api_service import NewsAPIService
from server.services.api_server.the_news_api_service import TheNewsAPIService
from server.services.article_categorizing_service import ArticleCategorizer


class NewsFetcher:
    def __init__(self):
        self.api_repo = ExternalAPIRepository()
        self.category_repo = CategoryRepository()
        self.categorizer = ArticleCategorizer()

        keys = self.api_repo.get_api_keys()
        self.newsapi_service = NewsAPIService("https://newsapi.org", keys.get("NewsAPI"))
        self.thenewsapi_service = TheNewsAPIService("https://api.thenewsapi.com", keys.get("TheNewsAPI"))

    def fetch_all(self):
        try:
            articles_newsapi = self._fetch_from_newsapi()
        except ApiException as e:
            print(f"NewsAPI Error: {e}")
            articles_newsapi = []

        try:
            articles_thenewsapi = self._fetch_from_thenewsapi()
        except ApiException as e:
            print(f"TheNewsAPI Error: {e}")
            articles_thenewsapi = []

        print(f"NewsAPI Articles Fetched: {len(articles_newsapi)}")
        print(f"TheNewsAPI Articles Fetched: {len(articles_thenewsapi)}")

        combined_articles = articles_newsapi + articles_thenewsapi
        return self._assign_and_register_categories(combined_articles)

    def _fetch_from_newsapi(self):
        last_updated = self.api_repo.get_last_accessed("NewsAPI")
        current_time = datetime.now(UTC)
        from_str = (last_updated or current_time - timedelta(hours=3)).strftime('%Y-%m-%d-%H-%M-%S')
        to_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')

        articles = self.newsapi_service.fetch_articles(
            from_date=from_str, to_date=to_str
        )
        self.api_repo.update_status("NewsAPI", "Active")
        return articles

    def _fetch_from_thenewsapi(self):
        articles = self.thenewsapi_service.fetch_top_news()
        self.api_repo.update_status("TheNewsAPI", "Active")
        return articles

    def _assign_and_register_categories(self, articles):
        categorized_articles = self.categorizer.categorize_articles(articles)
        return categorized_articles
