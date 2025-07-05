from datetime import datetime, UTC
from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.interfaces.repository_interfaces.i_external_api_repository import IExternalAPIRepository
from server.db.external_api_queries import (
    UPDATE_STATUS, GET_LAST_ACCESSED, GET_ALL_STATUSES, GET_ALL_KEYS, UPDATE_API_KEY, GET_API_KEYS
)
from server.exceptions.repository_exception import RepositoryException, APINameNotFoundException
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


class ExternalAPIRepository(IExternalAPIRepository):
    def update_status(self, name: str, status: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(UPDATE_STATUS, (status, datetime.now(UTC), name))

                if cur.rowcount == 0:
                    news_agg_logger(40, f"API name '{name}' not found for status update.")
                    raise APINameNotFoundException(f"API name '{name}' not found.")

                db.commit()
                news_agg_logger(20, f"Updated status for API '{name}' to '{status}'")
        except APINameNotFoundException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to update API status: {e}")
            raise RepositoryException(f"Failed to update API status: {e}")

    def get_last_accessed(self, name: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_LAST_ACCESSED, (name,))
                result = cur.fetchone()

                news_agg_logger(20, f"Fetched last accessed for API '{name}'")
                return result["last_accessed"] if result else datetime.now(UTC)
        except Exception as e:
            news_agg_logger(40, f"Failed to get last accessed for API '{name}': {e}")
            raise RepositoryException(f"Failed to get last accessed: {e}")

    def get_all_statuses(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ALL_STATUSES)

                result = [
                    {
                        "api_name": row["api_name"],
                        "status": row["status"],
                        "last_accessed": row["last_accessed"]
                    }
                    for row in cur.fetchall()
                ]

                news_agg_logger(20, f"Fetched all API statuses. Count: {len(result)}")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to get all statuses: {e}")
            raise RepositoryException(f"Failed to get all statuses: {e}")

    def get_all_keys(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ALL_KEYS)

                result = [
                    {
                        "api_name": row["api_name"],
                        "api_key": row["api_key"],
                        "last_accessed": row["last_accessed"]
                    }
                    for row in cur.fetchall()
                ]

                news_agg_logger(20, f"Fetched all API keys. Count: {len(result)}")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to get all keys: {e}")
            raise RepositoryException(f"Failed to get all keys: {e}")

    def update_api_key(self, api_name, api_key):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(UPDATE_API_KEY, (api_key, api_name))

                if cur.rowcount == 0:
                    news_agg_logger(40, f"API name '{api_name}' not found for API key update.")
                    raise APINameNotFoundException(f"API name '{api_name}' not found.")

                db.commit()
                news_agg_logger(20, f"Updated API key for '{api_name}'")
        except APINameNotFoundException:
            raise
        except Exception as e:
            news_agg_logger(40, f"Failed to update API key: {e}")
            raise RepositoryException(f"Failed to update API key: {e}")

    def get_api_keys(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_API_KEYS)
                result = {row['api_name']: row['api_key'] for row in cur.fetchall()}

                news_agg_logger(20, "External APIs details fetched")
                return result
        except Exception as e:
            news_agg_logger(40, f"Failed to call external API: {e}")
            raise RepositoryException(f"Failed to call external API: {e}")
