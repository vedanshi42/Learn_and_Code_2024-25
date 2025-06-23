from .base_api_service import BaseAPIService
from server.models.article import Article
from datetime import datetime


class TheNewsAPIService(BaseAPIService):
    def fetch_top_news(self):
        params = {
            "q": "search_fields=title,description,url",
            "language": "en",
            "api_token": self.api_key}
        data = self.get("/v1/news/top", params)

        return [
            Article(
                title=a["title"].encode("utf-8", errors="ignore").decode("utf-8"),
                content=a.get("description", "").encode("utf-8", errors="ignore").decode("utf-8"),
                source_url=a["url"].encode("utf-8", errors="ignore").decode("utf-8"),
                date_published=datetime.fromisoformat(a["published_at"].replace("Z", "+00:00")),
                category=a.get("category").encode("utf-8", errors="ignore").decode("utf-8")
            )
            for a in data.get("data", []) if a.get("title") and a.get("url")
        ]
