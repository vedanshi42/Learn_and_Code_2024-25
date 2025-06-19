from server.db.db_connection import DBConnection


class NotificationRepository:
    def replace_notifications_for_user(self, user_id: int, articles: list):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            # Clear old notifications
            cur.execute("DELETE FROM user_notifications WHERE user_id = %s", (user_id,))

            # Insert new ones
            for article in articles:
                cur.execute(
                    "INSERT INTO user_notifications (user_id, article_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (user_id, article['article_id'])
                )

            db.commit()
        finally:
            cur.close()
            db.close()

    def get_notifications_for_user(self, email: str) -> list:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT a.article_id, a.title, a.source_url, a.date_published
                FROM user_notifications n
                JOIN users u ON n.user_id = u.user_id
                JOIN articles a ON n.article_id = a.article_id
                WHERE u.email = %s
                ORDER BY a.date_published DESC
            """, (email,))
            return cur.fetchall()
        finally:
            cur.close()
            db.close()
