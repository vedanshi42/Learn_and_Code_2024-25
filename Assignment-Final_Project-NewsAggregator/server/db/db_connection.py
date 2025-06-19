import psycopg2
from psycopg2.extras import RealDictCursor
from server.config.settings import DB_SETTINGS


class DBConnection:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=DB_SETTINGS['host'],
                database=DB_SETTINGS['database'],
                user=DB_SETTINGS['user'],
                password=DB_SETTINGS['password']
            )
        except Exception as e:
            raise ConnectionError(f"Database connection failed: {e}")

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()
