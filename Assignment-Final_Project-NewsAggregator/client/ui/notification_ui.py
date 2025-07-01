from client.services.client_api import ClientAPIService


class NotificationUI:
    def __init__(self):
        self.client = ClientAPIService()

    def configure(self, user):
        while True:
            print("\n--- Notification Configuration ---")
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

    def _view_notifications(self, email):
        notes = self.client.get_user_notifications(email)
        if not notes:
            print("No new notifications.")
            return
        for n in notes[:5]:
            print(f"{n['date_published']} - {n['title']}")

    def _manage_categories(self, email):
        while True:
            categories = self.client.get_user_categories(email)
            print("\n--- Your Categories ---")
            for idx, c in enumerate(categories, 1):
                print(f"{idx}. {c['name']} - {'Enabled' if c['is_enabled'] else 'Disabled'}")
            print(f"{len(categories) + 1}. Add New Category")
            print("B. Back")

            ch = input("Choose: ")

            if ch.lower() == 'b':
                break
            elif ch == str(len(categories) + 1):
                new_cat = input("Enter new category name: ").strip()
                self.client.add_category_for_user(email, new_cat)
                print("Category added.")
            elif ch.isdigit() and 1 <= int(ch) <= len(categories):
                selected = categories[int(ch) - 1]
                if self.client.toggle_category(email, selected["name"]):
                    print("Category toggled.")
                else:
                    print('Cannot enable admin disabled categories')
            else:
                print("Invalid input.")

    def _manage_keywords(self, email):
        while True:
            keywords = self.client.get_user_keywords(email)
            print("\n--- Your Keywords ---")
            for idx, k in enumerate(keywords, 1):
                print(f"{idx}. {k['keyword']} - {'Enabled' if k['is_enabled'] else 'Disabled'}")
            print(f"{len(keywords) + 1}. Add New Keyword")
            print("B. Back")

            ch = input("Choose: ")

            if ch.lower() == 'b':
                break
            elif ch == str(len(keywords) + 1):
                new_kw = input("Enter new keyword: ").strip()
                self.client.add_keyword_for_user(email, new_kw)
                print("Keyword added.")
            elif ch.isdigit() and 1 <= int(ch) <= len(keywords):
                selected = keywords[int(ch) - 1]

                if self.client.toggle_keyword(email, selected["keyword"]):
                    print("Keyword toggled.")
                else:
                    print('Cannot enable admin disabled keywords')
            else:
                print("Invalid input.")
