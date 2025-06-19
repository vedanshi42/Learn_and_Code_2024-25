from server.db.db_connection import DBConnection


class KeywordRepository:
    def add_keyword_for_user(self, email: str, keyword: str) -> None:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                INSERT INTO keywords (user_id, keyword)
                VALUES (
                    (SELECT user_id FROM users WHERE email = %s),
                    %s
                ) ON CONFLICT DO NOTHING
            """, (email, keyword))
            db.commit()
        finally:
            cur.close()
            db.close()

    def get_keywords_for_user(self, email: str) -> list:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT keyword FROM keywords
                WHERE user_id = (SELECT user_id FROM users WHERE email = %s)
            """, (email,))
            return [row["keyword"] for row in cur.fetchall()]
        finally:
            cur.close()
            db.close()
