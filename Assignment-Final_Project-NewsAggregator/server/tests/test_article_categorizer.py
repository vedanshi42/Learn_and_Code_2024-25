from server.models.article import Article
from server.utils.categorizer import ArticleCategorizer
from server.repositories.category_repository import CategoryRepository
from server.repositories.article_repository import ArticleRepository


class TestArticleCategorizerFlow:
    def setup_class(self):
        self.categorizer = ArticleCategorizer()
        self.article_repo = ArticleRepository()
        self.category_repo = CategoryRepository()

    def test_full_categorization_and_insert(self):
        article = Article(
            title="AI disrupting classrooms",
            content="Machine learning and neural networks in education",
            category=None,
            source_url="https://example.com/ml-news",
            date_published="2025-06-18T10:00:00Z"
        )

        # Categorize
        categorized = self.categorizer.categorize_articles([article])[0]
        assert categorized.category == "Technology"

        # Ensure category is now in DB
        self.category_repo.add_if_not_exists(categorized.category)

        # Insert into articles
        result = self.article_repo.insert_if_new(categorized)
        assert result in [True, False]  # Could be False if re-running test
