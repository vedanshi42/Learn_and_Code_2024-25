import unittest
from unittest.mock import MagicMock
from server.services.personalization_service import PersonalizationService


class TestPersonalizationService(unittest.TestCase):
    def setUp(self):
        # Default real service, can be overridden in each test
        self.service = PersonalizationService()

    def test_get_and_score_recommended_articles(self):
        mock_article_repo = MagicMock()
        mock_pref_repo = MagicMock()
        mock_scorer_cls = MagicMock()
        mock_scorer = MagicMock()

        mock_article_repo.get_recommended_articles.return_value = [{"id": 1}]
        mock_pref_repo.get_liked_categories.return_value = ["cat"]
        mock_pref_repo.get_disliked_categories.return_value = []
        mock_pref_repo.get_liked_keywords.return_value = ["kw"]
        mock_pref_repo.get_disliked_keywords.return_value = []

        mock_scorer_cls.return_value = mock_scorer
        mock_scorer.score.return_value = 5
        service = PersonalizationService(
            pref_repo=mock_pref_repo,
            article_repo=mock_article_repo,
            scorer_cls=mock_scorer_cls,
        )
        # Use real score_articles logic
        result = service.get_and_score_recommended_articles(1)
        self.assertTrue(result[0]["score"] == 5)

    def test_score_articles(self):
        mock_pref_repo = MagicMock()
        mock_scorer_cls = MagicMock()
        mock_scorer = MagicMock()

        mock_pref_repo.get_liked_categories.return_value = ["cat"]
        mock_pref_repo.get_disliked_categories.return_value = []
        mock_pref_repo.get_liked_keywords.return_value = ["kw"]
        mock_pref_repo.get_disliked_keywords.return_value = []

        mock_scorer_cls.return_value = mock_scorer
        mock_scorer.score.return_value = 2
        service = PersonalizationService(
            pref_repo=mock_pref_repo,
            scorer_cls=mock_scorer_cls,
        )
        articles = [{"id": 1}]
        result = service.score_articles(1, articles)
        self.assertTrue(all("score" in a for a in result))

    def test_get_and_score_recommended_articles_empty(self):
        mock_article_repo = MagicMock()
        mock_article_repo.get_recommended_articles.return_value = []
        service = PersonalizationService(article_repo=mock_article_repo)
        service.score_articles = lambda user_id, articles: []
        result = service.get_and_score_recommended_articles(1)
        self.assertEqual(result, [])

    def test_get_and_score_recommended_articles_exception(self):
        mock_article_repo = MagicMock()
        mock_article_repo.get_recommended_articles.side_effect = Exception("DB error")
        service = PersonalizationService(article_repo=mock_article_repo)
        with self.assertRaises(Exception):
            service.get_and_score_recommended_articles(1)

    def test_score_articles_pref_exception(self):
        mock_pref_repo = MagicMock()
        mock_pref_repo.get_liked_categories.side_effect = Exception("DB error")
        service = PersonalizationService(pref_repo=mock_pref_repo)
        with self.assertRaises(Exception):
            service.score_articles(1, [{"id": 1}])

    def test_score_articles_empty(self):
        mock_pref_repo = MagicMock()
        service = PersonalizationService(pref_repo=mock_pref_repo)
        result = service.score_articles(1, [])
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
