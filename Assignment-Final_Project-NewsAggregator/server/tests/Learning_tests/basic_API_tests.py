from server.services.news_fetching_service import NewsFetcher
from server.repositories.external_api_repository import ExternalAPIRepository


class TestExternalAPI:
    def setup_class(self):
        self.fetcher = NewsFetcher()
        self.repo = ExternalAPIRepository()

    def test_api_fetch_articles(self):
        articles = self.fetcher.fetch_all()
        print(f"Total articles fetched: {len(articles)}")
        for article in articles[:3]:
            print(f"{article.title[:60]}")
        assert isinstance(articles, list)

    def test_server_status_tracking(self):
        newsapi_time = self.repo.get_last_accessed("NewsAPI")
        thenewsapi_time = self.repo.get_last_accessed("TheNewsAPI")
        print(f"NewsAPI last accessed: {newsapi_time}")
        print(f"TheNewsAPI last accessed: {thenewsapi_time}")
        assert newsapi_time is not None or thenewsapi_time is not None
