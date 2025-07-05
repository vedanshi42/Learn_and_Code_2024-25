from .base_api_service import BaseAPIService
from server.models.article import Article
from datetime import datetime


class TheNewsAPIService(BaseAPIService):
    def fetch_articles(self):
        params = {
            "q": "search_fields=title,description,url",
            "language": "en",
            "api_token": self.api_key}
        data = self.get("/v1/news/top", params)

        return [
            Article(
                title=article["title"],
                content=article.get("description", ""),
                source_url=article["url"],
                date_published=datetime.fromisoformat(article["published_at"].replace("Z", "+00:00")),
                category=article.get("category")
            )
            for article in data.get("data", []) if article.get("title") and article.get("url")
        ]
