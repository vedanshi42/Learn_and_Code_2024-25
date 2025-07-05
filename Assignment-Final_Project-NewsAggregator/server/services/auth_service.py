from server.repositories.user_repository import UserRepository
from server.utils.hasher import PasswordService
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.password_service = PasswordService()

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
        try:
            user = self.user_repo.get_user_by_email(email)
            if user and self.password_service.verify_password(password, user['password']):
                return user
            else:
                raise ValueError("Invalid email or password")
        except RepositoryException as e:
            news_agg_logger(40, f"Login failed for {email}: {e}")
            raise
        except Exception as e:
            news_agg_logger(40, f"Login failed for {email}: {e}")
            raise
