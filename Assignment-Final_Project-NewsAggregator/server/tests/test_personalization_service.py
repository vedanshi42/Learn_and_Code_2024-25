import unittest
from unittest.mock import patch, MagicMock
from server.services.personalization_service import PersonalizationService


class TestPersonalizationService(unittest.TestCase):
    def setUp(self):
        self.service = PersonalizationService()

    @patch('server.services.personalization_service.ArticleRepository')
    @patch('server.services.personalization_service.UserPreferenceRepository')
    @patch('server.services.personalization_service.ArticleScorer')
    def test_get_and_score_recommended_articles(self, mock_scorer, mock_pref_repo, mock_article_repo):
        mock_article_repo.return_value.get_recommended_articles.return_value = [{'id': 1}]
        mock_pref_repo.return_value.get_liked_categories.return_value = ['cat']
        mock_pref_repo.return_value.get_disliked_categories.return_value = []
        mock_pref_repo.return_value.get_liked_keywords.return_value = ['kw']
        mock_pref_repo.return_value.get_disliked_keywords.return_value = []
        mock_scorer.return_value.score.return_value = 5

        self.service.article_repo = mock_article_repo.return_value
        self.service.pref_repo = mock_pref_repo.return_value
        self.service.score_articles = MagicMock(return_value=[{'id': 1, 'score': 5}])
        result = self.service.get_and_score_recommended_articles(1)
        self.assertEqual(result, [{'id': 1, 'score': 5}])

    @patch('server.services.personalization_service.ArticleScorer')
    @patch('server.services.personalization_service.UserPreferenceRepository')
    def test_score_articles(self, mock_pref_repo, mock_scorer):
        mock_pref_repo.return_value.get_liked_categories.return_value = ['cat']
        mock_pref_repo.return_value.get_disliked_categories.return_value = []
        mock_pref_repo.return_value.get_liked_keywords.return_value = ['kw']
        mock_pref_repo.return_value.get_disliked_keywords.return_value = []
        mock_scorer.return_value.score.return_value = 2
        self.service.pref_repo = mock_pref_repo.return_value
        articles = [{'id': 1}]
        with patch('server.services.personalization_service.ArticleScorer', mock_scorer):
            result = self.service.score_articles(1, articles)
        self.assertTrue(all('score' in a for a in result))


if __name__ == '__main__':
    unittest.main()
