from server.repositories.notification_repository import NotificationRepository


class NotificationsViewer:
    def __init__(self):
        self.notification_repo = NotificationRepository()

    def get_user_notifications(self, email: str):
        return self.notification_repo.get_notifications_for_user(email)
