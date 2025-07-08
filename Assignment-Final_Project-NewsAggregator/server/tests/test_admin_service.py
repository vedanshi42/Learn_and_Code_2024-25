import unittest
from unittest.mock import MagicMock
from server.services.admin_service import AdminService


class TestAdminService(unittest.TestCase):
    def setUp(self):
        self.external_repo = MagicMock()
        self.category_repo = MagicMock()
        self.keyword_repo = MagicMock()
        self.article_repo = MagicMock()
        self.service = AdminService(
            external_repo=self.external_repo,
            category_repo=self.category_repo,
            keyword_repo=self.keyword_repo,
            article_repo=self.article_repo,
        )

    def test_get_external_keys(self):
        self.external_repo.get_all_keys.return_value = ["key1"]
        assert self.service.get_external_keys() == ["key1"]

    def test_update_api_key(self):
        self.service.update_api_key("api", "key")
        self.external_repo.update_api_key.assert_called_with("api", "key")

    def test_get_all_categories(self):
        self.category_repo.get_all_categories_with_status.return_value = ["cat"]
        assert self.service.get_all_categories() == ["cat"]

    def test_add_category(self):
        self.service.add_category("cat")
        self.category_repo.add_category.assert_called_with("cat")

    def test_disable_category(self):
        self.service.disable_category("cat")
        self.category_repo.disable_category.assert_called_with("cat")

    def test_get_all_keywords(self):
        self.keyword_repo.get_all_keywords_with_status.return_value = ["kw"]
        assert self.service.get_all_keywords() == ["kw"]

    def test_disable_keyword_globally(self):
        self.service.disable_keyword_globally("kw")
        self.keyword_repo.disable_keyword_globally.assert_called_with("kw")

    def test_get_reported_articles(self):
        self.article_repo.get_reported_articles_with_counts.return_value = ["art"]
        assert self.service.get_reported_articles() == ["art"]

    def test_delete_article(self):
        self.service.delete_article(1, 2)
        self.article_repo.delete_article.assert_called_with(1, 2)

    def test_get_external_statuses(self):
        self.external_repo.get_all_statuses.return_value = ["status"]
        assert self.service.get_external_statuses() == ["status"]

    def test_repo_exceptions(self):
        self.external_repo.get_all_keys.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.get_external_keys()
        self.category_repo.get_all_categories_with_status.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.get_all_categories()
        self.keyword_repo.get_all_keywords_with_status.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.get_all_keywords()
        self.article_repo.get_reported_articles_with_counts.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.get_reported_articles()
        self.article_repo.delete_article.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.delete_article(1, 2)
        self.external_repo.get_all_statuses.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.get_external_statuses()


if __name__ == "__main__":
    unittest.main()
