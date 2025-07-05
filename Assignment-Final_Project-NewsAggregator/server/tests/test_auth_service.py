import unittest
from unittest.mock import MagicMock
from server.services.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.service = AuthService()

    def test_signup_success(self):
        mock_user_repo = MagicMock()
        mock_password = MagicMock()
        mock_user_repo.email_exists.return_value = False
        mock_password.hash_password.return_value = "hashed"
        mock_user_repo.create_user.return_value = {"id": 1}
        service = AuthService(user_repo=mock_user_repo, password_service=mock_password)
        result = service.signup("user", "email", "pass")
        self.assertEqual(result, {"id": 1})

    def test_signup_user_exists(self):
        mock_user_repo = MagicMock()
        mock_user_repo.email_exists.return_value = True
        service = AuthService(user_repo=mock_user_repo)
        with self.assertRaises(ValueError):
            service.signup("user", "email", "pass")

    def test_login_success(self):
        mock_user_repo = MagicMock()
        mock_password = MagicMock()
        mock_user_repo.get_user_by_email.return_value = {"password": "hashed"}
        mock_password.verify_password.return_value = True
        service = AuthService(user_repo=mock_user_repo, password_service=mock_password)
        result = service.login("email", "pass")
        self.assertEqual(result, {"password": "hashed"})

    def test_login_invalid(self):
        mock_user_repo = MagicMock()
        mock_password = MagicMock()
        mock_user_repo.get_user_by_email.return_value = {"password": "hashed"}
        mock_password.verify_password.return_value = False
        service = AuthService(user_repo=mock_user_repo, password_service=mock_password)
        with self.assertRaises(ValueError):
            service.login("email", "pass")

    def test_signup_repo_exception(self):
        mock_user_repo = MagicMock()
        mock_user_repo.email_exists.side_effect = Exception("DB error")
        service = AuthService(user_repo=mock_user_repo)
        with self.assertRaises(Exception):
            service.signup("user", "email", "pass")

    def test_login_repo_exception(self):
        mock_user_repo = MagicMock()
        mock_password = MagicMock()
        mock_user_repo.get_user_by_email.side_effect = Exception("DB error")
        service = AuthService(user_repo=mock_user_repo, password_service=mock_password)
        with self.assertRaises(Exception):
            service.login("email", "pass")

    def test_signup_empty_fields(self):
        service = AuthService()
        with self.assertRaises(Exception):
            service.signup("", "", "")

    def test_login_empty_fields(self):
        service = AuthService()
        with self.assertRaises(ValueError):
            service.login("", "")


if __name__ == "__main__":
    unittest.main()
