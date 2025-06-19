from unittest.mock import patch, MagicMock
from server.db.db_connection import DBConnection


def test_db_connection_mocked():
    with patch("server.db.db_connection.psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db = DBConnection()
        cur = db.get_cursor()

        db.commit()
        db.rollback()
        db.close()

        mock_connect.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()
