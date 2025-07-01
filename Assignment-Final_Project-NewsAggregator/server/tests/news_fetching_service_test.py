from unittest.mock import patch
from datetime import datetime, timedelta, UTC
from server.services.news_fetching_service import NewsFetcher
from server.models.article import Article


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception(f"Status: {self.status_code}")


class TestNewsFetcher:
    def setup_class(self):
        self.fetcher = NewsFetcher()

    @patch("server.services.news_fetching_service.ExternalAPIRepository.get_last_accessed")
    @patch("server.services.news_fetching_service.requests.get")
    def test_fetch_from_newsapi_success(self, mock_get, mock_last_accessed):
        # simulate last_accessed = 1 day ago
        mock_last_accessed.return_value = datetime.now(UTC) - timedelta(days=1)
        mock_get.return_value = MockResponse({
            "articles": [
                {
                    "title": "NewsAPI Sample",
                    "description": "Sample content",
                    "url": "https://example.com/newsapi",
                    "publishedAt": "2025-06-01T10:00:00Z",
                    "category": "Technology"
                }
            ]
        })

        result = self.fetcher._fetch_from_newsapi()
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Article)
        assert result[0].title == "NewsAPI Sample"

    @patch("server.services.news_fetching_service.requests.get")
    def test_fetch_from_thenewsapi_success(self, mock_get):
        mock_get.return_value = MockResponse({
            "data": [
                {
                    "title": "TheNewsAPI Sample",
                    "description": "Another article",
                    "url": "https://example.com/thenewsapi",
                    "published_at": "2025-06-01T11:00:00Z",
                    "category": "World"
                }
            ]
        })

        result = self.fetcher._fetch_from_thenewsapi()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].title == "TheNewsAPI Sample"

    @patch("server.services.news_fetching_service.ExternalAPIRepository.get_last_accessed")
    @patch("server.services.news_fetching_service.requests.get")
    def test_fetch_from_newsapi_failure(self, mock_get, mock_last_accessed):
        mock_last_accessed.return_value = datetime.now(UTC) - timedelta(days=1)
        mock_get.side_effect = Exception("NewsAPI is down")

        result = self.fetcher._fetch_from_newsapi()
        assert result == []

    @patch("server.services.news_fetching_service.requests.get")
    def test_fetch_from_thenewsapi_failure(self, mock_get):
        mock_get.side_effect = Exception("TheNewsAPI is down")

        result = self.fetcher._fetch_from_thenewsapi()
        assert result == []

    @patch("server.services.news_fetching_service.ExternalAPIRepository.get_last_accessed")
    @patch("server.services.news_fetching_service.requests.get")
    def test_fetch_all_combined(self, mock_get, mock_last_accessed):
        mock_last_accessed.return_value = datetime.now(UTC) - timedelta(days=1)

        def side_effect(url, *args, **kwargs):
            if "newsapi" in url and 'thenewsapi' not in url:
                print(f"URL intercepted: {url}")
                return MockResponse({
                    "articles": [{
                        "title": "N1", "url": "https://news1.com",
                        "publishedAt": "2025-06-01T10:00:00Z"
                    }]

                })
            elif "thenewsapi" in url:
                print(f"URL intercepted: {url}")
                return MockResponse({
                    "data": [{
                        "title": "T1", "url": "https://news2.com",
                        "published_at": "2025-06-01T11:00:00Z"
                    }]
                })
            return MockResponse({})

        mock_get.side_effect = side_effect

        results = self.fetcher.fetch_all()
        assert len(results) == 2
        assert all(isinstance(r, Article) for r in results)
