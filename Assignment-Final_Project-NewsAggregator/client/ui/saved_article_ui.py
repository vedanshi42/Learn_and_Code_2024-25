from client.services.saved_article_client import SavedArticleClient


class SavedArticleUI:
    def __init__(self):
        self.client = SavedArticleClient()

    def manage(self, user):
        articles = self.client.get_saved_articles(user["user_id"])
        for article in articles:
            print(f"{article['article_id']} - {article['title']}")

        d = input("Enter ID to delete or B to go back: ")
        if d.lower() != "b":
            self.client.delete_saved_article(user["user_id"], int(d))
            print("Deleted.")
