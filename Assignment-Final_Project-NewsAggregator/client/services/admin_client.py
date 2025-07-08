import requests


class AdminClient:
    BASE_URL = "http://localhost:8000"

    def get_external_keys(self):
        try:
            response = requests.get(f"{self.BASE_URL}/admin/external-keys")
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def add_or_update_api_key(self, api_name, new_key):
        try:
            response = requests.post(
                f"{self.BASE_URL}/admin/api-keys",
                json={"api_name": api_name, "api_key": new_key},
            )
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_all_categories(self):
        try:
            response = requests.get(f"{self.BASE_URL}/admin/categories")
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def add_category(self, name):
        try:
            response = requests.post(
                f"{self.BASE_URL}/admin/categories", json={"name": name}
            )
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def disable_category(self, category_name):
        try:
            response = requests.patch(f"{self.BASE_URL}/admin/categories/{category_name}")
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_all_keywords(self):
        try:
            response = requests.get(f"{self.BASE_URL}/admin/keywords")
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def disable_keyword(self, keyword):
        try:
            response = requests.patch(f"{self.BASE_URL}/admin/keywords/{keyword}")
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_reported_articles(self):
        try:
            response = requests.get(f"{self.BASE_URL}/admin/reported-articles")
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def delete_article(self, article_id, user_id=None):
        try:
            response = requests.delete(
                f"{self.BASE_URL}/admin/articles/{article_id}",
                json={"user_id": user_id} if user_id is not None else None,
            )
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_external_statuses(self):
        try:
            response = requests.get(f"{self.BASE_URL}/admin/external-statuses")
            try:
                data = response.json()
            except Exception:
                data = {"error": "Invalid server response"}
            if not response.ok:
                if "detail" in data:
                    return {"error": data["detail"]}
                return {"error": f"HTTP {response.status_code}"}
            return data
        except Exception as e:
            return {"error": str(e)}
