from server.services.auth_service import AuthService
from server.services.notifications_service.notification_configurator import NotificationsConfigurator
from server.services.notifications_service.notification_updater import NotificationsUpdater
from server.services.notifications_service.notification_viewer import NotificationsViewer
from server.services.article_categorizing_service import ArticleCategorizer
from server.services.news_fetching_service import NewsFetcher
from server.repositories.article_repository import ArticleRepository
from server.utils.email_utils import EmailService


class TestEndToEndFlow:
    def test_user_notification_flow(self):
        email = "vedanshidixit18@rcew.ac.in"
        username = "TestUser"
        password = "secureTestPass"

        # === STEP 1: Sign up user ===
        auth_service = AuthService()
        try:
            user_id = auth_service.signup(username, email, password)
        except ValueError:
            pass

        # === STEP 2: Add preference ===
        pref_config = NotificationsConfigurator()
        pref_config.add_category_for_user(email, "World")

        # === STEP 3: Fetch articles from APIs ===
        fetcher = NewsFetcher()
        raw_articles = fetcher.fetch_all()

        # === STEP 4: Categorize Articles via ML ===
        categorizer = ArticleCategorizer()
        categorized_articles = categorizer.categorize_articles(raw_articles)
        print(categorized_articles)

        # === STEP 5: Insert into DB ===
        repo = ArticleRepository()
        inserted_count = 0
        for article in categorized_articles:
            if repo.insert_if_new(article):
                inserted_count += 1

        print(f"Inserted {inserted_count} new articles.")

        # === STEP 6: Update Notifications ===
        updater = NotificationsUpdater()
        updater.update_notifications_for_all_users()

        # === STEP 7: Read notifications for user ===
        viewer = NotificationsViewer()
        notifications = viewer.get_user_notifications(email)
        assert notifications and len(notifications) > 0

        # === STEP 8: Email Notification ===
        body = f"Hi {username},\n\nPlease check out the latest news articles for your preferred categories:\n\n"
        for article in notifications[:5]:
            body += f"- {article['title']}\n"
        body += "\nLogin to check more.\n\nRegards,\nNews Aggregator"

        email_service = EmailService()
        sent = email_service.send_email(
            to_email=email,
            subject="Your News Digest",
            body=body
        )
        assert sent is True
