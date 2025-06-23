from server.repositories.search_article_repository import SearchArticleRepository


class SearchArticleUI:
    def __init__(self):
        self.search_repo = SearchArticleRepository()

    def search(self, user):
        print("1. Search by Keyword\n2. Search by category\n3. Search by date\n4. Back")
        ch = input("Choose: ")
        if ch == '1':
            search_input = input('Enter Keyword: ')
            articles = self.search_repo.search_by_category(search_input)
        elif ch == '2':
            search_input = input('Enter Category: ')
            articles = self.search_repo.search_by_keyword(search_input)
        elif ch == '3':
            search_input = input("Enter date to filter: (YYYY-MM-DD)")
            articles = self.search_repo.search_by_date(search_input)
        else:
            return

        for id, content in articles.items():
            print(f"{id} - {content}")
