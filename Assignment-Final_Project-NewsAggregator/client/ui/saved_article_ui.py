from server.repositories.user_saved_article_repository import UserSavedArticleRepository


class SavedArticleUI:
    def __init__(self):
        self.repo = UserSavedArticleRepository()

    def manage(self, user):
        articles = self.repo.get_saved_articles(user.user_id)
        for a in articles:
            print(f"[{a['saved_id']}] {a['title']}")
        d = input("Enter ID to delete or B to go back: ")
        if d.lower() != 'b':
            self.repo.delete_by_id(user.user_id, int(d))
