from server.repositories.user_preference_repository import UserPreferenceRepository
from server.services.article_scoring_service import ArticleScorer


class PersonalizationService:
    def __init__(self):
        self.pref_repo = UserPreferenceRepository()

    def score_articles(self, user_id: int, articles: list[dict]) -> list[dict]:
        cats = self.pref_repo.get_liked_categories(user_id)
        keywords = self.pref_repo.get_enabled_keywords(user_id)
        disliked_kw, disliked_urls = self.pref_repo.get_disliked_keywords_and_urls(user_id)

        scorer = ArticleScorer(cats, keywords, disliked_kw, disliked_urls)

        for article in articles:
            article["score"] = scorer.score(article)

        return [a for a in sorted(articles, key=lambda x: x["score"], reverse=True) if a["score"] > -3]
