from server.repositories.user_repository import UserRepository
from server.utils.hasher import PasswordService


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.password_service = PasswordService()

    def signup(self, username: str, email: str, password: str):
        if self.user_repo.email_exists(email):
            raise ValueError("User already exists with that email")
        hashed = self.password_service.hash_password(password)
        return self.user_repo.create_user(username, email, hashed)

    def login(self, email: str, password: str):
        user = self.user_repo.get_user_by_email(email)
        if user and self.password_service.verify_password(password, user['password']):
            return user['user_id']
        else:
            raise ValueError("Invalid email or password")
