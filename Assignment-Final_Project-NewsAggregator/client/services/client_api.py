import requests


class ClientAPIService:
    BASE_URL = "http://localhost:8000"

    def login(self, email, password):
        res = requests.post(f"{self.BASE_URL}/auth/login", json={"email": email, "password": password})
        return res.json() if res.ok else {"error": res.json().get("detail", "Login failed")}

    def signup(self, username, email, password):
        res = requests.post(f"{self.BASE_URL}/auth/signup", json={
            "username": username, "email": email, "password": password
        })
        return res.json() if res.ok else {"error": res.json().get("detail", "Signup failed")}

    # Admin performed actions
    def get_external_statuses(self):
        return requests.get(f"{self.BASE_URL}/admin/external-statuses").json()

    def get_external_keys(self):
        return requests.get(f"{self.BASE_URL}/admin/external-keys").json()

    def update_api_key(self, api_name, new_key):
        return requests.post(f"{self.BASE_URL}/admin/update-key", json={"api_name": api_name, "api_key": new_key})

    def add_category(self, name):
        return requests.post(f"{self.BASE_URL}/admin/add-category", json={"name": name})

    def disable_category(self, name):
        return requests.post(f"{self.BASE_URL}/admin/disable-category", json={"name": name})

    def disable_keyword(self, word):
        return requests.post(f"{self.BASE_URL}/admin/disable-keyword", json={"word": word})

    def delete_article(self, article_id):
        return requests.delete(f"{self.BASE_URL}/admin/delete-article/{article_id}")

    def get_all_categories(self):
        return requests.get(f"{self.BASE_URL}/admin/categories").json()

    def get_all_keywords(self):
        return requests.get(f"{self.BASE_URL}/admin/keywords").json()

    def get_reported_articles(self):
        return requests.get(f"{self.BASE_URL}/admin/reported-articles").json()

    # News Article related actions
    def fetch_headlines(self, filter_by=None, sort_by=None, user_id=None):
        params = {}
        if filter_by:
            params["filter_by"] = filter_by
        if sort_by:
            params["sort_by"] = sort_by

        params["user_id"] = user_id
        res = requests.get(f"{self.BASE_URL}/headlines", params=params)
        return res.json() if res.ok else []

    def get_recommended_articles(self, user_id):
        res = requests.get(f"{self.BASE_URL}/recommended", params={"user_id": user_id})
        return res.json() if res.ok else []

    def save_article(self, user_id, article_id):
        requests.post(f"{self.BASE_URL}/save", json={"user_id": user_id, "article_id": article_id})

    def like_article(self, user_id, article_id):
        requests.post(f"{self.BASE_URL}/like", json={"user_id": user_id, "article_id": article_id})

    def dislike_article(self, user_id, article_id):
        requests.post(f"{self.BASE_URL}/dislike", json={"user_id": user_id, "article_id": article_id})

    def report_article(self, user_id, article_id):
        requests.post(f"{self.BASE_URL}/report", json={"user_id": user_id, "article_id": article_id})

    # --- Saved Articles ---
    def get_saved_articles(self, user_id):
        res = requests.get(f"{self.BASE_URL}/saved/{user_id}")
        return res.json() if res.ok else {}

    def delete_saved_article(self, user_id, article_id):
        requests.delete(f"{self.BASE_URL}/saved/{user_id}/{article_id}")

    # --- Search Articles ---
    def search_articles_by_category(self, category):
        res = requests.get(f"{self.BASE_URL}/search/category", params={"category": category})
        return res.json() if res.ok else {}

    def search_articles_by_keyword(self, keyword):
        res = requests.get(f"{self.BASE_URL}/search/keyword", params={"keyword": keyword})
        return res.json() if res.ok else {}

    def search_articles_by_date(self, date_str):
        res = requests.get(f"{self.BASE_URL}/search/date", params={"date": date_str})
        return res.json() if res.ok else {}

    # --- Notifications ---
    def get_user_notifications(self, email):
        res = requests.get(f"{self.BASE_URL}/notifications/{email}")
        return res.json() if res.ok else []

    def get_user_categories(self, email):
        res = requests.get(f"{self.BASE_URL}/notifications/categories/{email}")
        return res.json() if res.ok else []

    def get_user_keywords(self, email):
        res = requests.get(f"{self.BASE_URL}/notifications/keywords/{email}")
        return res.json() if res.ok else []

    def toggle_category(self, email, category):
        return requests.post(f"{self.BASE_URL}/notifications/categories/toggle", json={"email": email, "category": category})

    def toggle_keyword(self, email, keyword):
        return requests.post(f"{self.BASE_URL}/notifications/keywords/toggle", json={"email": email, "keyword": keyword})

    def add_category_for_user(self, email, category):
        return requests.post(f"{self.BASE_URL}/notifications/categories/add", json={"email": email, "category": category})

    def add_keyword_for_user(self, email, keyword):
        return requests.post(f"{self.BASE_URL}/notifications/keywords/add", json={"email": email, "keyword": keyword})
