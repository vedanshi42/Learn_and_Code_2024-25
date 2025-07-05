import unittest
from unittest.mock import patch
from server.services.news_fetching_service import NewsFetcher


class TestNewsFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = NewsFetcher()

    @patch("server.services.news_fetching_service.NewsAPIService")
    @patch("server.services.news_fetching_service.TheNewsAPIService")
    @patch("server.services.news_fetching_service.ExternalAPIRepository")
    @patch("server.services.news_fetching_service.ArticleCategorizer")
    def test_fetch_all(
        self, mock_categorizer, mock_api_repo, mock_thenewsapi, mock_newsapi
    ):
        mock_api_repo.return_value.get_api_keys.return_value = {
            "NewsAPI": "key1",
            "TheNewsAPI": "key2",
        }
        mock_newsapi.return_value.fetch_articles.return_value = [{"title": "A"}]
        mock_thenewsapi.return_value.fetch_articles.return_value = [{"title": "B"}]
        mock_categorizer.return_value.categorize_articles.return_value = [
            "catA",
            "catB",
        ]
        self.fetcher.api_repo = mock_api_repo.return_value
        self.fetcher.newsapi_service = mock_newsapi.return_value
        self.fetcher.thenewsapi_service = mock_thenewsapi.return_value
        self.fetcher.categorizer = mock_categorizer.return_value
        result = self.fetcher.fetch_all()
        self.assertEqual(result, ["catA", "catB"])


if __name__ == "__main__":
    unittest.main()
