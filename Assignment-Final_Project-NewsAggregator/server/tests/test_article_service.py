import unittest
from unittest.mock import MagicMock
from server.services.article_service import ArticleService


class TestArticleService(unittest.TestCase):
    def setUp(self):
        self.service = ArticleService()

    def test_get_headlines(self):
        mock_repo = MagicMock()
        mock_repo.get_filtered_articles.return_value = ["article1"]
        service = ArticleService(article_repo=mock_repo)
        result = service.get_headlines()
        self.assertEqual(result, ["article1"])

    def test_save_article(self):
        mock_repo = MagicMock()
        service = ArticleService(save_repo=mock_repo)
        service.save_article(1, 2)
        mock_repo.save_by_id.assert_called_with(1, 2)

    def test_like_article(self):
        mock_repo = MagicMock()
        service = ArticleService(feedback_repo=mock_repo)
        service.like_article(1, 2)
        mock_repo.like_article.assert_called_with(1, 2)

    def test_dislike_article(self):
        mock_repo = MagicMock()
        service = ArticleService(feedback_repo=mock_repo)
        service.dislike_article(1, 2)
        mock_repo.dislike_article.assert_called_with(1, 2)

    def test_report_article(self):
        mock_repo = MagicMock()
        service = ArticleService(report_repo=mock_repo)
        service.report_article(1, 2)
        mock_repo.report_article.assert_called_with(1, 2)

    def test_get_recommended_articles(self):
        mock_repo = MagicMock()
        mock_repo.get_recommended_articles.return_value = ["rec1"]
        service = ArticleService(article_repo=mock_repo)
        result = service.get_recommended_articles(1)
        self.assertEqual(result, ["rec1"])

    def test_get_headlines_empty(self):
        mock_repo = MagicMock()
        mock_repo.get_filtered_articles.return_value = []
        service = ArticleService(article_repo=mock_repo)
        result = service.get_headlines()
        self.assertEqual(result, [])

    def test_get_headlines_exception(self):
        mock_repo = MagicMock()
        mock_repo.get_filtered_articles.side_effect = Exception("DB error")
        service = ArticleService(article_repo=mock_repo)
        with self.assertRaises(Exception):
            service.get_headlines()

    def test_save_article_exception(self):
        mock_repo = MagicMock()
        mock_repo.save_by_id.side_effect = Exception("DB error")
        service = ArticleService(save_repo=mock_repo)
        with self.assertRaises(Exception):
            service.save_article(1, 2)

    def test_like_article_exception(self):
        mock_repo = MagicMock()
        mock_repo.like_article.side_effect = Exception("DB error")
        service = ArticleService(feedback_repo=mock_repo)
        with self.assertRaises(Exception):
            service.like_article(1, 2)

    def test_dislike_article_exception(self):
        mock_repo = MagicMock()
        mock_repo.dislike_article.side_effect = Exception("DB error")
        service = ArticleService(feedback_repo=mock_repo)
        with self.assertRaises(Exception):
            service.dislike_article(1, 2)

    def test_report_article_exception(self):
        mock_repo = MagicMock()
        mock_repo.report_article.side_effect = Exception("DB error")
        service = ArticleService(report_repo=mock_repo)
        with self.assertRaises(Exception):
            service.report_article(1, 2)

    def test_get_recommended_articles_empty(self):
        mock_repo = MagicMock()
        mock_repo.get_recommended_articles.return_value = []
        service = ArticleService(article_repo=mock_repo)
        result = service.get_recommended_articles(1)
        self.assertEqual(result, [])

    def test_get_recommended_articles_exception(self):
        mock_repo = MagicMock()
        mock_repo.get_recommended_articles.side_effect = Exception("DB error")
        service = ArticleService(article_repo=mock_repo)
        with self.assertRaises(Exception):
            service.get_recommended_articles(1)


if __name__ == "__main__":
    unittest.main()
