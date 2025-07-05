import unittest
from unittest.mock import patch
from server.services.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.service = AuthService()

    @patch('server.services.auth_service.UserRepository')
    @patch('server.services.auth_service.PasswordService')
    def test_signup_success(self, mock_password, mock_user_repo):
        mock_user_repo.return_value.email_exists.return_value = False
        mock_password.return_value.hash_password.return_value = 'hashed'
        mock_user_repo.return_value.create_user.return_value = {'id': 1}
        self.service.user_repo = mock_user_repo.return_value
        self.service.password_service = mock_password.return_value
        result = self.service.signup('user', 'email', 'pass')
        self.assertEqual(result, {'id': 1})

    @patch('server.services.auth_service.UserRepository')
    def test_signup_user_exists(self, mock_user_repo):
        mock_user_repo.return_value.email_exists.return_value = True
        self.service.user_repo = mock_user_repo.return_value
        with self.assertRaises(ValueError):
            self.service.signup('user', 'email', 'pass')

    @patch('server.services.auth_service.UserRepository')
    @patch('server.services.auth_service.PasswordService')
    def test_login_success(self, mock_password, mock_user_repo):
        mock_user_repo.return_value.get_user_by_email.return_value = {'password': 'hashed'}
        mock_password.return_value.verify_password.return_value = True
        self.service.user_repo = mock_user_repo.return_value
        self.service.password_service = mock_password.return_value
        result = self.service.login('email', 'pass')
        self.assertEqual(result, {'password': 'hashed'})

    @patch('server.services.auth_service.UserRepository')
    @patch('server.services.auth_service.PasswordService')
    def test_login_invalid(self, mock_password, mock_user_repo):
        mock_user_repo.return_value.get_user_by_email.return_value = {'password': 'hashed'}
        mock_password.return_value.verify_password.return_value = False
        self.service.user_repo = mock_user_repo.return_value
        self.service.password_service = mock_password.return_value
        with self.assertRaises(ValueError):
            self.service.login('email', 'pass')


if __name__ == '__main__':
    unittest.main()
