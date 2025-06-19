from unittest.mock import patch, MagicMock
from server.services.notifications_service.notification_configurator import NotificationsConfigurator
from server.services.notifications_service.notification_updater import NotificationsUpdater
from server.services.notifications_service.notification_viewer import NotificationsViewer


class TestNotifications:
    @patch("server.services.notification_configurator.KeywordRepository")
    def test_add_keyword(self, MockKeywordRepo):
        mock_repo = MockKeywordRepo.return_value
        configurator = NotificationsConfigurator()
        configurator.add_keyword_for_user("user@example.com", "AI")
        mock_repo.add_keyword_for_user.assert_called_once()

    @patch("server.services.notification_updater.NotificationRepository")
    @patch("server.services.notification_updater.SearchArticleRepository")
    @patch("server.services.notification_updater.UserRepository")
    @patch("server.services.notification_updater.KeywordRepository")
    @patch("server.services.notification_updater.CategoryRepository")
    def test_update_notifications(self, MockCategoryRepo, MockKeywordsRepo, MockUserRepo, MockArticleRepo, MockNotificationsRepo):
        MockUserRepo.return_value.get_all_users.return_value = [{"user_id": 1, "email": "test@example.com"}]
        MockKeywordsRepo.return_value.get_keywords_for_user.return_value = ["AI"]
        MockCategoryRepo.return_value.get_user_categories.return_value = ["Tech"]
        MockArticleRepo.return_value.find_articles_by_category_or_keyword.return_value = [MagicMock(article_id=10)]
        updater = NotificationsUpdater()
        updater.update_notifications_for_all_users()
        MockNotificationsRepo.return_value.replace_notifications_for_user.assert_called_once()

    @patch("server.services.notification_viewer.NotificationRepository")
    def test_view_notifications(self, MockNotiRepo):
        MockNotiRepo.return_value.get_notifications_for_user.return_value = ["A1", "A2"]
        viewer = NotificationsViewer()
        result = viewer.get_user_notifications("test@example.com")
        assert result == ["A1", "A2"]
