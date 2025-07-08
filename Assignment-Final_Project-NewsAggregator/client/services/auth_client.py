import requests


class AuthClient:
    BASE_URL = "http://localhost:8000"

    def login(self, email, password):
        try:
            result = requests.post(
                f"{self.BASE_URL}/auth/login",
                json={"email": email, "password": password},
            )
            return (
                result.json()
                if result.ok
                else {"error": result.json().get("detail", "Login failed")}
            )
        except Exception as e:
            return {"error": str(e)}

    def signup(self, username, email, password):
        try:
            result = requests.post(
                f"{self.BASE_URL}/auth/signup",
                json={"username": username, "email": email, "password": password},
            )
            return (
                result.json()
                if result.ok
                else {"error": result.json().get("detail", "Signup failed")}
            )
        except Exception as e:
            return {"error": str(e)}
