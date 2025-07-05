from server.models.article import Article
from server.repositories.category_repository import CategoryRepository
from server.machine_learning.ml_category_predictor import MLCategoryPredictor
from server.config.logging_config import news_agg_logger


class ArticleCategorizer:
    def __init__(self):
        self.predictor = MLCategoryPredictor()
        self.category_repo = CategoryRepository()

    def categorize_articles(self, articles: list[Article]):
        try:
            for article in articles:
                article.category = self.predictor.predict(article)
                self.category_repo.add_if_not_exists(article.category)
            return articles
        except Exception as e:
            news_agg_logger(40, f"Article categorization failed: {e}")
            raise
