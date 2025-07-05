from server.models.article import Article
from server.machine_learning.ml_category_predictor import MLCategoryPredictor


class TestMLCategoryPredictor:
    def setup_class(self):
        self.predictor = MLCategoryPredictor()

    def test_predict_technology_category(self):
        article = Article(
            title="OpenAI launches next-gen chatbot",
            content="AI and machine learning breakthrough changes everything.",
            category=None,
            source_url="https://example.com/ai-news",
            date_published="2025-06-18T10:00:00Z",
        )
        assert self.predictor.predict(article) == "Technology"

    def test_predict_unknown_fallback(self):
        article = Article(
            title="Mystery headline",
            content="Nothing here is obvious.",
            category=None,
            source_url="https://example.com/mystery",
            date_published="2025-06-18T10:00:00Z",
        )
        result = self.predictor.predict(article)
        assert isinstance(result, str)
