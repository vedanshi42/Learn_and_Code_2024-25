import unittest
from unittest.mock import patch
from server.services.notifications_service.notification_email_service import NotificationEmailService


class TestNotificationEmailService(unittest.TestCase):
    def setUp(self):
        self.service = NotificationEmailService()

    @patch('server.services.notifications_service.notification_email_service.UserRepository')
    @patch('server.services.notifications_service.notification_email_service.NotificationRepository')
    @patch('server.services.notifications_service.notification_email_service.EmailService')
    def test_send_notifications_to_all_users(self, mock_email, mock_notif_repo, mock_user_repo):
        mock_user_repo.return_value.get_all_users.return_value = [{'user_id': 1, 'username': 'u', 'email': 'e'}]
        mock_notif_repo.return_value.get_notifications_for_user.return_value = [{'title': 't', 'date_published': 'd'}]
        self.service.user_repo = mock_user_repo.return_value
        self.service.notifications_repo = mock_notif_repo.return_value
        self.service.emailer = mock_email.return_value
        self.service.send_notifications_to_all_users()
        mock_email.return_value.send_email.assert_called()


if __name__ == '__main__':
    unittest.main()
