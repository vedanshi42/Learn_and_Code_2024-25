import requests


class NotificationClient:
    BASE_URL = "http://localhost:8000"

    def send_all_user_notifications(self):
        try:
            res = requests.post(f"{self.BASE_URL}/users/notifications/send")
            return (
                res.json()
                if res.ok
                else {"error": res.json().get("detail", "Failed to send notifications")}
            )
        except Exception as e:
            return {"error": str(e)}

    def get_user_notifications(self, user_id):
        try:
            res = requests.get(f"{self.BASE_URL}/users/{user_id}/notifications")
            return (
                res.json()
                if res.ok
                else {
                    "error": res.json().get("detail", "Failed to fetch notifications")
                }
            )
        except Exception as e:
            return {"error": str(e)}

    def get_user_categories(self, user_id):
        try:
            res = requests.get(f"{self.BASE_URL}/users/{user_id}/categories")
            return (
                res.json()
                if res.ok
                else {
                    "error": res.json().get("detail", "Failed to fetch user categories")
                }
            )
        except Exception as e:
            return {"error": str(e)}

    def add_category_for_user(self, user_id, category):
        try:
            res = requests.post(
                f"{self.BASE_URL}/users/{user_id}/categories",
                json={"user_id": user_id, "category": category},
            )
            return (
                res.json()
                if res.ok
                else {"error": res.json().get("detail", "Failed to add category")}
            )
        except Exception as e:
            return {"error": str(e)}

    def toggle_category(self, user_id, category):
        try:
            res = requests.patch(
                f"{self.BASE_URL}/users/{user_id}/categories/{category}"
            )
            return (
                res.json()
                if res.ok
                else {"error": res.json().get("detail", "Failed to toggle category")}
            )
        except Exception as e:
            return {"error": str(e)}

    def get_user_keywords(self, user_id):
        try:
            res = requests.get(f"{self.BASE_URL}/users/{user_id}/keywords")
            return (
                res.json()
                if res.ok
                else {
                    "error": res.json().get("detail", "Failed to fetch user keywords")
                }
            )
        except Exception as e:
            return {"error": str(e)}

    def add_keyword_for_user(self, user_id, keyword):
        try:
            res = requests.post(
                f"{self.BASE_URL}/users/{user_id}/keywords",
                json={"user_id": user_id, "keyword": keyword},
            )
            return (
                res.json()
                if res.ok
                else {"error": res.json().get("detail", "Failed to add keyword")}
            )
        except Exception as e:
            return {"error": str(e)}

    def toggle_keyword(self, user_id, keyword):
        try:
            res = requests.patch(f"{self.BASE_URL}/users/{user_id}/keywords/{keyword}")
            return (
                res.json()
                if res.ok
                else {"error": res.json().get("detail", "Failed to toggle keyword")}
            )
        except Exception as e:
            return {"error": str(e)}
