import requests


class AdminClient:
    BASE_URL = "http://localhost:8000"

    def get_external_keys(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/admin/external-keys")
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def add_or_update_api_key(self, api_name, new_key):
        try:
            resp = requests.post(f"{self.BASE_URL}/admin/api-keys", json={"api_name": api_name, "api_key": new_key})
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_all_categories(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/admin/categories")
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def add_category(self, name):
        try:
            resp = requests.post(f"{self.BASE_URL}/admin/categories", json={"name": name})
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def disable_category(self, category_name):
        try:
            resp = requests.patch(f"{self.BASE_URL}/admin/categories/{category_name}")
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_all_keywords(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/admin/keywords")
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def disable_keyword(self, keyword):
        try:
            resp = requests.patch(f"{self.BASE_URL}/admin/keywords/{keyword}")
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_reported_articles(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/admin/reported-articles")
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def delete_article(self, article_id, user_id=None):
        try:
            resp = requests.delete(f"{self.BASE_URL}/admin/articles/{article_id}", json={"user_id": user_id} if user_id is not None else None)
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_external_statuses(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/admin/external-statuses")
            try:
                data = resp.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not resp.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {resp.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}
