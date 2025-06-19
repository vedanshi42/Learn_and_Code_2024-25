from server.services.auth_service import AuthService


class AuthUI:
    def __init__(self):
        self.service = AuthService()

    def login(self):
        email = input("Email: ")
        pwd = input("Password: ")
        try:
            return self.service.login(email, pwd)
        except Exception as e:
            print(e)
            return None

    def signup(self):
        name = input("Name: ")
        email = input("Email: ")
        pwd = input("Password: ")
        try:
            return self.service.signup(name, email, pwd)
        except Exception as e:
            print(e)
            return None
