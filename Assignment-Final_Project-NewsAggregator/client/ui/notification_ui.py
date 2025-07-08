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
            choice = input("Choose: ")

            if choice == "1":
                self._view_notifications(user["user_id"])
            elif choice == "2":
                self._manage_categories(user["user_id"])
            elif choice == "3":
                self._manage_keywords(user["user_id"])
            elif choice == "4":
                break
            else:
                print("Invalid option. Please select a valid option.")

    def _view_notifications(self, user_id):
        notes = self.client.get_user_notifications(user_id)
        if not notes or (isinstance(notes, dict) and notes.get("error")):
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
            for category_number, category in enumerate(categories, 1):
                print(
                    f"{category_number}. {category['name']} - {'Enabled' if category['is_enabled'] else 'Disabled'}"
                )

            print(f"{len(categories) + 1}. Add New Category")
            print("B. Back")

            choice = input("Choose: ")

            if choice.lower() == "b":
                break
            elif choice == str(len(categories) + 1):
                new_cat = input("Enter new category name: ").strip()

                response = self.client.add_category_for_user(user_id, new_cat)
                if response.get("error"):
                    print(f"Error: {response['error']}")
                else:
                    print("Category added.")
                continue

            elif choice.isdigit() and 1 <= int(choice) <= len(categories):
                selected = categories[int(choice) - 1]
                response = self.client.toggle_category(user_id, selected["name"])
                if isinstance(response, dict) and response.get("error"):
                    print(f"Error: {response['error']}")
                elif response:
                    print("Category toggled.")
                else:
                    print("Cannot enable admin disabled categories")
                continue

            else:
                print("Invalid option. Please select a valid option.")

    def _manage_keywords(self, user_id):
        while True:
            keywords = self.client.get_user_keywords(user_id)
            print("\n--- Your Keywords ---")

            for keyword_number, keyword in enumerate(keywords, 1):
                print(
                    f"{keyword_number}. {keyword['keyword']} - {'Enabled' if keyword['is_enabled'] else 'Disabled'}"
                )

            print(f"{len(keywords) + 1}. Add New Keyword")
            print("B. Back")

            choice = input("Choose: ")

            if choice.lower() == "b":
                break

            elif choice == str(len(keywords) + 1):
                new_keyword = input("Enter new keyword: ").strip()
                response = self.client.add_keyword_for_user(user_id, new_keyword)
                if isinstance(response, dict) and response.get("error"):
                    print(f"Error: {response['error']}")
                else:
                    print("Keyword added.")
                continue

            elif choice.isdigit() and 1 <= int(choice) <= len(keywords):
                selected = keywords[int(choice) - 1]
                response = self.client.toggle_keyword(user_id, selected["keyword"])
                if isinstance(response, dict) and response.get("error"):
                    print(f"Error: {response['error']}")
                elif response:
                    print("Keyword toggled.")
                else:
                    print("Cannot enable admin disabled keywords")
                continue

            else:
                print("Invalid option. Please select a valid option.")
