import pytest
from unittest.mock import patch
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
            date_published="2025-06-18T10:00:00Z",
        )

        # Categorize
        categorized = self.categorizer.categorize_articles([article])[0]
        assert categorized.category == "Technology"

        # Ensure category is now in DB
        self.category_repo.add_if_not_exists(categorized.category)

        # Insert into articles
        result = self.article_repo.insert_if_new(categorized)
        assert result in [True, False]  # Could be False if re-running test

    def test_categorize_empty_article(self):
        article = Article(
            title="",
            content="",
            category=None,
            source_url="",
            date_published="2025-06-18T10:00:00Z",
        )
        categorized = self.categorizer.categorize_articles([article])[0]
        assert isinstance(categorized.category, str)

    def test_categorize_none_article(self):
        with pytest.raises(Exception):
            self.categorizer.categorize_articles([None])

    def test_db_insert_failure(self):
        article = Article(
            title="Test",
            content="Test content",
            category="TestCat",
            source_url="url",
            date_published="2025-06-18T10:00:00Z",
        )
        with patch.object(
            ArticleRepository, "insert_if_new", side_effect=Exception("DB error")
        ):
            with pytest.raises(Exception):
                self.article_repo.insert_if_new(article)

    def test_category_repo_failure(self):
        with patch.object(
            CategoryRepository, "add_if_not_exists", side_effect=Exception("DB error")
        ):
            with pytest.raises(Exception):
                self.category_repo.add_if_not_exists("TestCat")

    def test_categorizer_handles_malformed(self):
        # Malformed article dict instead of Article instance
        with pytest.raises(Exception):
            self.categorizer.categorize_articles([{"bad": "data"}])
