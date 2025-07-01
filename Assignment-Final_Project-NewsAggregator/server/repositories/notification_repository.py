from server.db.db_connection import DBConnection
from server.decorators.personalization_decorators import personalize_notifications


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

    @personalize_notifications
    def get_notifications_for_user(self, email: str) -> list:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            # Get user_id
            cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if not user:
                return []

            user_id = user["user_id"]

            # Get enabled categories
            cur.execute("""
                SELECT category_id FROM user_categories
                WHERE user_id = %s AND is_enabled = TRUE
            """, (user_id,))
            cat_ids = [row["category_id"] for row in cur.fetchall()]

            # Get enabled keywords
            cur.execute("""
                SELECT keyword FROM keywords
                WHERE user_id = %s AND is_enabled = TRUE
            """, (user_id,))
            keywords = [row["keyword"] for row in cur.fetchall()]

            # Prepare base query
            base_query = """
                SELECT DISTINCT a.article_id, a.title, a.source_url, a.date_published
                FROM articles a
                WHERE
            """
            query_conditions = []
            query_params = []

            if cat_ids:
                query_conditions.append("a.category_id = ANY(%s)")
                query_params.append(cat_ids)

            if keywords:
                keyword_clauses = []
                for kw in keywords:
                    keyword_clauses.append("(a.title ILIKE %s OR a.content ILIKE %s)")
                    query_params.extend([f"%{kw}%", f"%{kw}%"])
                query_conditions.append(" OR ".join(keyword_clauses))

            # If no filters, return empty (user hasn’t enabled anything)
            if not query_conditions:
                return []

            full_query = base_query + " OR ".join(query_conditions) + " ORDER BY a.date_published DESC"
            cur.execute(full_query, query_params)

            return [
                {
                    "article_id": row["article_id"],
                    "title": row["title"],
                    "source_url": row["source_url"],
                    "date_published": row["date_published"].strftime("%Y-%m-%d %H:%M:%S")
                }
                for row in cur.fetchall()
            ]
        finally:
            cur.close()
            db.close()
