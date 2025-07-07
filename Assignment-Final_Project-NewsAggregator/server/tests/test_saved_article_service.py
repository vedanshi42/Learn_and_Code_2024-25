import unittest
from unittest.mock import MagicMock
from server.services.saved_article_service import SavedArticleService


class TestSavedArticleService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = SavedArticleService(repo=self.mock_repo)

    def test_get_saved_articles(self):
        self.mock_repo.get_saved_articles.return_value = ["a1", "a2"]
        result = self.service.get_saved_articles(1)
        self.mock_repo.get_saved_articles.assert_called_with(1)
        self.assertEqual(result, ["a1", "a2"])

    def test_get_saved_articles_exception(self):
        self.mock_repo.get_saved_articles.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.get_saved_articles(1)

    def test_delete_saved_article(self):
        self.service.delete_saved_article(1, 2)
        self.mock_repo.delete_by_id.assert_called_with(1, 2)

    def test_delete_saved_article_exception(self):
        self.mock_repo.delete_by_id.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.delete_saved_article(1, 2)


if __name__ == "__main__":
    unittest.main()
