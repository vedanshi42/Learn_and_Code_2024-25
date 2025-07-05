from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.keyword_queries import (
    ADD_KEYWORD_FOR_USER, GET_ADMIN_DISABLED_KEYWORDS, TOGGLE_KEYWORD,
    GET_KEYWORDS_FOR_USER, GET_ALL_KEYWORDS_WITH_STATUS,
    DISABLE_KEYWORD_GLOBALLY, DISABLE_KEYWORD_FOR_ALL_USERS
)
from server.exceptions.repository_exception import DisabledEntityException, RepositoryException
from server.config.logging_config import news_agg_logger


@contextmanager
def get_db_cursor():
    db = DBConnection()
    cur = db.get_cursor()
    try:
        yield cur, db
    finally:
        cur.close()
        db.close()


class KeywordRepository:
    def add_keyword_for_user(self, user_id: int, keyword: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(ADD_KEYWORD_FOR_USER, (user_id, keyword))
                db.commit()

                news_agg_logger(20, f"Keyword added: {keyword} for user {user_id}")
                return True
        except Exception as e:
            news_agg_logger(40, f"Failed to add keyword: {e}")
            raise RepositoryException(f"Failed to add keyword: {e}")

    def toggle_keyword(self, user_id: int, keyword: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ADMIN_DISABLED_KEYWORDS)
                admin_disabled_keywords = [row['keyword'] for row in cur.fetchall()]

                if keyword in admin_disabled_keywords:
                    news_agg_logger(40, f"Attempt to toggle admin-disabled keyword: {keyword}")
                    raise DisabledEntityException('Keyword disabled by admin')

                cur.execute(TOGGLE_KEYWORD, (user_id, keyword))

                db.commit()
                news_agg_logger(20, f"Toggled keyword {keyword} for user {user_id}")
        except DisabledEntityException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to toggle keyword: {e}")
            raise RepositoryException(f"Failed to toggle keyword: {e}")

    def get_keywords_for_user(self, user_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_KEYWORDS_FOR_USER, (user_id,))
                result = [{"keyword": row["keyword"], "is_enabled": row["is_enabled"]} for row in cur.fetchall()]

                news_agg_logger(20, f"Fetched keywords for user {user_id}. Count: {len(result)}")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to get keywords for user {user_id}: {e}")
            raise RepositoryException(f"Failed to get keywords for user: {e}")

    def get_all_keywords_with_status(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ALL_KEYWORDS_WITH_STATUS)
                result = [{"keyword": row["keyword"], "status": row['status']} for row in cur.fetchall()]

                news_agg_logger(20, f"Fetched all keywords with status. Count: {len(result)}")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to get all keywords with status: {e}")
            raise RepositoryException(f"Failed to get all keywords with status: {e}")

    def disable_keyword_globally(self, word: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(DISABLE_KEYWORD_GLOBALLY, (word,))

                cur.execute(DISABLE_KEYWORD_FOR_ALL_USERS, (word,))

                db.commit()
                news_agg_logger(20, f"Globally disabled keyword: {word}")
        except Exception as e:
            news_agg_logger(40, f"Failed to disable keyword globally: {e}")
            raise RepositoryException(f"Failed to disable keyword globally: {e}")
