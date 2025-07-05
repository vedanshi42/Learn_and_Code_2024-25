from client.services.search_client import SearchClient


class SearchArticleUI:
    def __init__(self):
        self.client = SearchClient()

    def search(self, user):
        while True:
            print("1. Search by Keyword\n2. Search by Category\n3. Search by Date\n4. Back")
            ch = input("Choose: ")

            if ch == '1':
                term = input("Enter keyword: ")
                result = self.client.search_articles(keyword=term)
            elif ch == '2':
                term = input("Enter category: ")
                result = self.client.search_articles(category=term)
            elif ch == '3':
                date = input("Enter date (YYYY-MM-DD): ")
                result = self.client.search_articles(date=date)
            elif ch == '4':
                return
            else:
                print("Invalid option. Please select a valid option.")
                continue

            if isinstance(result, dict) and result.get("error"):
                print(f"Error: {result['error']}")
                continue
            if not result:
                print("No articles found.")
                continue
            for article in result:
                print(f"{article['article_id']} - {article['title']}, url - {article['source_url']}")
