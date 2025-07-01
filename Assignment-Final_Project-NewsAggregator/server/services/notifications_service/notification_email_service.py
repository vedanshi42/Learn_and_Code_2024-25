from server.repositories.notification_repository import NotificationRepository
from server.repositories.user_repository import UserRepository
from server.utils.email_utils import EmailService


class NotificationEmailService:
    def __init__(self):
        self.note_repo = NotificationRepository()
        self.user_repo = UserRepository()
        self.emailer = EmailService()

    def send_notifications_to_all_users(self):
        users = self.user_repo.get_all_users()
        for user in users:
            notes = self.note_repo.get_notifications_for_user(user['email'])

            if not notes:
                continue

            body = f"Hi {user['username']},\n\nHere are your latest article notifications:\n\n"
            for n in notes[:5]:
                body += f"- {n['title']} ({n['date_published']})\n"

            body += "\nLogin to check more.\n\nRegards,\nNews Views"
            self.emailer.send_email(user['email'], "Your News Notifications", body)
