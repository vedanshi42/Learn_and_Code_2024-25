import unittest
from unittest.mock import patch
from server.services.article_service import ArticleService


class TestArticleService(unittest.TestCase):
    def setUp(self):
        self.service = ArticleService()

    @patch("server.services.article_service.ArticleRepository")
    def test_get_headlines(self, mock_repo):
        mock_repo.return_value.get_filtered_articles.return_value = ["article1"]
        self.service.article_repo = mock_repo.return_value
        result = self.service.get_headlines()
        self.assertEqual(result, ["article1"])

    @patch("server.services.article_service.UserSavedArticleRepository")
    def test_save_article(self, mock_repo):
        self.service.save_repo = mock_repo.return_value
        self.service.save_article(1, 2)
        mock_repo.return_value.save_by_id.assert_called_with(1, 2)

    @patch("server.services.article_service.FeedbackService")
    def test_like_article(self, mock_repo):
        self.service.feedback_repo = mock_repo.return_value
        self.service.like_article(1, 2)
        mock_repo.return_value.like_article.assert_called_with(1, 2)

    @patch("server.services.article_service.FeedbackService")
    def test_dislike_article(self, mock_repo):
        self.service.feedback_repo = mock_repo.return_value
        self.service.dislike_article(1, 2)
        mock_repo.return_value.dislike_article.assert_called_with(1, 2)

    @patch("server.services.article_service.ReportingService")
    def test_report_article(self, mock_repo):
        self.service.report_repo = mock_repo.return_value
        self.service.report_article(1, 2)
        mock_repo.return_value.report_article.assert_called_with(1, 2)

    @patch("server.services.article_service.ArticleRepository")
    def test_get_recommended_articles(self, mock_repo):
        mock_repo.return_value.get_recommended_articles.return_value = ["rec1"]
        self.service.article_repo = mock_repo.return_value
        result = self.service.get_recommended_articles(1)
        self.assertEqual(result, ["rec1"])


if __name__ == "__main__":
    unittest.main()
