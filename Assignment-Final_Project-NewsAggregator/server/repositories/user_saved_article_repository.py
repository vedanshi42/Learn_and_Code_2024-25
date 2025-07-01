from server.db.db_connection import DBConnection


class UserSavedArticleRepository:
    def save_by_id(self, user_id, article_id):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                INSERT INTO user_saved_articles (user_id, article_id, title, content, category, source_url, date_published)
                SELECT %s, article_id, title, content, c.name, source_url, date_published
                FROM articles a
                JOIN categories c ON a.category_id = c.category_id
                WHERE a.article_id = %s
                ON CONFLICT DO NOTHING
            """, (user_id, article_id))
            db.commit()
        finally:
            cur.close()
            db.close()

    def delete_by_id(self, user_id, article_id):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                DELETE FROM user_saved_articles
                WHERE article_id = %s AND user_id = %s
            """, (article_id, user_id))
            db.commit()
        finally:
            cur.close()
            db.close()

    def get_saved_articles(self, user_id):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT article_id, title, content, source_url, date_published
                        FROM user_saved_articles
                WHERE user_id = %s
                ORDER BY date_published DESC
            """, (user_id,))

            rows = cur.fetchall()

            return [
                {
                    "article_id": row["article_id"],
                    "title": row["title"],
                    "content": row["content"],
                    "source_url": row["source_url"],
                    "date_published": row["date_published"].strftime("%Y-%m-%d %H:%M:%S")
                }
                for row in rows]
        finally:
            cur.close()
            db.close()
