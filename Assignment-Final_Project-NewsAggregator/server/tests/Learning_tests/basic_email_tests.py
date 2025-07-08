from server.utils.email_utils import EmailService


def test_send_real_email():
    email_service = EmailService()
    result = email_service.send_email(
        to_email="",
        subject="Test Email from NewsAgg",
        body="This is a test message from noreply.newsAgg@gmail.com."
    )
    assert result is True
