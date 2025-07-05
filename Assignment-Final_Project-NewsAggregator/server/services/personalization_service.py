from server.repositories.user_preference_repository import UserPreferenceRepository
from server.repositories.article_repository import ArticleRepository
from server.utils.scorer import ArticleScorer
from server.config.logging_config import news_agg_logger
from server.interfaces.services_interfaces.i_personalization_service_interface import IPersonalizationService


class PersonalizationService(IPersonalizationService):
    def __init__(self, pref_repo=None, article_repo=None, scorer_cls=None):
        self.pref_repo = pref_repo or UserPreferenceRepository()
        self.article_repo = article_repo or ArticleRepository()
        self.scorer_cls = scorer_cls or ArticleScorer

    def get_and_score_recommended_articles(self, user_id: int):
        try:
            articles = self.article_repo.get_recommended_articles(user_id)
            return self.score_articles(user_id, articles)
        except Exception as e:
            news_agg_logger.error(
                f"Error fetching or scoring recommended articles for user_id={user_id}: {e}"
            )
            raise Exception(f"Failed to get or score recommended articles: {e}")

    def score_articles(self, user_id: int, articles: list[dict]):
        try:
            liked_categories = self.pref_repo.get_liked_categories(user_id)
            disliked_categories = self.pref_repo.get_disliked_categories(user_id)
            liked_keywords = self.pref_repo.get_liked_keywords(user_id)
            disliked_keywords = self.pref_repo.get_disliked_keywords(user_id)
        except Exception as e:
            news_agg_logger.error(
                f"Error fetching user preferences for user_id={user_id}: {e}"
            )
            raise Exception(f"Failed to fetch user preferences for scoring: {e}")

        scorer = self.scorer_cls(
            liked_categories,
            liked_keywords,
            disliked_keywords,
            disliked_categories=disliked_categories,
        )

        for article in articles:
            article["score"] = scorer.score(article)

        return [
            a
            for a in sorted(articles, key=lambda x: x["score"], reverse=True)
            if a["score"] > -3
        ]
