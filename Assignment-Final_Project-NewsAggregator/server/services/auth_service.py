from server.repositories.user_repository import UserRepository
from server.utils.hasher import PasswordService
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger
from server.interfaces.services_interfaces.i_auth_service_interface import IAuthService


class AuthService(IAuthService):
    def __init__(self, user_repo=None, password_service=None):
        self.user_repo = user_repo or UserRepository()
        self.password_service = password_service or PasswordService()

    def signup(self, username: str, email: str, password: str):
        try:
            if self.user_repo.email_exists(email):
                raise ValueError("User already exists with that email")
            hashed = self.password_service.hash_password(password)
            return self.user_repo.create_user(username, email, hashed)
        except RepositoryException as e:
            news_agg_logger(40, f"Signup failed for {email}: {e}")
            raise
        except Exception as e:
            news_agg_logger(40, f"Signup failed for {email}: {e}")
            raise

    def login(self, email: str, password: str):
        if not email or not password:
            raise ValueError("Email and password must not be empty.")
        try:
            user = self.user_repo.get_user_by_email(email)
            if user and self.password_service.verify_password(
                password, user["password"]
            ):
                return user
            else:
                raise ValueError("Invalid email or password")
        except Exception as e:
            news_agg_logger(40, f"Login failed for {email}: {e}")
            raise
