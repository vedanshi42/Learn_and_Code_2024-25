from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.user_saved_article_queries import (
    SAVE_BY_ID,
    DELETE_BY_ID,
    GET_SAVED_ARTICLES,
)
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger
from server.interfaces.repository_interfaces.i_user_saved_article_repository import (
    IUserSavedArticleRepository,
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


class UserSavedArticleRepository(IUserSavedArticleRepository):
    def save_by_id(self, user_id, article_id):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(SAVE_BY_ID, (user_id, article_id))

                db.commit()
                news_agg_logger(
                    20, f"User saved article {article_id} for user {user_id}"
                )
                return True
        except Exception as e:
            news_agg_logger(20, f"Failed to save article: {e}")
            raise RepositoryException(f"Failed to save article: {e}")

    def delete_by_id(self, user_id, article_id):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(DELETE_BY_ID, (article_id, user_id))

                db.commit()
        except Exception as e:
            news_agg_logger(40, f"Failed to delete saved article: {e}")
            raise RepositoryException(f"Failed to delete saved article: {e}")

    def get_saved_articles(self, user_id):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_SAVED_ARTICLES, (user_id,))
                rows = cur.fetchall()

                return [
                    {
                        "article_id": row["article_id"],
                        "title": row["title"],
                        "content": row["content"],
                        "source_url": row["source_url"],
                        "date_published": row["date_published"].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                    for row in rows
                ]
        except Exception as e:
            news_agg_logger(40, f"Failed to get saved articles: {e}")
            raise RepositoryException(f"Failed to get saved articles: {e}")
