from datetime import datetime, UTC
from server.db.db_connection import DBConnection
from server.interfaces.i_external_api_repository import IExternalAPIRepository


class ExternalAPIRepository(IExternalAPIRepository):
    def update_status(self, name: str, status: str):
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("""
                UPDATE external_api_servers
                SET status = %s, last_accessed = %s
                WHERE api_name = %s
            """, (status, datetime.now(UTC), name))
            db.commit()
        finally:
            cur.close()
            db.close()

    def get_last_accessed(self, name: str) -> datetime:
        db = DBConnection()
        cur = db.get_cursor()
        try:
            cur.execute("SELECT last_accessed FROM external_api_servers WHERE api_name = %s", (name,))
            result = cur.fetchone()
            return result["last_accessed"] if result else datetime.now(UTC)
        finally:
            cur.close()
            db.close()

    def get_all_statuses(self):
        cur = DBConnection().get_cursor()
        cur.execute("SELECT api_name, status, last_accessed FROM external_api_servers")
        return cur.fetchall()

    def get_all_keys(self):
        cur = DBConnection().get_cursor()
        cur.execute("SELECT api_name, api_key, last_accessed FROM external_api_servers")
        return cur.fetchall()

    def update_api_key(self, api_name, api_key):
        cur = DBConnection().get_cursor()
        cur.execute(
            "UPDATE external_api_servers SET api_key = %s WHERE api_name = %s",
            (api_key, api_name)
        )
        DBConnection().commit()

    def get_api_keys(self):
        db = DBConnection()
        cur = db.get_cursor()
        cur.execute("""
            SELECT api_name, api_key FROM external_api_servers
        """)

        return {row['api_name']: row['api_key'] for row in cur.fetchall()}
