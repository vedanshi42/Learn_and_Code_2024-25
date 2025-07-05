from server.repositories.notification_repository import NotificationRepository
from server.config.logging_config import news_agg_logger


class NotificationsViewer:
    def __init__(self):
        self.notification_repo = NotificationRepository()

    def get_user_notifications(self, email: str):
        try:
            return self.notification_repo.get_notifications_for_user(email)
        except Exception as e:
            news_agg_logger(40, f"Failed to get notifications for user {email}: {e}")
            raise
