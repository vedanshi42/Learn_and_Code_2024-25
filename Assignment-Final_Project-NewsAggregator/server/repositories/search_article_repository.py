from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.search_article_queries import (
    FIND_ARTICLES_BY_CATEGORY_OR_KEYWORD,
    SEARCH_BY_KEYWORD,
    SEARCH_BY_CATEGORY,
    SEARCH_BY_DATE,
)
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger
from server.interfaces.repository_interfaces.i_search_article_repository import (
    ISearchArticleRepository,
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


class SearchArticleRepository(ISearchArticleRepository):
    def find_articles_by_category_or_keyword(self, category=None, keyword=None):
        try:
            with get_db_cursor() as (cur, db):
                category_pattern = f"%{category}%" if category else ""
                keyword_pattern = f"%{keyword}%" if keyword else ""

                cur.execute(
                    FIND_ARTICLES_BY_CATEGORY_OR_KEYWORD,
                    (category_pattern, keyword_pattern, keyword_pattern),
                )
                news_agg_logger(
                    20,
                    f"Searched articles by category or keyword: category={category}, keyword={keyword}",
                )
                return cur.fetchall()

        except Exception as e:
            news_agg_logger(
                40, f"Failed to search articles by category or keyword: {e}"
            )
            raise RepositoryException(
                f"Failed to search articles by category or keyword: {e}"
            )

    def search_by_keyword(self, keyword):
        try:
            with get_db_cursor() as (cur, db):
                pattern = f"%{keyword}%"
                cur.execute(SEARCH_BY_KEYWORD, (pattern, pattern))
                return [
                    {
                        "article_id": row["article_id"],
                        "title": row["title"],
                        "source_url": row["source_url"],
                        "date_published": row["date_published"].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                    for row in cur.fetchall()
                ]
        except Exception as e:
            raise RepositoryException(f"Failed to search articles by keyword: {e}")

    def search_by_category(self, category):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(SEARCH_BY_CATEGORY, (category,))
                return [
                    {
                        "article_id": row["article_id"],
                        "title": row["title"],
                        "source_url": row["source_url"],
                        "date_published": row["date_published"].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                    for row in cur.fetchall()
                ]
        except Exception as e:
            raise RepositoryException(f"Failed to search articles by category: {e}")

    def search_by_date(self, date):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(SEARCH_BY_DATE, (date,))
                return [
                    {
                        "article_id": row["article_id"],
                        "title": row["title"],
                        "source_url": row["source_url"],
                        "date_published": row["date_published"].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                    for row in cur.fetchall()
                ]
        except Exception as e:
            raise RepositoryException(f"Failed to search articles by date: {e}")
