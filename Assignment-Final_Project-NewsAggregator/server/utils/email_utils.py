import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from server.config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS


class EmailService:
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
