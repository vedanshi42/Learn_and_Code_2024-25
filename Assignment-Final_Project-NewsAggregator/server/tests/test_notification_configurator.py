import unittest
from unittest.mock import patch
from server.services.notifications_service.notification_configurator import (
    NotificationsConfigurator,
)


class TestNotificationsConfigurator(unittest.TestCase):
    def setUp(self):
        self.service = NotificationsConfigurator()

    @patch(
        "server.services.notifications_service.notification_configurator.KeywordRepository"
    )
    def test_add_keyword_for_user(self, mock_repo):
        self.service.keyword_repo = mock_repo.return_value
        self.service.add_keyword_for_user(1, "kw")
        mock_repo.return_value.add_keyword_for_user.assert_called_with(1, "kw")

    @patch(
        "server.services.notifications_service.notification_configurator.CategoryRepository"
    )
    def test_add_category_for_user(self, mock_repo):
        self.service.category_repo = mock_repo.return_value
        self.service.add_category_for_user(1, "cat")
        mock_repo.return_value.subscribe_user_to_category.assert_called_with(1, "cat")

    @patch(
        "server.services.notifications_service.notification_configurator.CategoryRepository"
    )
    def test_toggle_category(self, mock_repo):
        self.service.category_repo = mock_repo.return_value
        self.service.toggle_category(1, "cat")
        mock_repo.return_value.toggle_category.assert_called_with(1, "cat")

    @patch(
        "server.services.notifications_service.notification_configurator.KeywordRepository"
    )
    def test_toggle_keyword(self, mock_repo):
        self.service.keyword_repo = mock_repo.return_value
        self.service.toggle_keyword(1, "kw")
        mock_repo.return_value.toggle_keyword.assert_called_with(1, "kw")

    @patch(
        "server.services.notifications_service.notification_configurator.KeywordRepository"
    )
    def test_get_user_keywords(self, mock_repo):
        mock_repo.return_value.get_keywords_for_user.return_value = ["kw"]
        self.service.keyword_repo = mock_repo.return_value
        result = self.service.get_user_keywords(1)
        self.assertEqual(result, ["kw"])

    @patch(
        "server.services.notifications_service.notification_configurator.CategoryRepository"
    )
    def test_get_user_categories(self, mock_repo):
        mock_repo.return_value.get_user_categories.return_value = ["cat"]
        self.service.category_repo = mock_repo.return_value
        result = self.service.get_user_categories(1)
        self.assertEqual(result, ["cat"])

    @patch(
        "server.services.notifications_service.notification_configurator.NotificationRepository"
    )
    def test_get_user_notifications(self, mock_repo):
        mock_repo.return_value.get_notifications_for_user.return_value = ["notif"]
        self.service.notification_repo = mock_repo.return_value
        result = self.service.get_user_notifications(1)
        self.assertEqual(result, ["notif"])


if __name__ == "__main__":
    unittest.main()
