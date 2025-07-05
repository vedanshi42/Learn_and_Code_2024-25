from client.services.admin_client import AdminClient


class AdminUI:
    def __init__(self, client=None):
        self.client = client if client else AdminClient()
        self.menu_actions = {
            "1": self._view_external_servers,
            "2": self._view_api_keys,
            "3": self._update_api_key,
            "4": self._add_category,
            "5": self._manage_categories,
            "6": self._manage_keywords,
            "7": self._manage_reported_articles,
            "8": self._logout,
        }
        self._running = True

    def menu(self):
        while self._running:
            print("\n--- Admin Menu ---")
            print("1. View External Servers")
            print("2. View Server Details")
            print("3. Update API Key")
            print("4. Add Category")
            print("5. View & Manage All Categories")
            print("6. View & Manage All Keywords")
            print("7. View & Delete Reported Articles")
            print("8. Logout")
            choice = input("Choose: ")
            action = self.menu_actions.get(choice)
            if action:
                try:
                    action()
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Invalid choice.")

    def _logout(self):
        self._running = False

    def _handle_response(self, response, success_msg=None):
        if isinstance(response, dict) and response.get("error"):
            print(f"Error: {response['error']}")
            return False
        if success_msg:
            print(success_msg)
        return True

    def _view_external_servers(self):
        statuses = self.client.get_external_statuses()
        if not self._handle_response(statuses):
            return
        for s in statuses:
            print(
                f"{s['api_name']}: {s['status']} (Last Accessed: {s['last_accessed']})"
            )

    def _view_api_keys(self):
        keys = self.client.get_external_keys()
        if not self._handle_response(keys):
            return
        for k in keys:
            print(
                f"{k['api_name']} - Key: {k['api_key']} (Last Accessed: {k['last_accessed']})"
            )

    def _update_api_key(self):
        name = input("API name: ")
        new_key = input("New API key: ")
        result = self.client.add_or_update_api_key(name, new_key)
        self._handle_response(result, "API key updated.")

    def _add_category(self):
        name = input("New Category: ")
        result = self.client.add_category(name)
        self._handle_response(result, "Category added.")

    def _manage_categories(self):
        categories = self.client.get_all_categories()
        if not self._handle_response(categories):
            return
        print("\n--- All Categories ---")

        for category_number, category in enumerate(categories, 1):
            print(f"{category_number}. {category['name']} | {category['status']}")
        print("B. Back")

        choice = input("Enter category number to enable/disable or B to go back: ")
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            name = categories[int(choice) - 1]["name"]
            result = self.client.disable_category(name)
            self._handle_response(result, f"Category '{name}' disabled.")
        elif choice.lower() == "b":
            return
        else:
            print("Invalid choice.")

    def _manage_keywords(self):
        keywords = self.client.get_all_keywords()
        if not self._handle_response(keywords):
            return
        print("\n--- All Keywords ---")

        for keyword_number, keyword in enumerate(keywords, 1):
            print(f"{keyword_number}. {keyword['keyword']} | {keyword['status']}")
        print("B. Back")

        choice = input("Enter keyword number to disable or B to go back: ")

        if choice.isdigit() and 1 <= int(choice) <= len(keywords):
            word = keywords[int(choice) - 1]["keyword"]
            result = self.client.disable_keyword(word)
            self._handle_response(result, f"Keyword '{word}' disabled.")
        elif choice.lower() == "b":
            return
        else:
            print("Invalid choice.")

    def _manage_reported_articles(self):
        articles = self.client.get_reported_articles()
        if not self._handle_response(articles):
            return
        if not articles:
            print("No reported articles found.")
            return
        print("\n--- Reported Articles ---")
        for number, article in enumerate(articles, 1):
            print(
                f"{number}. ID: {article['article_id']} | Title: {article['title']} | Reports: {article['report_count']}"
            )
        print("B. Back")
        choice = input(
            "Enter number of article to delete if report_count > 5 or B to go back: "
        )
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(articles):
                article = articles[index]
                if article["report_count"] >= 5:
                    result = self.client.delete_article(article["article_id"])
                    self._handle_response(
                        result, f"Article '{article['title']}' deleted."
                    )
                else:
                    print("Article does not have enough reports to delete.")
            else:
                print("Invalid selection.")
        elif choice.lower() == "b":
            return
        else:
            print("Invalid choice.")
