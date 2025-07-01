from client.services.client_api import ClientAPIService


class SavedArticleUI:
    def __init__(self):
        self.client = ClientAPIService()

    def manage(self, user):
        articles = self.client.get_saved_articles(user['user_id'])
        for a in articles:
            print(f"{a['article_id']} - {a['title']}")

        d = input("Enter ID to delete or B to go back: ")
        if d.lower() != 'b':
            self.client.delete_saved_article(user['user_id'], int(d))
            print("Deleted.")
