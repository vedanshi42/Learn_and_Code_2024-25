from server.repositories.external_api_repository import ExternalAPIRepository
from server.repositories.category_repository import CategoryRepository


class AdminUI:
    def __init__(self):
        self.api_repo = ExternalAPIRepository()
        self.cat_repo = CategoryRepository()

    def menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. View External Servers")
            print("2. View Server Details")
            print("3. Update API Key")
            print("4. Add Category")
            print("5. Logout")
            ch = input("Choose: ")
            if ch == '1':
                servers = self.api_repo.get_all_statuses()
                for s in servers:
                    print(f"{s['api_name']}: {s['status']}")
            elif ch == '2':
                keys = self.api_repo.get_all_keys()
                for k in keys:
                    print(f"{k['api_name']} - Key: {k['api_key']} (Last Accessed: {k['last_accessed']})")
            elif ch == '3':
                name = input("API name: ")
                new_key = input("New Key: ")
                self.api_repo.update_api_key(name, new_key)
            elif ch == '4':
                name = input("New Category: ")
                self.cat_repo.add_category(name)
            elif ch == '5':
                break
