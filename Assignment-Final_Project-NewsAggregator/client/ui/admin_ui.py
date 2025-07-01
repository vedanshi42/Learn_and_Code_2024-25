from client.services.client_api import ClientAPIService


class AdminUI:
    def __init__(self):
        self.client = ClientAPIService()

    def menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. View External Servers")
            print("2. View Server Details")
            print("3. Update API Key")
            print("4. Add Category")
            print("5. View & Manage All Categories")
            print("6. View & Manage All Keywords")
            print("7. View & Delete Reported Articles")
            print("8. Logout")
            ch = input("Choose: ")

            if ch == '1':
                self._view_external_servers()
            elif ch == '2':
                self._view_api_keys()
            elif ch == '3':
                self._update_api_key()
            elif ch == '4':
                self._add_category()
            elif ch == '5':
                self._manage_categories()
            elif ch == '6':
                self._manage_keywords()
            elif ch == '7':
                self._manage_reported_articles()
            elif ch == '8':
                break
            else:
                print("Invalid choice.")

    def _view_external_servers(self):
        statuses = self.client.get_external_statuses()
        for s in statuses:
            print(f"{s['api_name']}: {s['status']} (Last Accessed: {s['last_accessed']})")

    def _view_api_keys(self):
        keys = self.client.get_external_keys()
        for k in keys:
            print(f"{k['api_name']} - Key: {k['api_key']} (Last Accessed: {k['last_accessed']})")

    def _update_api_key(self):
        name = input("API name: ")
        new_key = input("New API key: ")
        self.client.update_api_key(name, new_key)

    def _add_category(self):
        name = input("New Category: ")
        self.client.add_category(name)

    def _manage_categories(self):
        categories = self.client.get_all_categories()
        print("\n--- All Categories ---")
        for idx, cat in enumerate(categories, 1):
            print(f"{idx}. {cat['name']} | {cat['status']}")

        print("B. Back")
        ch = input("Enter category number to enable/disable or B to go back: ")
        if ch.isdigit() and 1 <= int(ch) <= len(categories):
            name = categories[int(ch) - 1]['name']
            self.client.disable_category(name)
            print(f"Category '{name}' disabled.")
        elif ch.lower() == 'b':
            return
        else:
            print("Invalid choice.")

    def _manage_keywords(self):
        keywords = self.client.get_all_keywords()
        print("\n--- All Keywords ---")
        for idx, kw in enumerate(keywords, 1):
            print(f"{idx}. {kw['keyword']} | {kw['status']}")

        print("B. Back")
        ch = input("Enter keyword number to disable or B to go back: ")
        if ch.isdigit() and 1 <= int(ch) <= len(keywords):
            word = keywords[int(ch) - 1]['keyword']
            self.client.disable_keyword(word)
            print(f"Keyword '{word}' disabled.")
        elif ch.lower() == 'b':
            return
        else:
            print("Invalid choice.")

    def _manage_reported_articles(self):
        articles = self.client.get_reported_articles()
        if not articles:
            print("No reported articles found.")
            return

        print("\n--- Reported Articles ---")
        for idx, a in enumerate(articles, 1):
            print(f"{idx}. ID: {a['article_id']} | Title: {a['title']} | Reports: {a['report_count']}")

        print("B. Back")
        ch = input("Enter number of article to delete if report_count > 5 or B to go back: ")
        if ch.isdigit():
            index = int(ch) - 1
            if 0 <= index < len(articles):
                article = articles[index]
                if article["report_count"] >= 5:
                    self.client.delete_article(article["article_id"])
                    print(f"Article '{article['title']}' deleted.")
                else:
                    print("Article does not have enough reports to delete.")
            else:
                print("Invalid selection.")
        elif ch.lower() == 'b':
            return
        else:
            print("Invalid choice.")
