from unittest.mock import patch, MagicMock
from server.utils.email_utils import EmailService


class TestEmailService:
    def setup_class(self):
        self.email_service = EmailService()

    @patch("server.utils.email_utils.smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        result = self.email_service.send_email(
            to_email="test@example.com",
            subject="Test Subject",
            body="Test Body"
        )

        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch("server.utils.email_utils.smtplib.SMTP", side_effect=Exception("SMTP failure"))
    def test_send_email_failure(self, mock_smtp):
        result = self.email_service.send_email(
            to_email="fail@example.com",
            subject="Fail Test",
            body="This should fail"
        )
        assert result is False
