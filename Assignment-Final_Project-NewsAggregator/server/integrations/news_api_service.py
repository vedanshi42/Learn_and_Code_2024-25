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
                title=a["title"],
                content=a.get("description", ""),
                source_url=a["url"],
                date_published=datetime.fromisoformat(a["publishedAt"].replace("Z", "+00:00")),
                category=a.get("category")
            )
            for a in data.get("articles", []) if a.get("title") and a.get("url")
        ]
