import unittest
from unittest.mock import MagicMock
from server.services.news_fetching_service import NewsFetcher
from server.exceptions.api_exception import ApiException


class TestNewsFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = NewsFetcher()

    def test_fetch_all(self):
        mock_api_repo = MagicMock()
        mock_newsapi = MagicMock()
        mock_thenewsapi = MagicMock()
        mock_categorizer = MagicMock()
        mock_api_repo.get_api_keys.return_value = {
            "NewsAPI": "key1",
            "TheNewsAPI": "key2",
        }
        mock_newsapi.fetch_articles.return_value = [{"title": "A"}]
        mock_thenewsapi.fetch_articles.return_value = [{"title": "B"}]
        mock_categorizer.categorize_articles.return_value = ["catA", "catB"]
        fetcher = NewsFetcher(
            api_repo=mock_api_repo,
            newsapi_service=mock_newsapi,
            thenewsapi_service=mock_thenewsapi,
            categorizer=mock_categorizer,
        )
        result = fetcher.fetch_all()
        self.assertEqual(result, ["catA", "catB"])

    def test_fetch_all_empty(self):
        mock_api_repo = MagicMock()
        mock_newsapi = MagicMock()
        mock_thenewsapi = MagicMock()
        mock_categorizer = MagicMock()
        mock_api_repo.get_api_keys.return_value = {
            "NewsAPI": "key1",
            "TheNewsAPI": "key2",
        }
        mock_newsapi.fetch_articles.return_value = []
        mock_thenewsapi.fetch_articles.return_value = []
        mock_categorizer.categorize_articles.return_value = []
        fetcher = NewsFetcher(
            api_repo=mock_api_repo,
            newsapi_service=mock_newsapi,
            thenewsapi_service=mock_thenewsapi,
            categorizer=mock_categorizer,
        )
        result = fetcher.fetch_all()
        self.assertEqual(result, [])

    def test_fetch_all_api_exception(self):
        mock_api_repo = MagicMock()
        mock_newsapi = MagicMock()
        mock_thenewsapi = MagicMock()
        mock_categorizer = MagicMock()
        mock_api_repo.get_api_keys.return_value = {
            "NewsAPI": "key1",
            "TheNewsAPI": "key2",
        }
        mock_newsapi.fetch_articles.side_effect = ApiException("API error")
        mock_thenewsapi.fetch_articles.return_value = []
        mock_categorizer.categorize_articles.return_value = []
        fetcher = NewsFetcher(
            api_repo=mock_api_repo,
            newsapi_service=mock_newsapi,
            thenewsapi_service=mock_thenewsapi,
            categorizer=mock_categorizer,
        )
        result = fetcher.fetch_all()
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    def test_fetch_all_both_api_exception(self):
        mock_api_repo = MagicMock()
        mock_newsapi = MagicMock()
        mock_thenewsapi = MagicMock()
        mock_categorizer = MagicMock()
        mock_api_repo.get_api_keys.return_value = {
            "NewsAPI": "key1",
            "TheNewsAPI": "key2",
        }
        mock_newsapi.fetch_articles.side_effect = ApiException("API error 1")
        mock_thenewsapi.fetch_articles.side_effect = ApiException("API error 2")
        mock_categorizer.categorize_articles.return_value = []
        fetcher = NewsFetcher(
            api_repo=mock_api_repo,
            newsapi_service=mock_newsapi,
            thenewsapi_service=mock_thenewsapi,
            categorizer=mock_categorizer,
        )
        result = fetcher.fetch_all()
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
