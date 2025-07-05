import requests


class SavedArticleClient:
    BASE_URL = "http://localhost:8000"

    def get_saved_articles(self, user_id):
        try:
            result = requests.get(f"{self.BASE_URL}/users/{user_id}/saved-articles")
            return (
                result.json()
                if result.ok
                else {
                    "error": result.json().get("detail", "Failed to fetch saved articles")
                }
            )
        except Exception as e:
            return {"error": str(e)}

    def delete_saved_article(self, user_id, article_id):
        try:
            result = requests.delete(
                f"{self.BASE_URL}/users/{user_id}/saved-articles/{article_id}"
            )
            return (
                result.json()
                if result.ok
                else {
                    "error": result.json().get("detail", "Failed to delete saved article")
                }
            )
        except Exception as e:
            return {"error": str(e)}
