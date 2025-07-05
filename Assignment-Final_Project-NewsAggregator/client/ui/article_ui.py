from client.services.article_client import ArticleClient
from server.repositories.feedback_repository import FeedbackService
from tabulate import tabulate
from client.helpers.ui_helpers import UIHelpers
import textwrap


class ArticleUI:
    def __init__(self):
        self.client = ArticleClient()
        self.feedback_service = FeedbackService()

    def view_headlines(self, user):
        print("\n=== View Headlines ===")
        filter_by = self._get_filter_option()
        sort_by = self._get_sort_option()

        articles = self.client.fetch_headlines(
            filter_by=filter_by, sort_by=sort_by, user_id=user["user_id"]
        )
        if isinstance(articles, dict) and "error" in articles:
            print(f"Error: {articles['error']}")
            return
        self._handle_article_flow(articles, user)

    def view_recommended_articles(self, user):
        print("\n=== Recommended Articles ===")
        articles = self.client.get_recommended_articles(user["user_id"])
        if isinstance(articles, dict) and "error" in articles:
            print(f"Error: {articles['error']}")
            return
        self._handle_article_flow(articles, user)

    def _get_filter_option(self):
        print(
            "1. No Filter\n2. Filter by Category\n3. Filter by Date\n4. Filter by Date Range"
        )
        option = input("Choose filter: ").strip()

        if option == "2":
            return input("Enter Category: ").strip()

        elif option == "3":
            input_date = input("Enter Date (YYYY-MM-DD): ").strip()
            if input_date:
                try:
                    return UIHelpers.validate_date_format(input_date)
                except ValueError as e:
                    print(f"Invalid date format: {e}")
            return None
        elif option == "4":
            from_date = input("Enter From Date (YYYY-MM-DD): ").strip()
            to_date = input("Enter To Date (YYYY-MM-DD): ").strip()
            try:
                from_date = UIHelpers.validate_date_format(from_date)
                to_date = UIHelpers.validate_date_format(to_date)
                return {"from_date": from_date, "to_date": to_date}
            except ValueError as e:
                print(f"Invalid date format: {e}")
                return None
        return None

    def _get_sort_option(self):
        print("1. No Sort\n2. Sort by Likes\n3. Sort by Dislikes\n4. Sort by Date")
        option = input("Choose sorting: ").strip()
        return {"2": "likes", "3": "dislikes", "4": "date_published"}.get(option)

    def _handle_article_flow(self, articles, user):
        if not articles:
            print("No articles found.")
            return
        if isinstance(articles, dict) and "error" in articles:
            print(f"Error: {articles['error']}")
            return

        self._print_articles(articles)

        while True:
            print(
                "\nOptions:\n1. Save Article\n2. Like\n3. Dislike\n4. Report\n5. Back"
            )
            choice = input("Select an option: ").strip()
            if choice == "5":
                break
            elif choice in {"1", "2", "3", "4"}:
                self._handle_user_action(choice, user)
            else:
                print("Invalid option. Please select a valid option.")

    def _print_articles(self, articles):
        def wrap(text, width=30):
            return textwrap.fill(str(text), width=width)

        table = [
            [
                a["article_id"],
                wrap(a["title"], 30),
                a["category"],
                wrap(a["source_url"], 30),
                a["date_published"],
                a["likes"],
                a["dislikes"],
            ]
            for a in articles
        ]

        print(
            tabulate(
                table,
                headers=["ID", "Title", "Category", "URL", "Date", "Likes", "Dislikes"],
                tablefmt="simple",
            )
        )

    def _handle_user_action(self, choice, user):
        try:
            aid = int(input("Enter Article ID: ").strip())
        except ValueError:
            print("Invalid article ID. Must be a number.")
            return

        user_id = user["user_id"]

        try:
            if choice == "1":
                result = self.client.save_article(user_id, aid)
                if isinstance(result, dict) and "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Article {aid} saved.")

            elif choice == "2":
                result = self.client.like_article(user_id, aid)
                if isinstance(result, dict) and "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Article {aid} liked.")

            elif choice == "3":
                result = self.client.dislike_article(user_id, aid)
                if isinstance(result, dict) and "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Article {aid} disliked.")

            elif choice == "4":
                result = self.client.report_article(user_id, aid)
                if isinstance(result, dict) and "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Article {aid} reported.")

            else:
                print("Invalid option.")
        except Exception as e:
            print(f"Error performing action: {e}")
