from abc import ABC, abstractmethod


class IReportingRepository(ABC):

    @abstractmethod
    def report_article(self, user_id: int, article_id: int):
        pass
