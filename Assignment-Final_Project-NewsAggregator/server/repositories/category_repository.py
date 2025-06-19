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
            # Get user_id
            cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if not user:
                raise ValueError("User not found.")
            user_id = user['user_id']

            # Get category_id
            cur.execute("SELECT category_id FROM categories WHERE name = %s", (category,))
            cat = cur.fetchone()
            if not cat:
                raise ValueError("Category not found.")
            category_id = cat['category_id']

            # Insert into user_categories
            cur.execute("""
                INSERT INTO user_categories (user_id, category_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (user_id, category_id))

            db.commit()
        finally:
            cur.close()
            db.close()

    def get_user_categories(self, user_id):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("SELECT category_id FROM user_categories WHERE user_id = %s", (user_id,))
            category_ids = [row["category_id"] for row in cur.fetchall()]
            cur.execute("SELECT name FROM categories WHERE category_id = ANY(%s)", (category_ids,))
            categories = [row["name"] for row in cur.fetchall()]
            return categories
        finally:
            cur.close()
            db.close()
