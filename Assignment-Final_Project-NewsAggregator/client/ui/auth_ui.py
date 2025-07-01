from client.services.client_api import ClientAPIService


class AuthUI:
    def __init__(self):
        self.client = ClientAPIService()

    def login(self):
        user_email = input("Email: ")
        user_password = input("Password: ")
        user = self.client.login(user_email, user_password)
        if user:
            print("Login successful")
            return user
        print("Login failed.")
        return None

    def signup(self):
        user_name = input("Name: ")
        user_email = input("Email: ")
        user_password = input("Password: ")
        user = self.client.signup(user_name, user_email, user_password)
        if user:
            print("Signup successful")
            return user
        print("Signup failed.")
        return None
