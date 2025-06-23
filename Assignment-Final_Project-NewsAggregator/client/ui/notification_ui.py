from server.services.notifications_service.notification_configurator import NotificationsConfigurator
from server.services.notifications_service.notification_viewer import NotificationsViewer


class NotificationUI:
    def __init__(self):
        self.config = NotificationsConfigurator()
        self.viewer = NotificationsViewer()

    def configure(self, user):
        while True:
            print("\n--- Notification Preferences ---")
            print("1. View Notifications")
            print("2. Manage Categories")
            print("3. Manage Keywords")
            print("4. Back")
            ch = input("Choose: ")

            if ch == '1':
                self._view_notifications(user['email'])
            elif ch == '2':
                self._manage_categories(user['email'])
            elif ch == '3':
                self._manage_keywords(user['email'])
            elif ch == '4':
                break
            else:
                print("Invalid choice.")

    def _view_notifications(self, email):
        print("\nYour Notifications:")
        notes = self.viewer.get_user_notifications(email)
        if not notes:
            print("No new articles for your preferences.")
        for n in notes:
            print(f"- {n['title']}")

    def _manage_categories(self, email):
        while True:
            categories = self.config.get_user_categories(email)
            print("\n--- Your Categories ---")
            for idx, c in enumerate(categories, 1):
                status = "Enabled" if c["is_enabled"] else "Disabled"
                print(f"{idx}. {c['name']} - {status}")
            print(f"{len(categories) + 1}. Add New Category")
            print("B. Back")

            ch = input("Choose an option: ")
            if ch.lower() == 'b':
                break
            elif ch == str(len(categories) + 1):
                new_cat = input("Enter new category name: ").strip()
                self.config.add_category_for_user(email, new_cat)
                print("Category added and enabled.")
            elif ch.isdigit() and 1 <= int(ch) <= len(categories):
                selected = categories[int(ch) - 1]
                self.config.toggle_category(email, selected["name"])
                print("Category status toggled.")
            else:
                print("Invalid input.")

    def _manage_keywords(self, email):
        while True:
            keywords = self.config.get_user_keywords(email)
            print("\n--- Your Keywords ---")
            for idx, k in enumerate(keywords, 1):
                status = "Enabled" if k["is_enabled"] else "Disabled"
                print(f"{idx}. {k['keyword']} - {status}")
            print(f"{len(keywords) + 1}. Add New Keyword")
            print("B. Back")

            ch = input("Choose an option: ")
            if ch.lower() == 'b':
                break
            elif ch == str(len(keywords) + 1):
                new_kw = input("Enter new keyword: ").strip()
                self.config.add_keyword_for_user(email, new_kw)
                print("Keyword added and enabled.")
            elif ch.isdigit() and 1 <= int(ch) <= len(keywords):
                selected = keywords[int(ch) - 1]
                self.config.toggle_keyword(email, selected["keyword"])
                print("Keyword status toggled.")
            else:
                print("Invalid input.")
