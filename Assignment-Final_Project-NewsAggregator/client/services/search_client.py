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
            result = requests.get(f"{self.BASE_URL}/articles", params=params)
            return (
                result.json()
                if result.ok
                else {"error": result.json().get("detail", "Failed to search articles")}
            )
        except Exception as e:
            return {"error": str(e)}
