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
            cur.execute("""SELECT keyword FROM keywords WHERE is_enabled_by_admin IS FALSE""")
            admin_disabled_keywords = [row['keyword'] for row in cur.fetchall()]

            if keyword in admin_disabled_keywords:
                raise ValueError('Keyword disabled by admin')
            else:
                cur.execute("""
                    UPDATE keywords
                    SET is_enabled = NOT is_enabled
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

    def get_all_keywords_with_status(self):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                SELECT keyword,
                    (CASE WHEN is_enabled_by_admin IS TRUE THEN 'Enabled'
                        ELSE 'Disabled'
                        END) AS status
                FROM keywords

                ORDER BY keyword
            """)
            return [{
                "keyword": row["keyword"],
                "status": row['status']}
                for row in cur.fetchall()]
        finally:
            cur.close()
            db.close()

    def disable_keyword_globally(self, word: str):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""UPDATE keywords
                        SET is_enabled_by_admin = NOT is_enabled_by_admin
                        WHERE keyword = %s""", (word,))
            db.commit()

            cur.execute("""
                UPDATE keywords
                SET is_enabled = NOT is_enabled
                WHERE keyword = %s
            """, (word,))
            db.commit()
        finally:
            cur.close()
            db.close()
