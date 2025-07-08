import unittest
from unittest.mock import MagicMock
from server.services.search_service import SearchService


class TestSearchService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = SearchService(repo=self.mock_repo)

    def test_search_by_category(self):
        self.mock_repo.search_by_category.return_value = ["a1", "a2"]
        result = self.service.search_by_category("cat")
        self.mock_repo.search_by_category.assert_called_with("cat")
        self.assertEqual(result, ["a1", "a2"])

    def test_search_by_category_exception(self):
        self.mock_repo.search_by_category.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.search_by_category("cat")

    def test_search_by_keyword(self):
        self.mock_repo.search_by_keyword.return_value = ["a1"]
        result = self.service.search_by_keyword("kw")
        self.mock_repo.search_by_keyword.assert_called_with("kw")
        self.assertEqual(result, ["a1"])

    def test_search_by_keyword_exception(self):
        self.mock_repo.search_by_keyword.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.search_by_keyword("kw")

    def test_search_by_date(self):
        self.mock_repo.search_by_date.return_value = ["a1"]
        result = self.service.search_by_date("2025-07-07")
        self.mock_repo.search_by_date.assert_called_with("2025-07-07")
        self.assertEqual(result, ["a1"])

    def test_search_by_date_exception(self):
        self.mock_repo.search_by_date.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            self.service.search_by_date("2025-07-07")


if __name__ == "__main__":
    unittest.main()
