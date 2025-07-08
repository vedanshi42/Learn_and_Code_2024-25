from .base_api_service import BaseAPIService
from server.models.article import Article
from datetime import datetime


class NewsAPIService(BaseAPIService):
    def fetch_articles(self, from_date, to_date):
        params = {
            "q": "language=en",
            "from": from_date,
            "to": to_date,
            "sortBy": "publishedAt",
            "apiKey": self.api_key
        }
        data = self.get("/v2/everything", params)
        return [
            Article(
                title=article["title"],
                content=article.get("description", ""),
                source_url=article["url"],
                date_published=datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00")),
                category=article.get("category")
            )
            for article in data.get("articles", []) if article.get("title") and article.get("url")
        ]
