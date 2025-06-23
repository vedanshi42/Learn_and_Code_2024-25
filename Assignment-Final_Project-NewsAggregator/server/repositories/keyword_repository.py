from server.db.db_connection import DBConnection


class KeywordRepository:
    def add_keyword_for_user(self, email: str, keyword: str) -> None:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                INSERT INTO keywords (user_id, keyword, is_enabled)
                VALUES (
                    (SELECT user_id FROM users WHERE email = %s),
                    %s,
                    TRUE
                ) ON CONFLICT DO NOTHING
            """, (email, keyword))
            db.commit()
        finally:
            cur.close()
            db.close()

    def toggle_keyword(self, email: str, keyword: str):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                UPDATE keywords
                SET is_enabled = FALSE
                WHERE user_id = (SELECT user_id FROM users WHERE email = %s)
                AND keyword = %s
            """, (email, keyword))
            db.commit()
        finally:
            cur.close()
            db.close()

    def get_keywords_for_user(self, email: str) -> list[dict]:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT keyword, is_enabled FROM keywords
                WHERE user_id = (SELECT user_id FROM users WHERE email = %s)
            """, (email,))
            return [{"keyword": row["keyword"], "is_enabled": row["is_enabled"]} for row in cur.fetchall()]
        finally:
            cur.close()
            db.close()
