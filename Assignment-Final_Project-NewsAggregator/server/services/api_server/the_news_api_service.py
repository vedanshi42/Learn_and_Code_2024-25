from .base_api_service import BaseAPIService
from server.models.article import Article
from datetime import datetime


class TheNewsAPIService(BaseAPIService):
    def fetch_top_news(self):
        params = {"api_token": self.api_key}
        data = self.get("/v1/news/top", params)

        return [
            Article(
                title=a["title"],
                content=a.get("description", ""),
                source_url=a["url"],
                date_published=datetime.fromisoformat(a["published_at"].replace("Z", "+00:00")),
                category=a.get("category")
            )
            for a in data.get("data", []) if a.get("title") and a.get("url")
        ]
