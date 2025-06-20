from server.repositories.search_article_repository import SearchArticleRepository
from server.repositories.user_saved_article_repository import UserSavedArticleRepository


class ArticleUI:
    def __init__(self):
        self.search_article_repo = SearchArticleRepository()
        self.save_repo = UserSavedArticleRepository()

    def view_headlines(self, user):
        print("1. Today's headlines\n2. Filter by date range\n3. Filter by category\n4. Back")
        ch = input("Choose: ")
        if ch == '1':
            articles = self.search_article_repo.find_today_articles()
        elif ch == '2':
            from_date, to_date = input("Enter date range(YYYY-MM-DD to YYYY-MM-DD): ").split(' to ')
            articles = self.search_article_repo.find_by_date_range(from_date, to_date)
        elif ch == '3':
            input_category = input("Enter category: ")
            articles = self.search_article_repo.search_by_category(input_category)
        else:
            return

        for id, content in articles.items():
            print(f"{id} - {content}")

        aid = input("Enter Article ID to save or B to go back: ")
        if aid.lower() != 'b':
            self.save_repo.save_by_id(user['user_id'], int(aid))

    def search(self):
        print("Search by:\n1. Keyword\n2. Category\n3. Back")
        c = input("Choose: ")
        if c == '1':
            kw = input("Keyword: ")
            articles = self.search_article_repo.search_by_keyword(kw)
        elif c == '2':
            cat = input("Category: ")
            articles = self.search_article_repo.search_by_category(cat)
        else:
            return

        for art in articles:
            print(f"{art['article_id']: art['title'], art['date_published']}")
        save = input("Enter ID to save or B to go back: ")
        if save.lower() != 'b':
            self.save_repo.save_by_id(articles['article_id'], int(save))
