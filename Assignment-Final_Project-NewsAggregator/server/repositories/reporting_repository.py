from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.reporting_queries import REPORT_ARTICLE
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger
from server.interfaces.repository_interfaces.i_reporting_repository import (
    IReportingRepository,
)


@contextmanager
def get_db_cursor():
    db = DBConnection()
    cur = db.get_cursor()
    try:
        yield cur, db
    finally:
        cur.close()
        db.close()


class ReportingService(IReportingRepository):
    def report_article(self, user_id: int, article_id: int):
        try:
            with get_db_cursor() as (cur, db):

                cur.execute(REPORT_ARTICLE, (user_id, article_id))
                db.commit()
                news_agg_logger(
                    20, f"Article reported: user_id={user_id}, article_id={article_id}"
                )

                return True
        except Exception as e:
            news_agg_logger(40, f"Failed to report article: {e}")
            raise RepositoryException(f"Failed to report article: {e}")
