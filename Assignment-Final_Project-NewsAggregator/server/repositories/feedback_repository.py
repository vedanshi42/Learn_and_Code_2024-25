from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.feedback_queries import (
    SELECT_FEEDBACK_TYPE,
    UPDATE_USER_FEEDBACK,
    INSERT_USER_FEEDBACK,
)
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger
from server.interfaces.repository_interfaces.i_feedback_repository import (
    IFeedbackRepository,
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


class FeedbackService(IFeedbackRepository):
    def like_article(self, user_id: int, article_id: int):
        self._add_feedback(user_id, article_id, "like")

    def dislike_article(self, user_id: int, article_id: int):
        self._add_feedback(user_id, article_id, "dislike")

    def _add_feedback(self, user_id, article_id, action):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(SELECT_FEEDBACK_TYPE, (user_id, article_id))
                existing = cur.fetchone()

                if existing:
                    if existing["feedback_type"] == action:
                        return
                    else:
                        self._update_feedback_counts(
                            cur, article_id, existing["feedback_type"], -1
                        )
                        self._update_feedback_counts(cur, article_id, action, 1)
                        cur.execute(UPDATE_USER_FEEDBACK, (action, user_id, article_id))
                else:
                    cur.execute(INSERT_USER_FEEDBACK, (user_id, article_id, action))
                    self._update_feedback_counts(cur, article_id, action, 1)

                db.commit()
                news_agg_logger(20, f"Feedback submitted by user {user_id}")
                return True

        except Exception as e:
            news_agg_logger(40, f"Failed to submit feedback: {e}")
            raise RepositoryException(f"Failed to add feedback: {e}")

    def _update_feedback_counts(self, cur, article_id, action, delta):
        column = "likes" if action == "like" else "dislikes"

        query = f"""
            INSERT INTO feedback (article_id, {column})
            VALUES (%s, %s)
            ON CONFLICT (article_id) DO UPDATE
            SET {column} = feedback.{column} + %s
        """
        cur.execute(query, (article_id, delta, delta))
