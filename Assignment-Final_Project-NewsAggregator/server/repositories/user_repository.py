from server.db.db_connection import DBConnection
from server.interfaces.i_user_repository import IUserRepository


class UserRepository(IUserRepository):
    def get_user_by_email(self, email: str):
        db = DBConnection()
        try:
            cur = db.get_cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            return user
        finally:
            db.close()

    def create_user(self, username, email, hashed_pw, role='user'):
        db = DBConnection()
        try:
            cur = db.get_cursor()
            cur.execute(
                """
                INSERT INTO users (username, email, password, role)
                VALUES (%s, %s, %s, %s) RETURNING user_id
                """,
                (username, email, hashed_pw, role)
            )
            user_role = cur.fetchone()['role']
            db.commit()
            cur.close()
            return user_role
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def email_exists(self, email: str):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            db.close()

    def get_all_users(self):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            return users
        except Exception as e:
            print(f'Cannot get users as table is empty or {e}')

        finally:
            cur.close()
            db.close()
