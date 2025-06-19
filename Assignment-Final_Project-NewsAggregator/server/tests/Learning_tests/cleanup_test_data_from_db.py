from server.db.db_connection import DBConnection


class DBCleanupService:
    def run_cleanup(self):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("DELETE FROM keywords WHERE user_id IN (SELECT user_id FROM users WHERE email = 'testuser@example.com')")
            cur.execute("DELETE FROM users WHERE email = 'testuser@example.com'")
            cur.execute("DELETE FROM articles")
            cur.execute("DELETE FROM categories WHERE name = 'Politics'")
            db.commit()
            print("Cleanup complete.")
        finally:
            cur.close()
            db.close()


if __name__ == "__main__":
    cleaner = DBCleanupService()
    cleaner.run_cleanup()
