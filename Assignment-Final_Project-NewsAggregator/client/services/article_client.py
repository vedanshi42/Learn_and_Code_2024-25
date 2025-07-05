import requests


class ArticleClient:
    BASE_URL = "http://localhost:8000"

    def fetch_headlines(self, filter_by=None, sort_by=None, user_id=None):
        try:
            params = {}
            if filter_by:
                params["filter_by"] = filter_by
            if sort_by:
                params["sort_by"] = sort_by
            if user_id is not None:
                params["user_id"] = user_id
            res = requests.get(f"{self.BASE_URL}/articles/headlines", params=params)
            return res.json() if res.ok else {"error": res.json().get("detail", "Failed to fetch headlines")}
        except Exception as e:
            return {"error": str(e)}

    def get_recommended_articles(self, user_id):
        try:
            res = requests.get(f"{self.BASE_URL}/articles/recommended", params={"user_id": user_id})
            return res.json() if res.ok else {"error": res.json().get("detail", "Failed to fetch recommendations")}
        except Exception as e:
            return {"error": str(e)}

    def save_article(self, user_id, article_id):
        try:
            res = requests.post(f"{self.BASE_URL}/users/{user_id}/saved-articles", json={"user_id": user_id, "article_id": article_id})
            return res.json() if res.ok else {"error": res.json().get("detail", "Failed to save article")}
        except Exception as e:
            return {"error": str(e)}

    def like_article(self, user_id, article_id):
        try:
            res = requests.post(f"{self.BASE_URL}/articles/{article_id}/likes", json={"user_id": user_id, "article_id": article_id})
            return res.json() if res.ok else {"error": res.json().get("detail", "Failed to like article")}
        except Exception as e:
            return {"error": str(e)}

    def dislike_article(self, user_id, article_id):
        try:
            res = requests.post(f"{self.BASE_URL}/articles/{article_id}/dislikes", json={"user_id": user_id, "article_id": article_id})
            return res.json() if res.ok else {"error": res.json().get("detail", "Failed to dislike article")}
        except Exception as e:
            return {"error": str(e)}

    def report_article(self, user_id, article_id):
        try:
            res = requests.post(f"{self.BASE_URL}/articles/{article_id}/reports", json={"user_id": user_id, "article_id": article_id})
            return res.json() if res.ok else {"error": res.json().get("detail", "Failed to report article")}
        except Exception as e:
            return {"error": str(e)}
