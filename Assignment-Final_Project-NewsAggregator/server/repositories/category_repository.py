from server.db.db_connection import DBConnection


class CategoryRepository:
    def add_category(self, name: str) -> None:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING", (name,))
            db.commit()
        finally:
            cur.close()
            db.close()

    def get_all_categories(self) -> list:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("SELECT name FROM categories")
            return [row["name"] for row in cur.fetchall()]
        finally:
            cur.close()
            db.close()

    def add_if_not_exists(self, category_name: str):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                INSERT INTO categories (name)
                VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (category_name,))
            db.commit()
        finally:
            cur.close()
            db.close()

    def subscribe_user_to_category(self, email: str, category: str):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if not user:
                raise ValueError("User not found.")
            user_id = user['user_id']

            cur.execute("SELECT category_id FROM categories WHERE name = %s", (category,))
            cat = cur.fetchone()
            if not cat:
                raise ValueError("Category not found.")
            category_id = cat['category_id']

            cur.execute("""
                INSERT INTO user_categories (user_id, category_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (user_id, category_id))

            db.commit()
        finally:
            cur.close()
            db.close()

    def toggle_category(self, email: str, category: str):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                UPDATE user_categories
                SET is_enabled = FALSE
                WHERE user_id = (SELECT user_id FROM users WHERE email = %s)
                AND category_id = (SELECT category_id FROM categories WHERE name = %s)
            """, (email, category))
            db.commit()
        finally:
            cur.close()
            db.close()

    def get_user_categories(self, email: str) -> list[dict]:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if not user:
                return []

            cur.execute("""
                SELECT c.name, uc.is_enabled FROM user_categories uc
                JOIN categories c ON uc.category_id = c.category_id
                WHERE uc.user_id = %s
            """, (user["user_id"],))
            return [{"name": row["name"], "is_enabled": row["is_enabled"]} for row in cur.fetchall()]
        finally:
            cur.close()
            db.close()