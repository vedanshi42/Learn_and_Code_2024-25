import requests


class SearchClient:
    BASE_URL = "http://localhost:8000"

    def search_articles(self, category=None, keyword=None, date=None):
        try:
            params = {}
            if category:
                params["category"] = category
            if keyword:
                params["keyword"] = keyword
            if date:
                params["date"] = date
            res = requests.get(f"{self.BASE_URL}/articles", params=params)
            return res.json() if res.ok else {"error": res.json().get("detail", "Failed to search articles")}
        except Exception as e:
            return {"error": str(e)}
