from server.db.db_connection import DBConnection
import bcrypt
from datetime import datetime, UTC


class DBSeeder:
    def __init__(self):
        self.db = DBConnection()
        self.cur = self.db.get_cursor()

    def seed_admin_user(self):
        admin_email = "admin@newsagg.com"
        admin_pass = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        self.cur.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
        """, ("Admin", admin_email, admin_pass, "admin"))

    def seed_categories(self):
        default_categories = ["All", "Technology", "Politics", "Sports", "World", "Business"]
        for cat in default_categories:
            self.cur.execute("""
                INSERT INTO categories (name)
                VALUES (%s)
                ON CONFLICT DO NOTHING;
            """, (cat,))

    def seed_external_apis(self):
        apis = [
            ("newsapi", "a2aa9260eae046beb3122caa2754f6be"),
            ("thenewsapi", "Z4QNmyQFjKpabIObLNdKKCAGpLqTjAGMazzMl8jL")
        ]
        for name, key in apis:
            self.cur.execute("""
                INSERT INTO external_api_servers (api_name, api_key, status, last_accessed)
                VALUES (%s, %s, 'Active', %s)
                ON CONFLICT (api_name) DO NOTHING;
            """, (name, key, datetime.now(UTC)))

    def run_all(self):
        self.seed_admin_user()
        self.seed_categories()
        self.seed_external_apis()
        self.db.commit()
        print("Database seeded successfully.")


if __name__ == "__main__":
    DBSeeder().run_all()
