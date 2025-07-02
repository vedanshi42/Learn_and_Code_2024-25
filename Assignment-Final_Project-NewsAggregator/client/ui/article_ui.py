from client.services.client_api import ClientAPIService
from server.repositories.feedback_repository import FeedbackService
from tabulate import tabulate


class ArticleUI:
    def __init__(self):
        self.client = ClientAPIService()
        self.feedback_service = FeedbackService()

    def view_headlines(self, user):
        print("\n=== View Headlines ===")
        filter_by = self._get_filter_option()
        sort_by = self._get_sort_option()

        articles = self.client.fetch_headlines(filter_by=filter_by, sort_by=sort_by, user_id=user['user_id'])
        self._handle_article_flow(articles, user)

    def view_recommended_articles(self, user):
        print("\n=== Recommended Articles ===")
        articles = self.client.get_recommended_articles(user['user_id'])
        self._handle_article_flow(articles, user)

    def _get_filter_option(self):
        print("1. No Filter\n2. Filter by Category\n3. Filter by Date")
        option = input("Choose filter: ").strip()
        if option == '2':
            return input("Enter Category: ").strip()
        elif option == '3':
            return input("Enter Date (YYYY-MM-DD): ").strip()
        return None

    def _get_sort_option(self):
        print("1. No Sort\n2. Sort by Likes\n3. Sort by Dislikes\n4. Sort by Date")
        option = input("Choose sorting: ").strip()
        return {
            '2': 'likes',
            '3': 'dislikes',
            '4': 'date_published'
        }.get(option)

    def _handle_article_flow(self, articles, user):
        if not articles:
            print("No articles found.")
            return

        self._print_articles(articles)

        while True:
            print("\nOptions:\n1. Save Article\n2. Like\n3. Dislike\n4. Report\n5. Back")
            choice = input("Select an option: ").strip()
            if choice == '5':
                break
            self._handle_user_action(choice, user)

    def _print_articles(self, articles):
        table = [[
            a['article_id'], a['title'], a['category'], a['source_url'],
            a['date_published'], a['likes'], a['dislikes']
        ] for a in articles]

        print(tabulate(
            table,
            headers=["ID", "Title", "Category", "URL", "Date", "Likes", "Dislikes"],
            maxcolwidths=[None, 30]
        ))

    def _handle_user_action(self, choice, user):
        try:
            aid = int(input("Enter Article ID: ").strip())
        except ValueError:
            print("Invalid article ID. Must be a number.")
            return

        user_id = user['user_id']

        try:
            if choice == '1':
                self.client.save_article(user_id, aid)
                print(f"Article {aid} saved.")
            elif choice == '2':
                self.client.like_article(user_id, aid)
                print(f"Article {aid} liked.")
            elif choice == '3':
                self.client.dislike_article(user_id, aid)
                print(f"Article {aid} disliked.")
            elif choice == '4':
                self.client.report_article(user_id, aid)
                print(f"Article {aid} reported.")
            else:
                print("Invalid option.")
        except Exception as e:
            print(f"Error performing action: {e}")
