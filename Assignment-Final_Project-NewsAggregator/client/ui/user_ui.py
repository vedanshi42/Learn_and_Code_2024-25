from client.ui.article_ui import ArticleUI
from client.ui.notification_ui import NotificationUI
from client.ui.saved_article_ui import SavedArticleUI
from client.ui.search_ui import SearchArticleUI


class UserUI:
    def __init__(self):
        self.article_ui = ArticleUI()
        self.notif_ui = NotificationUI()
        self.saved_ui = SavedArticleUI()
        self.search_ui = SearchArticleUI()

    def menu(self, user):
        while True:
            print(f"\nHi {user['username']}, Welcome to NewsViews")
            print("1. View Headlines")
            print("2. View Recommended Articles")
            print("3. My Saved Articles")
            print("4. Search Headlines")
            print("5. Notifications")
            print("6. Logout")
            ch = input("Choose: ")
            if ch == '1':
                self.article_ui.view_headlines(user)
            elif ch == '2':
                self.article_ui.view_recommended_articles(user)
            elif ch == '3':
                self.saved_ui.manage(user)
            elif ch == '4':
                self.search_ui.search(user)
            elif ch == '5':
                self.notif_ui.configure(user)
            elif ch == '6':
                break
