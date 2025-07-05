from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.category_queries import (
    ADD_CATEGORY, GET_ALL_CATEGORIES, GET_ALL_CATEGORIES_WITH_STATUS, ADD_IF_NOT_EXISTS,
    GET_CATEGORY_ID, SUBSCRIBE_USER_TO_CATEGORY, GET_ADMIN_DISABLED_CATEGORIES,
    TOGGLE_USER_CATEGORY, GET_CATEGORY_ID_BY_NAME, DISABLE_CATEGORY, DISABLE_USER_CATEGORY,
    GET_USER_CATEGORIES_BY_ID, GET_USER
)
from server.exceptions.repository_exception import NotFoundException, DisabledEntityException, RepositoryException
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


class CategoryRepository:
    def add_category(self, name: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(ADD_CATEGORY, (name,))
                db.commit()
                news_agg_logger(20, f"Category added: {name}")
        except Exception as e:
            news_agg_logger(40, f"Failed to add category: {e}")
            raise RepositoryException(f"Failed to add category: {e}")

    def get_all_categories(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ALL_CATEGORIES)
                result = [row["name"] for row in cur.fetchall()]
                news_agg_logger(20, f"Fetched all categories. Count: {len(result)}")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to fetch all categories: {e}")
            raise RepositoryException(f"Failed to fetch all categories: {e}")

    def get_all_categories_with_status(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ALL_CATEGORIES_WITH_STATUS)
                result = [{"name": row["name"], "status": row["status"]} for row in cur.fetchall()]
                news_agg_logger(20, f"Fetched all categories with status. Count: {len(result)}")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to fetch categories with status: {e}")
            raise RepositoryException(f"Failed to fetch categories with status: {e}")

    def add_if_not_exists(self, category_name: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(ADD_IF_NOT_EXISTS, (category_name,))
                db.commit()
                news_agg_logger(20, f"Category added if not exists: {category_name}")
        except Exception as e:
            news_agg_logger(40, f"Failed to add category if not exists: {e}")
            raise RepositoryException(f"Failed to add category if not exists: {e}")

    def subscribe_user_to_category(self, user_id: int, category: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_USER, (user_id,))
                user = cur.fetchone()

                if not user:
                    news_agg_logger(40, f"User not found for subscribe: {user_id}")
                    raise NotFoundException("User not found.")

                cur.execute(GET_CATEGORY_ID, (category,))
                cat = cur.fetchone()

                if not cat:
                    news_agg_logger(40, f"Category not found for subscribe: {category}")
                    raise NotFoundException("Category not found.")

                category_id = cat['category_id']
                cur.execute(SUBSCRIBE_USER_TO_CATEGORY, (user_id, category_id))
                db.commit()

                news_agg_logger(20, f"User {user_id} subscribed to category {category}")
        except NotFoundException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to subscribe user to category: {e}")
            raise RepositoryException(f"Failed to subscribe user to category: {e}")

    def toggle_category(self, user_id: int, category: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ADMIN_DISABLED_CATEGORIES)

                admin_disabled_categories = [row['name'] for row in cur.fetchall()]

                if category in admin_disabled_categories:
                    news_agg_logger(40, f"Attempt to toggle admin-disabled category: {category}")
                    raise DisabledEntityException('Category disabled by admin')
                cur.execute(TOGGLE_USER_CATEGORY, (user_id, category))

                db.commit()
                news_agg_logger(20, f"Toggled category {category} for user {user_id}")
        except DisabledEntityException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to toggle category: {e}")
            raise RepositoryException(f"Failed to toggle category: {e}")

    def get_user_categories(self, user_id: int):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_USER_CATEGORIES_BY_ID, (user_id,))
                result = [{"name": row["name"], "is_enabled": row["is_enabled"]} for row in cur.fetchall()]

                news_agg_logger(20, f"Fetched user categories for user {user_id}. Count: {len(result)}")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to fetch user categories: {e}")
            raise RepositoryException(f"Failed to fetch user categories: {e}")

    def disable_category(self, name: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_CATEGORY_ID_BY_NAME, (name,))
                row = cur.fetchone()

                if not row:
                    news_agg_logger(40, f"Category not found for disable: {name}")
                    raise NotFoundException(f"Category '{name}' not found.")

                category_id = row['category_id']
                cur.execute(DISABLE_CATEGORY, (category_id,))
                cur.execute(DISABLE_USER_CATEGORY, (category_id,))

                db.commit()
                news_agg_logger(20, f"Disabled category {name} (id {category_id})")
        except NotFoundException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to disable category: {e}")
            raise RepositoryException(f"Failed to disable category: {e}")
