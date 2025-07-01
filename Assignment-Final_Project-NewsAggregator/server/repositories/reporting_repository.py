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

            db.commit()
            return True

        finally:
            cur.close()
            db.close()
