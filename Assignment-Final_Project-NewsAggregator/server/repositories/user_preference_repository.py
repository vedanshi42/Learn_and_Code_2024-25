from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.user_preference_queries import (
    GET_LIKED_CATEGORIES, GET_DISLIKED_CATEGORIES, GET_ENABLED_KEYWORDS, GET_LIKED_KEYWORDS, GET_DISLIKED_KEYWORDS, GET_SAVED_ARTICLE_CATEGORIES, GET_SAVED_ARTICLE_KEYWORDS
)
from server.interfaces.repository_interfaces.i_user_preference_repository import IUserPreferenceRepository
from server.exceptions.repository_exception import RepositoryException
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


class UserPreferenceRepository(IUserPreferenceRepository):
    def get_liked_categories(self, user_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_LIKED_CATEGORIES, (user_id,))
                liked = {row["name"] for row in cur.fetchall()}

                cur.execute(GET_SAVED_ARTICLE_CATEGORIES, (user_id,))
                saved = {row["name"] for row in cur.fetchall()}

                return liked.union(saved)
        except Exception as e:
            news_agg_logger(40, f"Failed to get liked categories for user_id={user_id}: {e}")
            raise RepositoryException(f"Failed to get liked categories: {e}")

    def get_disliked_categories(self, user_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_DISLIKED_CATEGORIES, (user_id,))
                disliked = {row["name"] for row in cur.fetchall()}

                return disliked
        except Exception as e:
            news_agg_logger(40, f"Failed to get disliked categories for user_id={user_id}: {e}")
            raise RepositoryException(f"Failed to get disliked categories: {e}")

    def get_liked_keywords(self, user_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ENABLED_KEYWORDS, (user_id,))
                enabled = {row["keyword"].lower() for row in cur.fetchall()}

                cur.execute(GET_LIKED_KEYWORDS, (user_id,))
                liked_titles, liked_contents = [], []

                for row in cur.fetchall():
                    liked_titles.extend(row['title'].split())
                    liked_contents.extend(row['content'].split())
                liked_keywords = set(kw for kw in (liked_titles + liked_contents) if len(kw) > 3)

                cur.execute(GET_SAVED_ARTICLE_KEYWORDS, (user_id,))
                saved_titles, saved_contents = [], []

                for row in cur.fetchall():
                    saved_titles.extend(row['title'].split())
                    saved_contents.extend(row['content'].split())
                saved_keywords = set(kw for kw in (saved_titles + saved_contents) if len(kw) > 3)

                return enabled.union(liked_keywords).union(saved_keywords)
        except Exception as e:
            news_agg_logger(40, f"Failed to get liked keywords for user_id={user_id}: {e}")
            raise RepositoryException(f"Failed to get liked keywords: {e}")

    def get_disliked_keywords(self, user_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_DISLIKED_KEYWORDS, (user_id, user_id))

                disliked_titles, disliked_contents = [], []

                for row in cur.fetchall():
                    disliked_titles.extend(row['title'].split())
                    disliked_contents.extend(row['content'].split())

                disliked_keywords = set(kw for kw in (disliked_titles + disliked_contents) if len(kw) > 3)

                return disliked_keywords
        except Exception as e:
            news_agg_logger(40, f"Failed to get disliked keywords for user_id={user_id}: {e}")
            raise RepositoryException(f"Failed to get disliked keywords: {e}")
