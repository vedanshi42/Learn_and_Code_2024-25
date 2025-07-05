from client.services.notification_client import NotificationClient


class NotificationUI:
    def __init__(self):
        self.client = NotificationClient()

    def configure(self, user):
        while True:
            print("\n--- Notification Configuration ---")
            print("1. View Notifications")
            print("2. Manage Categories")
            print("3. Manage Keywords")
            print("4. Back")
            ch = input("Choose: ")

            if ch == '1':
                self._view_notifications(user['user_id'])
            elif ch == '2':
                self._manage_categories(user['user_id'])
            elif ch == '3':
                self._manage_keywords(user['user_id'])
            elif ch == '4':
                break
            else:
                print("Invalid option. Please select a valid option.")

    def _view_notifications(self, user_id):
        notes = self.client.get_user_notifications(user_id)
        if not notes or (isinstance(notes, dict) and notes.get('error')):
            print("No new notifications.")
            return
        for n in notes[:5]:
            print(f"{n['date_published']} - {n['title']}")

    def _manage_categories(self, user_id):
        while True:
            categories = self.client.get_user_categories(user_id)

            if not isinstance(categories, list):
                print("Could not fetch categories or received invalid data.")
                return

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

                resp = self.client.add_category_for_user(user_id, new_cat)
                if resp.get('error'):
                    print(f"Error: {resp['error']}")
                else:
                    print("Category added.")
                continue

            elif ch.isdigit() and 1 <= int(ch) <= len(categories):
                selected = categories[int(ch) - 1]
                resp = self.client.toggle_category(user_id, selected["name"])
                if isinstance(resp, dict) and resp.get('error'):
                    print(f"Error: {resp['error']}")
                elif resp:
                    print("Category toggled.")
                else:
                    print('Cannot enable admin disabled categories')
                continue

            else:
                print("Invalid option. Please select a valid option.")

    def _manage_keywords(self, user_id):
        while True:
            keywords = self.client.get_user_keywords(user_id)
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
                resp = self.client.add_keyword_for_user(user_id, new_kw)
                if isinstance(resp, dict) and resp.get('error'):
                    print(f"Error: {resp['error']}")
                else:
                    print("Keyword added.")
                continue

            elif ch.isdigit() and 1 <= int(ch) <= len(keywords):
                selected = keywords[int(ch) - 1]
                resp = self.client.toggle_keyword(user_id, selected["keyword"])
                if isinstance(resp, dict) and resp.get('error'):
                    print(f"Error: {resp['error']}")
                elif resp:
                    print("Keyword toggled.")
                else:
                    print('Cannot enable admin disabled keywords')
                continue

            else:
                print("Invalid option. Please select a valid option.")
