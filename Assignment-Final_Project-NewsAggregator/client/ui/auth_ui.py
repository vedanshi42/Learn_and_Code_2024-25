from client.helpers.ui_helpers import UIHelpers
from client.services.auth_client import AuthClient


class AuthUI:
    def __init__(self):
        self.client = AuthClient()

    def login(self):
        user_email = input("Email: ")
        user_password = UIHelpers.get_hidden_password("Password: ")

        user = self.client.login(user_email, user_password)

        if user and "error" not in user:
            print(f"Login successful for {user_email}")
            return user

        print(f"Login failed: {user.get('error')}")
        return None

    def signup(self):
        user_name = input("Name: ")
        while True:
            user_email = input("Email: ")

            if UIHelpers.is_valid_email(user_email):
                break

            print(
                "Invalid email format. Please enter a valid email (e.g. user@example.com)."
            )

        user_password = UIHelpers.get_hidden_password("Password: ")
        user = self.client.signup(user_name, user_email, user_password)

        if user and "error" not in user:
            print("Signup successful")
            return user

        print(f"Signup failed: {user.get('error')}")
        return None
