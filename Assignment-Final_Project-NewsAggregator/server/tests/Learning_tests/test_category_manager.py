from server.models.article import Article
from server.services.news_categorizing_service import ArticleCategorizer


class TestArticleCategorizer:
    def setup_class(self):
        self.categorizer = ArticleCategorizer()

    def test_assign_known_category(self):
        article = Article(
            title="The AI revolution in education",
            content="New advancements in neural networks...",
            category=None,
            source_url="https://example.com/ai-news",
            date_published="2025-06-17T10:00:00Z"
        )
        category = self.categorizer.categorize(article)
        assert category == "Technology"

    def test_fallback_to_uncategorized(self):
        article = Article(
            title="A random event",
            content="Nothing matches our keywords here",
            category=None,
            source_url="https://example.com/random-news",
            date_published="2025-06-17T10:00:00Z"
        )
        category = self.categorizer.categorize(article)
        assert category == "Uncategorized"
