from client.services.client_api import ClientAPIService


class SearchArticleUI:
    def __init__(self):
        self.client = ClientAPIService()

    def search(self, user):
        print("1. Search by Keyword\n2. Search by Category\n3. Search by Date\n4. Back")
        ch = input("Choose: ")

        if ch == '1':
            term = input("Enter keyword: ")
            articles = self.client.search_articles_by_keyword(term)
        elif ch == '2':
            term = input("Enter category: ")
            articles = self.client.search_articles_by_category(term)
        elif ch == '3':
            date = input("Enter date (YYYY-MM-DD): ")
            articles = self.client.search_articles_by_date(date)
        else:
            return

        for article_id, article_content in articles.items():
            print(f"{article_id} - {article_content[0]}, url - {article_content[1]}")
