import unittest
from unittest.mock import patch
from server.services.notifications_service.notification_updater import NotificationsUpdater


class TestNotificationsUpdater(unittest.TestCase):
    def setUp(self):
        self.service = NotificationsUpdater()

    @patch('server.services.notifications_service.notification_updater.UserRepository')
    @patch('server.services.notifications_service.notification_updater.KeywordRepository')
    @patch('server.services.notifications_service.notification_updater.CategoryRepository')
    @patch('server.services.notifications_service.notification_updater.SearchArticleRepository')
    @patch('server.services.notifications_service.notification_updater.NotificationRepository')
    def test_update_notifications_for_all_users(self, mock_notif_repo, mock_search_repo, mock_cat_repo, mock_kw_repo, mock_user_repo):
        mock_user_repo.return_value.get_all_users.return_value = [{'user_id': 1, 'email': 'e'}]
        mock_kw_repo.return_value.get_keywords_for_user.return_value = ['kw']
        mock_cat_repo.return_value.get_user_categories.return_value = ['cat']
        mock_search_repo.return_value.find_articles_by_category_or_keyword.return_value = ['art']
        self.service.user_repo = mock_user_repo.return_value
        self.service.keyword_repo = mock_kw_repo.return_value
        self.service.category_repo = mock_cat_repo.return_value
        self.service.search_article_repo = mock_search_repo.return_value
        self.service.notification_repo = mock_notif_repo.return_value
        self.service.update_notifications_for_all_users()
        mock_notif_repo.return_value.replace_notifications_for_user.assert_called_with(1, ['art'])


if __name__ == '__main__':
    unittest.main()
