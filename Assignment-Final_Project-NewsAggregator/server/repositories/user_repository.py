from contextlib import contextmanager
from server.db.db_connection import DBConnection
from server.db.user_queries import (
    GET_USER_BY_EMAIL, CREATE_USER, GET_USER_BY_EMAIL_AFTER_CREATE,
    EMAIL_EXISTS, GET_ALL_USERS
)
from server.interfaces.i_user_repository import IUserRepository
from server.exceptions.repository_exception import RepositoryException
from server.config.logging_config import news_agg_logger


@contextmanager
def get_db_cursor():
    db = DBConnection()
    cur = db.get_cursor()
    try:
        yield cur, db
    finally:
        cur.close()
        db.close()


class UserRepository(IUserRepository):
    def get_user_by_email(self, email: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_USER_BY_EMAIL, (email,))
                user = cur.fetchone()

                return dict(user) if user else None
        except Exception as e:
            raise RepositoryException(f"Failed to get user by email: {e}")

    def create_user(self, username, email, hashed_pw, role='user'):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(CREATE_USER, (username, email, hashed_pw, role))
                db.commit()

                cur.execute(GET_USER_BY_EMAIL_AFTER_CREATE, (email,))
                user = cur.fetchone()
                news_agg_logger(20, f"User {user['username']} created.")

                return dict(user) if user else None
        except Exception as e:
            news_agg_logger(40, f"Failed to create user: {e}")
            with get_db_cursor() as (cur, db):
                db.rollback()
            raise RepositoryException(f"Failed to create user: {e}")

    def email_exists(self, email: str):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(EMAIL_EXISTS, (email,))

                return cur.fetchone() is not None
        except Exception as e:
            raise RepositoryException(f"Failed to check if email exists: {e}")

    def get_all_users(self):
        try:
            with get_db_cursor() as (cur, db):
                cur.execute(GET_ALL_USERS)
                users = cur.fetchall()

                return users
        except Exception as e:
            raise RepositoryException(f"Failed to get all users: {e}")
