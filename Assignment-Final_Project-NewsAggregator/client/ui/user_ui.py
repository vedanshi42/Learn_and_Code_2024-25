from client.ui.article_ui import ArticleUI
from client.ui.notification_ui import NotificationUI
from client.ui.saved_article_ui import SavedArticleUI


class UserUI:
    def __init__(self):
        self.article_ui = ArticleUI()
        self.notif_ui = NotificationUI()
        self.saved_ui = SavedArticleUI()

    def menu(self, user):
        while True:
            print("\n--- User Menu ---")
            print("1. View Headlines")
            print("2. My Saved Articles")
            print("3. Search Headlines")
            print("4. Notifications")
            print("5. Logout")
            ch = input("Choose: ")
            if ch == '1':
                self.article_ui.view_headlines(user)
            elif ch == '2':
                self.saved_ui.manage(user)
            elif ch == '3':
                self.article_ui.search(user)
            elif ch == '4':
                self.notif_ui.configure(user)
            elif ch == '5':
                break
