from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.notification_queries import (
    DELETE_USER_NOTIFICATIONS,
    INSERT_USER_NOTIFICATION,
    GET_USER,
    GET_USER_ENABLED_CATEGORIES,
    GET_USER_ENABLED_KEYWORDS,
)
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger
from server.interfaces.repository_interfaces.i_notification_repository import (
    INotificationRepository,
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


class NotificationRepository(INotificationRepository):
    def replace_notifications_for_user(self, user_id: int, articles: list):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(DELETE_USER_NOTIFICATIONS, (user_id,))

                for article in articles:
                    cur.execute(
                        INSERT_USER_NOTIFICATION, (user_id, article["article_id"])
                    )

                db.commit()
                news_agg_logger(20, f"Notifications replaced for user {user_id}")
        except Exception as e:
            news_agg_logger(40, f"Failed to replace notifications: {e}")
            raise RepositoryException(f"Failed to replace notifications: {e}")

    def get_notifications_for_user(self, user_id: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_USER, (user_id,))
                user = cur.fetchone()

                if not user:
                    news_agg_logger(20, f"No user found with ID {user_id}")
                    return []

                cur.execute(GET_USER_ENABLED_CATEGORIES, (user_id,))
                cat_ids = [row["category_id"] for row in cur.fetchall()]

                cur.execute(GET_USER_ENABLED_KEYWORDS, (user_id,))
                keywords = [row["keyword"] for row in cur.fetchall()]

                query_conditions = []
                query_params = []

                if cat_ids:
                    query_conditions.append("a.category_id = ANY(%s)")
                    query_params.append(cat_ids)

                if keywords:
                    keyword_clauses = []
                    for kw in keywords:
                        keyword_clauses.append(
                            "(a.title ILIKE %s OR a.content ILIKE %s)"
                        )
                        query_params.extend([f"%{kw}%", f"%{kw}%"])
                    query_conditions.append(" OR ".join(keyword_clauses))

                if not query_conditions:
                    news_agg_logger(
                        20,
                        f"No notifications found for user {user_id} due to empty conditions",
                    )
                    return []

                base_query = """SELECT DISTINCT
                                a.article_id, a.title, a.source_url, a.date_published
                                FROM articles a WHERE """
                full_query = (
                    base_query
                    + " OR ".join(query_conditions)
                    + " ORDER BY a.date_published DESC"
                )
                cur.execute(full_query, query_params)

                notifications = [
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
                news_agg_logger(20, f"Notifications retrieved for user {user_id}")
                return notifications
        except Exception as e:
            news_agg_logger(40, f"Failed to get notifications for user: {e}")
            raise RepositoryException(f"Failed to get notifications for user: {e}")
