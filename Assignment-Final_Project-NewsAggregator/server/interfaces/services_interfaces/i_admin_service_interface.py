from abc import ABC, abstractmethod


class IAdminService(ABC):
    @abstractmethod
    def get_external_keys(self):
        pass

    @abstractmethod
    def update_api_key(self, api_name, api_key):
        pass

    @abstractmethod
    def get_all_categories(self):
        pass

    @abstractmethod
    def add_category(self, name):
        pass

    @abstractmethod
    def disable_category(self, category_name):
        pass

    @abstractmethod
    def get_all_keywords(self):
        pass

    @abstractmethod
    def disable_keyword_globally(self, keyword):
        pass

    @abstractmethod
    def get_reported_articles(self):
        pass

    @abstractmethod
    def delete_article(self, user_id, article_id):
        pass

    @abstractmethod
    def get_external_statuses(self):
        pass
