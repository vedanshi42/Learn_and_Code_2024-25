from client.services.client_api import ClientAPIService
from server.repositories.feedback_repository import FeedbackService
from tabulate import tabulate


class ArticleUI:
    def __init__(self):
        self.client = ClientAPIService()
        self.feedback_service = FeedbackService()

    def view_headlines(self, user):
        print("\n=== View Headlines ===")
        print("1. No Filter\n2. Filter by Category\n3. Filter by Date")
        filter_option = input("Choose filter: ")
        filter_by = None

        if filter_option == '2':
            filter_by = input("Enter Category: ")
        elif filter_option == '3':
            filter_by = input("Enter Date (YYYY-MM-DD): ")

        print("1. No Sort\n2. Sort by Likes\n3. Sort by Dislikes\n4. Sort by Date")
        sort_option = input("Choose sorting: ")
        sort_by = None

        if sort_option == '2':
            sort_by = 'likes'
        elif sort_option == '3':
            sort_by = 'dislikes'
        elif sort_option == '4':
            sort_by = 'date_published'

        articles = self.client.fetch_headlines(filter_by=filter_by, sort_by=sort_by, user_id=user['user_id'])

        if not articles:
            print("No articles found.")
            return

        table = []
        for a in articles:
            table.append([
                a['article_id'], a['title'], a['source_url'],
                a['date_published'], a['likes'], a['dislikes']
            ])

        print(tabulate(table, headers=["ID", "Title", "URL", "Date", "Likes", "Dislikes"],
                       maxcolwidths=[None, 30]))

        while True:
            print("\nOptions:\n1. Save Article\n2. Like\n3. Dislike\n4. Report\n5. Back")
            choice = input("Select an option: ")
            if choice == '5':
                break

            try:
                aid = int(input("Enter Article ID: "))
                if choice == '1':
                    self.client.save_article(user['user_id'], aid)
                    print(f"Article with {aid} saved to your saved articles.")
                elif choice == '2':
                    self.client.like_article(user['user_id'], aid)
                    print(f"Article with {aid} liked.")
                elif choice == '3':
                    self.client.dislike_article(user['user_id'], aid)
                    print(f"Article with {aid} disliked.")
                elif choice == '4':
                    self.client.report_article(user['user_id'], aid)
                    print(f"Article with {aid} reported.")
                else:
                    print("Invalid option.")
            except Exception as e:
                print(f"Error: {e}")
