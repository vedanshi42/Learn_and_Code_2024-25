from server.db.db_connection import DBConnection


class FeedbackService:
    def like_article(self, user_id: int, article_id: int):
        self._add_feedback(user_id, article_id, 'like')

    def dislike_article(self, user_id: int, article_id: int):
        self._add_feedback(user_id, article_id, 'dislike')

    def _add_feedback(self, user_id, article_id, action):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT feedback_type FROM user_article_feedback
                WHERE user_id = %s AND article_id = %s
            """, (user_id, article_id))
            existing = cur.fetchone()

            if existing:
                if existing[0] == action:
                    return
                else:
                    self._update_feedback_counts(cur, article_id, existing[0], -1)
                    self._update_feedback_counts(cur, article_id, action, 1)
                    cur.execute("""
                        UPDATE user_article_feedback
                        SET feedback_type = %s
                        WHERE user_id = %s AND article_id = %s
                    """, (action, user_id, article_id))
            else:
                cur.execute("""
                    INSERT INTO user_article_feedback (user_id, article_id, feedback_type)
                    VALUES (%s, %s, %s)
                """, (user_id, article_id, action))
                self._update_feedback_counts(cur, article_id, action, 1)

            db.commit()
        finally:
            cur.close()
            db.close()

    def _update_feedback_counts(self, cur, article_id, action, delta):
        column = "likes" if action == "like" else "dislikes"
        cur.execute(f"""
            INSERT INTO feedback (article_id, {column})
            VALUES (%s, %s)
            ON CONFLICT (article_id) DO UPDATE
            SET {column} = feedback.{column} + %s
        """, (article_id, delta, delta))

    def get_feedback_counts(self, article_id):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT likes, dislikes FROM feedback WHERE article_id = %s
            """, (article_id,))
            return cur.fetchone() or (0, 0)
        finally:
            cur.close()
            db.close()
