from server.repositories.notification_repository import NotificationRepository
from server.repositories.user_repository import UserRepository
from server.utils.email_utils import EmailService
from server.config.logging_config import news_agg_logger


class NotificationEmailService:
    def __init__(self):
        self.note_repo = NotificationRepository()
        self.user_repo = UserRepository()
        self.emailer = EmailService()

    def send_notifications_to_all_users(self):
        try:
            users = self.user_repo.get_all_users()
            for user in users:
                try:
                    notifications = self.note_repo.get_notifications_for_user(user['email'])
                    if not notifications:
                        continue
                    body = f"Hi {user['username']},\n\nHere are your latest article notifications:\n\n"

                    for n in notifications[:5]:
                        body += f"- {n['title']} ({n['date_published']})\n"
                    body += "\nLogin to check more.\n\nRegards,\nNews Views"

                    try:
                        self.emailer.send_email(user['email'], "Your News Notifications", body)
                    except Exception as email_err:
                        news_agg_logger(40, f"Failed to send email to {user['email']}: {email_err}")
                except Exception as e:
                    news_agg_logger(40, f"Failed to process notifications for user {user['email']}: {e}")
            news_agg_logger(20, "Notification emails sent to all users.")
        except Exception as e:
            news_agg_logger(40, f"Failed to send notifications to all users: {e}")
            raise
