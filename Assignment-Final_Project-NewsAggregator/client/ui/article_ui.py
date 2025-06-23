from server.repositories.search_article_repository import SearchArticleRepository
from server.repositories.user_saved_article_repository import UserSavedArticleRepository
from server.repositories.feedback_repository import FeedbackService
from server.repositories.reporting_repository import ReportingService
from tabulate import tabulate


class ArticleUI:
    def __init__(self):
        self.search_article_repo = SearchArticleRepository()
        self.save_repo = UserSavedArticleRepository()
        self.feedback_service = FeedbackService()
        self.report_service = ReportingService()

    def view_headlines(self, user):
        print("\n=== View Headlines ===")
        print("1. Today's headlines\n2. Filter by date range\n3. Filter by category\n4. Back")
        ch = input("Choose: ")

        if ch == '1':
            articles_dict = self.search_article_repo.find_today_articles()
        elif ch == '2':
            from_date, to_date = input("Enter date range (YYYY-MM-DD to YYYY-MM-DD): ").split(' to ')
            articles_dict = self.search_article_repo.find_by_date_range(from_date, to_date)
        elif ch == '3':
            category = input("Enter category: ")
            articles_dict = self.search_article_repo.search_by_category(category)
        else:
            return

        # Prepare table data
        table = []
        for aid, data in articles_dict.items():
            title, url, date_str = data
            likes, dislikes = self.feedback_service.get_feedback_counts(aid)
            table.append([aid, title[:50], url, date_str, likes, dislikes])

        print(tabulate(table, headers=["ID", "Title", "URL", "Date", "Likes", "Dislikes"]))

        # Interaction loop
        while True:
            print("\nOptions:\n1. Save Article\n2. Like\n3. Dislike\n4. Report\n5. Back")
            choice = input("Select an option: ")
            if choice == '5':
                break

            try:
                aid = int(input("Enter Article ID: "))
                if aid not in articles_dict:
                    print("Invalid ID.")
                    continue

                if choice == '1':
                    self.save_repo.save_by_id(user['user_id'], aid)
                elif choice == '2':
                    self.feedback_service.like_article(user['user_id'], aid)
                elif choice == '3':
                    self.feedback_service.dislike_article(user['user_id'], aid)
                elif choice == '4':
                    self.report_service.report_article(user['user_id'], aid)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid numeric ID.")

