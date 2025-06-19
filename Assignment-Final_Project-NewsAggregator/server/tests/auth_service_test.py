import pytest
from unittest.mock import MagicMock
from server.services.auth_service import AuthService


class TestAuthService:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.auth_service = AuthService(user_repo=self.mock_repo)

    def test_signup_success(self):
        self.mock_repo.find_by_email.return_value = None
        self.mock_repo.create_user.return_value = 1
        result = self.auth_service.signup("user", "email@example.com", "pass")
        assert result == 1

    def test_signup_duplicate_email(self):
        self.mock_repo.find_by_email.return_value = {"email": "email@example.com"}
        with pytest.raises(Exception, match="Email already registered"):
            self.auth_service.signup("user", "email@example.com", "pass")

    def test_login_success(self):
        import bcrypt
        hashed_pw = bcrypt.hashpw("pass".encode(), bcrypt.gensalt()).decode()
        self.mock_repo.find_by_email.return_value = {"email": "email@example.com", "password": hashed_pw}
        user = self.auth_service.login("email@example.com", "pass")
        assert user["email"] == "email@example.com"

    def test_login_user_not_found(self):
        self.mock_repo.find_by_email.return_value = None
        with pytest.raises(Exception, match="User not found"):
            self.auth_service.login("noone@example.com", "pass")

    def test_login_wrong_password(self):
        import bcrypt
        hashed_pw = bcrypt.hashpw("pass".encode(), bcrypt.gensalt()).decode()
        self.mock_repo.find_by_email.return_value = {"email": "email@example.com", "password": hashed_pw}
        with pytest.raises(Exception, match="Invalid credentials"):
            self.auth_service.login("email@example.com", "wrongpass")
