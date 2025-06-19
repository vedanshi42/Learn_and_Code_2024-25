from server.models.article import Article
from server.repositories.category_repository import CategoryRepository
from server.services.ml_category_predictor import MLCategoryPredictor


class ArticleCategorizer:
    def __init__(self):
        self.predictor = MLCategoryPredictor()
        self.category_repo = CategoryRepository()

    def categorize_articles(self, articles: list[Article]) -> list[Article]:
        for article in articles:
            article.category = self.predictor.predict(article)
            self.category_repo.add_if_not_exists(article.category)
        return articles
