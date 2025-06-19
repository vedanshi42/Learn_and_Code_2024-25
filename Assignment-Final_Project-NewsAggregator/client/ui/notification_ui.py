from server.services.notification_configurator import NotificationsConfigurator
from server.services.notification_viewer import NotificationsViewer


class NotificationUI:
    def __init__(self):
        self.config = NotificationsConfigurator()
        self.viewer = NotificationsViewer()

    def configure(self, user):
        print("\n--- Your Notifications ---")
        notes = self.viewer.get_user_notifications(user.email)
        for n in notes:
            print(f"- {n['title']}")

        print("\n1. Add Category\n2. Add Keyword\n3. Back")
        ch = input("Choose: ")
        if ch == '1':
            c = input("Enter Category: ")
            self.config.add_category_for_user(user.email, c)
        elif ch == '2':
            k = input("Enter Keyword: ")
            self.config.add_keyword_for_user(user.email, k)
