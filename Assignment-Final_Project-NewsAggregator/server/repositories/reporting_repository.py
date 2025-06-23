from server.db.db_connection import DBConnection


class ReportingService:
    def report_article(self, user_id: int, article_id: int):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                INSERT INTO reported_articles (user_id, article_id)
                VALUES (%s, %s) ON CONFLICT DO NOTHING
            """, (user_id, article_id))

            cur.execute("""
                SELECT COUNT(*) FROM reported_articles WHERE article_id = %s
            """, (article_id,))
            report_count = cur.fetchone()[0]

            if report_count >= 15:
                cur.execute("DELETE FROM articles WHERE article_id = %s", (article_id,))
                print("Article deleted by system due to excessive reports.")
            db.commit()
        finally:
            cur.close()
            db.close()
